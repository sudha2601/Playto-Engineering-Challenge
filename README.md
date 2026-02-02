# Project Name

A full-stack web application featuring a nested comment system and a real-time activity leaderboard.

---

## 🚀 Live Demo

https://playto-engineering-challenge-kgdg.vercel.app/

---

## 📄 Documentation

For details on the database modeling (**The Tree**), the leaderboard logic (**The Math**), and the AI generation audit, please see:

- `EXPLAINER.md`

---

## 🛠 Local Development Setup

### Prerequisites

Make sure you have the following installed:

- Python 3.8+  
- Node.js (v16+ recommended)  
- pip  
- npm or yarn  
- Docker & Docker Compose (optional)

---

## 📥 Clone the Repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

---

## 🔧 Backend Setup (Local)

1. Enter the backend directory:
   ```bash
   cd backend
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # macOS / Linux
   source .venv/bin/activate
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. (Optional) Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

Backend runs at:
http://127.0.0.1:8000/

---

## 🎨 Frontend Setup (Local)

Open a new terminal:

1. Enter the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn
   ```

3. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

Frontend runs at:
http://localhost:5173/

---

## 🐳 Running with Docker (Frontend Only)

The frontend is dockerized. The backend in the demo is deployed on Render.

From the project root, build and run:

```bash
docker compose up --build
```

Frontend will be available at:
http://localhost:5173/

To stop and remove containers:
```bash
docker compose down
```

> Note: If you want to run the backend via Docker as well, add a backend service and a PostgreSQL service to the compose file, and update environment variables accordingly.

---

## Testing

A basic Django test is included to validate the leaderboard logic.
The test verifies:
Post likes give +5 karma to the post author
Comment likes give +1 karma to the comment author
Only likes from the last 24 hours are counted
Older likes are ignored

Backend:
```bash
cd backend
python manage.py test
```

## 💻 Tech Stack

- Backend: Django (Python), Django REST Framework  
- Frontend: React, Vite  
- Database: SQLite (local) / PostgreSQL (production)  
- Containerization: Docker (frontend)  
- Hosting (demo): Render (backend) & Vercel (frontend)

---



