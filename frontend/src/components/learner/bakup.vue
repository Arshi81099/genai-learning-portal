<template>
    <div class="main-tutor">
      <header class="header">
        <div class="username">{{ username }}</div>
        <h1>{{ courseName }}: Learner Portal</h1>
        <button class="sign-out" @click="signOut">Sign Out</button>
      </header>
      <div class="content">
        <aside class="sidebar">
          <ul>
            <li @click="selectSection('about')" :class="{ active: selectedTopic === 'about' }">About</li>
            <li v-for="topic in topics" :key="topic.id" class="topic">
              <div @click="toggleTopic(topic.id)" :class="{ active: selectedTopic === topic.id }">
                {{ topic.name }}
                <span class="arrow" :class="{ down: selectedTopic === topic.id }">&#9660;</span>
              </div>
              <ul v-if="selectedTopic === topic.id" class="topic-content">
                <li v-if="topic.content.video" @click="selectContent('video', topic.id)" :class="{ active: selectedContent === 'video' && selectedTopic === topic.id }">
                  Video
                </li>
                <li v-if="topic.content.quiz" @click="selectContent('quiz', topic.id)" :class="{ active: selectedContent === 'quiz' && selectedTopic === topic.id }">
                  Quiz
                </li>
                <li v-if="topic.content.codingQuiz" @click="selectContent('codingQuiz', topic.id)" :class="{ active: selectedContent === 'codingQuiz' && selectedTopic === topic.id }">
                  Coding Quiz
                </li>
              </ul>
            </li>
          </ul>
        </aside>
        <main class="main-content">
          <div v-if="selectedTopic === 'about'">
            <p>This is all about Course information and About Instructor.</p>
          </div>
          <div v-else-if="selectedContent === 'video'">
            <h1>Video</h1>
            <div v-if="!video.link">
              <p>The content will be added soon</p>
            </div>
            <div v-else>
              <iframe :src="video.link" frameborder="0" allowfullscreen></iframe>
            </div>
          </div>
          <div v-else-if="selectedContent === 'quiz'">
            <h1>Quiz</h1>
            <div v-if="quizQuestions.length === 0">
              <p>The content will be added soon</p>
            </div>
            <form v-else @submit.prevent="submitQuiz">
              <ol>
                <li v-for="question in quizQuestions" :key="question.id">
                  <div>{{ question.question }}</div>
                  <ul>
                    <li v-for="(option, index) in question.options" :key="index">
                      <label>
                        <input type="radio" :name="'question-' + question.id" :value="option" v-model="userAnswers[question.id]" />
                        {{ option }}
                      </label>
                    </li>
                  </ul>
                  <div v-if="submitted">
                    <span v-if="userAnswers[question.id] === question.correct_option" style="color: green;">&#10004; Correct</span>
                    <span v-else style="color: red;">&#10008; Incorrect</span>
                    <div><strong>Correct Answer:</strong> {{ question.correct_option }}</div>
                  </div>
                </li>
              </ol>
              <button class="submit-btn" type="submit">Submit</button>
            </form>
            <div v-if="submitted">
              <h2>Your Score: {{ score }} / {{ quizQuestions.length }}</h2>
            </div>
          </div>
          <div v-else-if="selectedContent === 'codingQuiz'">
            <div v-if="!codingQuiz.question">
              <p>The content will be added soon</p>
            </div>
            <div v-else>
              <div>
                <strong>Programming language: </strong>{{ codingQuiz.language }}
              </div>
              <p>{{ codingQuiz.question }}</p>
              <p>Input: {{ codingQuiz.test_cases[0] }}</p>
              <p>Expected Output: {{ codingQuiz.test_cases[1] }}</p>
              <textarea class="code-editor" v-model="codingAnswer" placeholder="Write your code here..."></textarea>
              <button class="submit-btn" @click="submitCode">Submit Code</button>
              <div v-if="submittedCode">
                <p v-if="passed" style="color: green;">All test cases passed!</p>
                <p v-else style="color: red;">
                  Test cases failed. 
                  <button class="ai-help-btn" @click="takeHelpFromAI">Take help from AI</button>
                </p>
                <div v-if="aiHelpResponse" class="ai-help-response">
                  <h3>AI Assistance:</h3>
                  <p>{{ aiHelpResponse }}</p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import axiosFetch from '@/axios';
  import { GoogleGenerativeAI } from "@google/generative-ai";
  
  export default {
    name: 'MainLearner',
    props: ['courseId', 'courseName'],
    data() {
      return {
        username: null,
        currentQuizId: null,
        selectedTopic: 'about',
        selectedContent: null,
        topics: [],
        video: {},
        quizQuestions: [],
        codingQuiz: {},
        codingAnswer: '', // Store user's code answer
        userAnswers: {},
        score: 0,
        submitted: false,
        submittedCode: false,
        passed: false,
        aiHelpResponse: null, // Store AI help response
        model: null
      };
    },
    async created() {
      this.fetchUsername();
        try {
          const API_KEY = "AIzaSyCESDMdIk_sDsBtW7eoaD_JFnOjvuwTgfg";
          const genAI = new GoogleGenerativeAI(API_KEY);
          this.model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        } catch (error) {
          console.error("Error initializing the model:", error);
        }
      },
    methods: {
      async fetchUsername() {
        try {
          const resp = await axiosFetch.get('/api/info/username');
          this.username = resp.data.username;
          await this.fetchTopics();
        } catch (error) {
          console.error('Error in getting username:', error);
        }
      },
      async fetchTopics() {
        try {
          const resp = await axiosFetch.get(`/api/learner/course/get-topics`, { params: { courseId: this.courseId } });
          this.topics = resp.data;
        } catch (error) {
          console.error('Error fetching topics:', error);
        }
      },
      selectSection(section) {
        this.selectedTopic = section;
        this.selectedContent = null;
      },
      toggleTopic(topicId) {
        this.selectedTopic = this.selectedTopic === topicId ? null : topicId;
        this.selectedContent = null;
      },
      async selectContent(content, topicId) {
        this.selectedContent = content;
        this.selectedTopic = topicId;
        await this.fetchContent(topicId);
      },
      async fetchContent(topicId) {
        try {
          const resp = await axiosFetch.get(`/api/learner/topic/content`, { params: { 'topicId': topicId, 'type': this.selectedContent } });
          const content = resp.data;
  
          if (content.type === 'video') {
            this.video = content.details;
            this.quizQuestions = [];
            this.codingQuiz = {};
          } else if (content.type === 'quiz') {
            this.currentQuizId = content.quizId;
            this.quizQuestions = content.details || [];
            this.video = {};
            this.codingQuiz = {};
            this.userAnswers = {};
            this.submitted = false;
            this.score = 0;
          } else if (content.type === 'codingQuiz') {
            this.codingQuiz = content.details;
            this.video = {};
            this.quizQuestions = [];
          }
  
        } catch (error) {
          console.error('Error fetching topic content:', error);
        }
      },
      submitQuiz() {
        this.submitted = true;
        this.calculateScore();
      },
      calculateScore() {
        this.score = 0;
        this.quizQuestions.forEach(question => {
          if (this.userAnswers[question.id] === question.correct_option) {
            this.score++;
          }
        });
      },
      async submitCode() {
        const code = this.codingAnswer;
        const input = this.codingQuiz.test_cases[0];
  
        try {
          const response = await axios.post('https://emkc.org/api/v2/piston/execute', {
            language: this.codingQuiz.language, // Dynamic language selection
            version: this.getLanguageVersion(this.codingQuiz.language), // Get appropriate language version
            files: [
              {
                content: code
              }
            ],
            stdin: input
          });
  
          const output = response.data.run.output.trim();
          this.passed = output === this.codingQuiz.test_cases[1];
          this.submittedCode = true;
        } catch (error) {
          console.error('Error submitting code:', error);
        }
      },
      getLanguageVersion(language) {
        const versions = {
          python: '3.10.0',
          java: '17.0.0',
          javascript: 'node-18.0.0',
          // Add other languages and versions as needed
        };
        return versions[language] || 'latest';
      },
      async signOut() {
        try {
          localStorage.removeItem('authToken');
          this.$router.push({ name: 'landingPage' });
        } catch (error) {
          console.error('Error logging out:', error);
        }
      },
      async takeHelpFromAI() {
        const prompt = `Language: ${this.codingQuiz.language}\nQuestion: ${this.codingQuiz.question}\nInput: ${this.codingQuiz.test_cases[0]}\nExpected Output: ${this.codingQuiz.test_cases[1]}\nCode:\n${this.codingAnswer}\n\nWhat is the error in this code and how can I resolve it?`;
        
        try {
          const result = await this.generateText(prompt);
          this.aiHelpResponse = result.response.text();
        } catch (error) {
          console.error('Error getting help from AI:', error);
          this.aiHelpResponse = "Sorry, something went wrong while getting help from AI.";
        }
      },
      async generateText(prompt) {
        try {
          const result = await this.model.generateContent(prompt);
          return result;
        } catch (error) {
          console.error("Error generating text:", error);
          throw error;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .main-tutor {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #53df7d;
    color: white;
    padding: 10px;
  }
  .username {
    font-size: 1.2em;
  }
  .sign-out {
    background-color: rgb(0, 157, 255);
    color: white;
    border: none;
    padding: 10px;
    cursor: pointer;
  }
  .content {
    display: flex;
    flex: 1;
  }
  .sidebar {
    width: 250px;
    background-color: #f4f4f4;
    padding: 10px;
  }
  .sidebar ul {
    list-style-type: none;
    padding: 0;
  }
  .sidebar ul li {
    padding: 10px;
    cursor: pointer;
  }
  .sidebar ul li.active {
    background-color: #53df7d;
    color: white;
  }
  .sidebar ul li .arrow {
    float: right;
  }
  .sidebar ul li .arrow.down {
    transform: rotate(180deg);
  }
  .topic-content {
    padding-left: 20px;
  }
  .main-content {
    flex: 1;
    padding: 20px;
  }
  .main-content iframe {
    width: 100%;
    height: 400px;
  }
  button {
    margin: 10px 0;
  }
  .submit-btn, .ai-help-btn {
    background-color: #007BFF;
    color: white;
    border: none;
    padding: 10px;
    cursor: pointer;
    border-radius: 5px;
  }
  .submit-btn:hover, .ai-help-btn:hover {
    background-color: #0056b3;
  }
  .code-editor {
    width: 100%;
    height: 150px;
    margin: 10px 0;
    font-family: monospace;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  .ai-help-response {
    margin-top: 20px;
    background-color: #f1f1f1;
    padding: 15px;
    border-radius: 5px;
  }
  </style>
  