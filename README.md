# DIEMS Events - College Event Management Platform

DIEMS Events is a premium, AI-powered Full-Stack Event Management Platform designed specifically for college events and fests. It centralizes communication, provides real-time updates via WebSockets, handles registrations with QR code ticketing, and offers role-based dashboards for Students, Organizers, and Admins.

## Features

- **Premium UI/UX**: Built with React, Tailwind CSS, Framer Motion, and GSAP-inspired animations. Dark mode glassmorphism design.
- **Role-Based Access**:
  - **Students**: Discover events, register, view tickets, receive real-time notifications.
  - **Organizers**: Create events, manage registrations, view analytics.
  - **Admins**: Manage users, oversee platform statistics.
- **Real-Time Notifications**: Integrated `Flask-SocketIO` to push instant updates without refreshing.
- **QR Code Ticketing**: Automatic QR code generation upon successful registration.
- **AI Recommendations (Mock)**: Suggests upcoming events based on the user's department and interests.
- **API Documentation**: Auto-generated Swagger UI.

## Tech Stack

- **Frontend**: React (Vite), Tailwind CSS, Framer Motion, Zustand, Axios, Socket.IO Client.
- **Backend**: Python Flask, SQLAlchemy (MySQL/SQLite), JWT-Extended, Flask-SocketIO, Flasgger (Swagger), qrcode.

---

## Setup Instructions

### 1. Backend Setup

Ensure you have Python 3.9+ installed.

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

# Install dependencies (If requirements.txt doesn't exist, install these manually)
pip install flask flask-cors python-dotenv flask-sqlalchemy flask-jwt-extended werkzeug flask-socketio flasgger qrcode[pil]

# Seed the database with dummy data
python seed.py

# Run the server
python app.py
```
*The backend runs on `http://localhost:5000`.*
*View API Documentation at `http://localhost:5000/apidocs`.*

### 2. Frontend Setup

Ensure you have Node.js 18+ installed.

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```
*The frontend typically runs on `http://localhost:5173`.*

---

## Environment Variables

Copy `.env.example` to `.env` in the root directory and configure as needed:

```env
DATABASE_URL=sqlite:///app.db
SECRET_KEY=super_secret_dev_key_123!
JWT_SECRET_KEY=super_secret_jwt_key_456!
VITE_API_URL=http://localhost:5000/api
```
*(Note: To use MySQL in production, change `DATABASE_URL` to `mysql+pymysql://user:password@localhost/diems_events`)*

---

## Deployment Instructions

### Backend (Render / Heroku)
1. Ensure `gunicorn` and `eventlet` are installed for production WSGI.
2. Set up a PostgreSQL or MySQL database on your hosting provider.
3. Add the database URI to the environment variables.
4. Command: `gunicorn -k eventlet -w 1 app:app`

### Frontend (Vercel / Netlify)
1. In the `frontend` directory, run `npm run build`.
2. Connect your GitHub repository to Vercel.
3. Ensure the Build Command is `npm run build` and Output Directory is `dist`.
4. Add `VITE_API_URL` to the Vercel Environment Variables pointing to your hosted backend URL.

## Database Schema
Refer to `database_schema.sql` for the raw MySQL schema and ER Diagram relationships.
