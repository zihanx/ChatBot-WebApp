# ChatBot-WebApp
A full-stack **Django web application** that provides users with LLM-based mental wellness support.

## Features (Technical details)

- **Chat with AI** – Interact with a mental wellness assistant with Gemini API.
  - Integrates single point chat completion API with Gemini. The project maintains a .xml prompt template for a structured prompt (`chatbot/templates/chatbot/prompt_template.xml`).
  - Maintains chat context. In the template, the projects dynamically injects previous chat history to prompt and also user's infomation to remember context.
  - Limit token counts. To prevent the long prompt from negatively impacting the response, the project summarizes the previous half of the chat history and keep the latest half when excceeds certain threshold, shrinking the total tokens of the prompt (`chatbot/utils/prompt.py`).
  - Stream output. The project uses SseEmitter to stream response to user.
- **User Profiles** – Customize personal infomation and mental health status.
  - Dynamically rendered with prompt template. The user's information will be integrated into the user context section in the prompt.

## Tech Stack
- **Backend:** Django 
- **Frontend:** Django Templates, HTML, CSS 
- **Database:** SQLite
- **AI Integration:** Gemini API

## Getting Started
### Dependencies
Make sure to have Django environment.
### Configure .env
Copy the .env.sample and rename it to be .env, replace your own secret key
### Run migration and start the app
```
python manage.py migrate
python manage.py runserver
```
Visit http://localhost:8000 to get started.
