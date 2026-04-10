# 🏢 Biometric Hostel Attendance System

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![DeepFace](https://img.shields.io/badge/DeepFace-FF6F00?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

A strictly-enforced Full-Stack Biometric application designed to flawlessly track hostel student attendance. 
It uses **React.js** on the frontend to dynamically capture webcam snapshots, and a high-performance **FastAPI** Python backend powered by **DeepFace (Facenet512)** neural networks to precisely map and verify facial structures!

## ✨ Key Features
- **Facial Biometric Verification:** Utilizes the DeepFace AI engine to strictly enforce 85% Cosine Similarity metrics against FaceNet structural dimension rules.
- **Intranet Whitelisting:** Aggressively secures the attendance and login API endpoints using SQLite Subnet blocking algorithms (e.g. requires routing from `172.16.x.x`), fundamentally preventing off-site attendance fraud!
- **Interactive Admin Dashboard:** A dark-mode optimized React portal to dynamically search 10,000+ students on the fly, purge user data flexibly, register new student faces, and visually audit real-time attendance system logs.
- **JWT Security:** Completely stateless session tokenization hashed natively via the `bcrypt` standard.

## 🚀 Local Installation

### 1. Backend Setup
Make sure you are strictly running a stable **Python 3.10** LTS virtual environment to guarantee that heavy ML dependencies like `tensorflow` and `numpy` C-extensions compile safely on Windows OS.
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install deepface tensorflow opencv-python-headless --no-cache-dir
```
Copy the `.env.example` into a new `.env` file, then boot the server:
```bash
uvicorn app.main:app --reload --port 8000
```
### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The application will elegantly boot up at `http://localhost:5173`. 
*(Default Administrative Master Account: `admin` / `admin`)*
