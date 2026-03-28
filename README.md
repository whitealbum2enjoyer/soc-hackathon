1. git init
2. git remote add origin https://github.com/whitealbum2enjoyer/soc-hackathon
3. git fetch origin
4. git checkout -b main
5. git reset --hard origin/main

# 📚 Marx Library Room Occupancy Tracker

A modern, full-stack application built for the **USA School of Computing Hackathon** to track and display real-time occupancy for library study rooms.

![Architecture](https://img.shields.io/badge/Architecture-Full--Stack-blue)
![Backend](https://img.shields.io/badge/Backend-Python%20%2F%20Flask-green)
![Frontend](https://img.shields.io/badge/Frontend-React%20%2F%20Vite-blueviolet)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)

---

## 🚀 One-Click Quick Start

Getting started is easy! You just need **Python** and **Node.js** installed.

### 1. Automatic Setup
This command installs all Python and React dependencies and initializes the database.
```bash
npm run setup
```

### 2. Start the Application
Run both the Python API and the React frontend simultaneously in a single terminal:
```bash
npm start
```
Your browser should automatically open to `http://localhost:5173`.

---

## 🛠️ Tech Stack

- **Frontend**: React.js with Vite, using premium Vanilla CSS for a custom dark-mode "Glassmorphism" UI.
- **Backend**: Python Flask REST API.
- **Security**: 
  - Parameterized SQL queries to prevent **SQL Injection**.
  - Secure password hashing using `Werkzeug`.
- **Database**: SQLite (relational database).

---

## 📖 Features

- **Real-time Occupancy**: Instantly see which rooms are "Available" (Green) or "Occupied" (Red).
- **Interactive Check-In/Out**: Simple one-click buttons to change room status.
- **User System**: Basic user registration and password verification.
- **Secure by Design**: Built with modern security best practices in mind.

---

## 👨‍💻 Project Structure

- `/app.py`: The main Flask API server.
- `/schema.sql`: The database blueprint.
- `/init_db.py`: Database initialization script.
- `/frontend/`: The React source code and assets.

---

## 📝 Hackathon Notes
- Created by Iven & Nando
- Built for the 2026 USA School of Computing Hackathon.
