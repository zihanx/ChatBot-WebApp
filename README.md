# ChatBot-WebApp
A full-stack **Django web application** that provides users with LLM-based mental wellness support.

## Features

- **Chat with AI** – Interact with a mental wellness assistant with Gemini API.
- **User Profiles** – Customize personal infomation and mental health status.

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