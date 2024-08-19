from flask import session, request, abort, jsonify
from flask_restful import Resource,reqparse
from sqlalchemy import distinct
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity


class allMyCourses(Resource):
    @jwt_required()
    def get(self):
        username = request.args.get('username', None)
        # Handle missing username parameter
        if not username:
            return {"message": "Username parameter is missing."}, 400
        combined_data = db.session.query(Course, MyCourses).join(
            Course, MyCourses.courseId == Course.courseId
            ).filter(MyCourses.username == username).all()
        
        result = []
        if combined_data != []:
            for course, my_courses in combined_data:
                result.append({
                    'courseId': my_courses.courseId,
                    'courseName': course.courseName,
                })
        return result, 200
    
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

class fetch_transcript(Resource):
    def get(self):
        try:
            data = request.json
            video_id =data['videoId']
            # Fetch the transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            # Format the transcript as JSON
            formatter = JSONFormatter()
            json_transcript = formatter.format_transcript(transcript)
            print(json_transcript)
            return {'message': 'success'}
        except Exception as e:
            return {'message': 'failed '}
            return str(e)