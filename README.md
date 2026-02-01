# Project Name

A full-stack web application featuring a nested comment system and a real-time activity leaderboard.

## 🚀 Live Demo
**[[Link to your deployed website here](https://playto-engineering-challenge-kgdg.vercel.app/)]**

## 📄 Documentation
For details on the database modeling (The Tree), the leaderboard logic (The Math), and the AI generation audit, please see:
[**EXPLAINER.md**](./EXPLAINER.md)

---

## 🛠️ Local Development Setup

Follow these steps to run the application locally.

### Prerequisites
* Python installed
* Node.js installed

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-project-folder>

### 2. Backend setup
Navigate to the backend directory to start the Django server.

```bash
# Enter the backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run migrations to setup the database
python manage.py migrate

# Start the server
python manage.py runserver
The backend API is now running at http://127.0.0.1:8000/

### 3. Frontend Setup
Open a new terminal and navigate to the frontend directory.

Note: node_modules are included in the repository, so no installation is required.

```bash
# Enter the frontend directory
cd frontend

# Start the development server
npm run dev
The frontend is now running at http://localhost:3000/ (or the port shown in your terminal).

###💻 Tech Stack
Backend: Python (Django)

Frontend: Node.js / React

Database: SQLite / PostgreSQL (Update as needed)
