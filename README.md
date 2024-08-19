# GENAI Learning Portal

## Overview
GENAI Learning Portal is an educational platform designed to enhance learning experiences by integrating advanced AI technologies. The portal offers a variety of features to support both learners and tutors.

## Project Structure

### Backend
- **Language:** Python
- **Files:**
  - `admin.py`: Handles administrative functionalities.
  - `app.py`: The main entry point for the backend server.
  - `auth.py`: Manages authentication and authorization.
  - `config.py`: Contains configuration settings.
  - `learner.py`: Handles learner-specific functionalities.
  - `models.py`: Defines the database models.
  - `tutor.py`: Manages tutor-related functionalities.

### Frontend
- **Framework:** Vue.js
- **Files:**
  - `App.vue`: The main Vue component.
  - `axios.js`: Configures Axios for HTTP requests.
  - `main.js`: Initializes and configures the Vue instance.
  - **Directories:**
    - `public`: Contains static files and the main `index.html`.
    - `src/assets`: Contains images, stylesheets, and other assets.
    - `src/components`: Vue components used in the application.
    - `src/routes`: Contains route definitions for the application.

## Setup Instructions

### Backend
1. **Install dependencies:**
   - pip install -r requirements.txt

2. **Run python:**
    - python app.py


### Frontend
1. **Install dependencies:**
npm install

2. **Run the development server:**
npm run serve


## Features
- **User Authentication:** Secure login and registration for learners and tutors.
- **Course Management:** Tutors can create and manage courses.
- **Interactive Learning:** Learners can participate in interactive lessons and quizzes.


## Screenshots
1. Home Page:

2. Course Page:

3. Admin Dashboard:
