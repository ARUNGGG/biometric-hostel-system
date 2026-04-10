# Hostel Biometric Attendance System

This project contains a fullstack application implementing biometric attendance.

## System Requirements
- Python 3.9+
- Node.js 18+
- PostgreSQL database server running locally or externally.

## Backend Setup (FastAPI)

1. Open a terminal and navigate to the `backend` folder.
2. Ensure you have activated your python environment, or simply use your core python package if dependencies aren't strict.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure `.env`:
   Update the `DATABASE_URL` in `backend/.env` to point to a valid PostgreSQL database.
5. Run the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

## Frontend Setup (React / Vite)

1. Open a new terminal and navigate to the `frontend` folder.
2. Install npm modules:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## Admin Initialization
Upon first boot, use the interactive setup at `http://localhost:8000/docs` to register an admin student manually and add allowed subnets (e.g `127.0.0.0/8`, `192.168.1.0/24`) to permit local traffic.
