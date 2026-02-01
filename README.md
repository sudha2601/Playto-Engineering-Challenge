Project Name

A full-stack web application featuring a nested comment system and a real-time activity leaderboard.

🚀 Live Demo

https://playto-engineering-challenge-kgdg.vercel.app/

📄 Documentation

For details on the database modeling (The Tree), the leaderboard logic (The Math), and the AI generation audit, please see:

EXPLAINER.md

🛠 Local Development Setup
Prerequisites

Python

Node.js

Clone the Repository
git clone <your-repo-url>
cd <your-project-folder>

Backend Setup
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


Backend runs at:

http://127.0.0.1:8000/

Frontend Setup

Open a new terminal:

cd frontend
npm run dev


Frontend runs at:

http://localhost:3000/


(or the port shown in terminal)

Tech Stack
Backend

Django

Frontend

React

Database

SQLite / PostgreSQL
