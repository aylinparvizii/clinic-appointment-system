# 🏥 Clinic Appointment System API

A RESTful backend API for managing a clinic appointment system.

This project is built with **FastAPI**, **SQLAlchemy**, **Microsoft SQL Server**, **JWT Authentication**, and **Alembic**.

---

# ✨ Features

## Authentication

- User Registration
- User Login
- JWT Authentication
- Password Hashing (bcrypt)
- Protected Endpoints

---

## Authorization

Role Based Access Control (RBAC)

Supported roles:

- 👨‍⚕️ Doctor
- 🧑 Patient
- 👨‍💼 Admin

Each role has different permissions.

---

# 👨‍⚕️ Doctor Module

Doctors can:

- View appointments
- Create schedules
- Update schedules
- Delete schedules
- Create visit records
- View patient information
- View received reviews

---

# 🧑 Patient Module

Patients can:

- Register
- Login
- View doctors
- View doctor schedules
- Book appointments
- Cancel appointments
- View appointment history
- Submit doctor reviews
- View visit records

---

# 👨‍💼 Admin Module

Admins can:

- View all users
- Change user role
- Activate / Deactivate users

---

# 📅 Appointment Management

Appointment workflow:

Available Schedule

↓

Book Appointment

↓

Completed

↓

Visit Record

↓

Review

Appointment statuses:

- scheduled
- completed
- cancelled

---

# 📝 Visit Records

Doctors can create medical reports after appointments.

Each visit record contains:

- Diagnosis
- Prescription
- Notes
- Visit Date

Patients can later access their medical history.

---

# ⭐ Reviews

Patients can

- Rate doctors (1–5)
- Leave comments

Doctors can

- View all reviews
- View ratings

---

# 🗄 Database

Microsoft SQL Server

Tables:

- Users
- Doctors
- Patients
- Specialties
- Schedules
- Appointments
- VisitRecords
- Reviews

Database migrations are managed using **Alembic**.

---

# 🛠 Tech Stack

## Backend

- FastAPI
- Python 3.11+
- SQLAlchemy ORM
- Pydantic

## Database

- Microsoft SQL Server
- Alembic

## Authentication

- JWT
- OAuth2 Password Bearer
- Passlib (bcrypt)

## Testing

- Pytest
- FastAPI TestClient

## Containerization

- Docker
- Docker Compose

---

# 📂 Project Structure

```
backend
│
├── alembic/
│
├── app/
│   │
│   ├── core/
│   │   ├── logger.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   ├── dependencies.py
│   │   └── session.py
│   │
│   ├── models/
│   │
│   ├── routers/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   ├── tests/
│   │
│   ├── seed.py
│   │
│   └── main.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

# ⚙ Installation

Clone repository

```bash
git clone https://github.com/<your-username>/clinic-appointment-system.git
```

Go to project

```bash
cd clinic-project/backend
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file.

Example:

```env
DATABASE_URL=mssql+pyodbc://sa:password@localhost/clinicDB?driver=ODBC+Driver+17+for+SQL+Server

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# 🗃 Database Migration

Generate migration

```bash
alembic revision --autogenerate -m "Initial migration"
```

Apply migrations

```bash
alembic upgrade head
```

---

# 🌱 Seed Database

Populate sample data

```bash
python -m app.seed
```

This creates:

- Admin account
- Doctors
- Patients
- Specialties
- Schedules

---

# ▶ Running the Project

Development

```bash
uvicorn app.main:app --reload
```

API Documentation

Swagger

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# 🐳 Run with Docker

Build containers

```bash
docker compose up --build
```

Stop containers

```bash
docker compose down
```

---

# 🧪 Run Tests

```bash
pytest -v
```

Current tests include:

- Authentication
- Authorization
- Users
- Doctors
- Schedules
- Appointments
- Reviews
- Visit Records
- Validation

---

# 🔑 Authentication

Login returns a JWT token.

Use it in requests:

```
Authorization: Bearer <access_token>
```

---

# 📌 API Endpoints

| Module | Endpoint |
|---------|----------|
| Auth | `/auth` |
| Users | `/users` |
| Doctors | `/doctors` |
| Patients | `/patients` |
| Specialties | `/specialties` |
| Schedules | `/schedules` |
| Appointments | `/appointments` |
| Visit Records | `/visit-records` |
| Reviews | `/reviews` |

---

# 🚀 Future Improvements

- Vue.js Frontend
- Email Notifications
- SMS Notifications
- Payment Gateway
- Advanced Search & Filtering
- Pagination
- Logging Dashboard
- CI/CD Pipeline
- Kubernetes Deployment

---

# 👩‍💻 Author

**Aylin**

Backend Developer Portfolio Project

GitHub:
https://github.com/aylinparvizii