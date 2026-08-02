from fastapi import FastAPI

from .database.base import Base
from .database.session import engine
from . import models
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, auth, doctors, schedule, appointments, visit_records, specialty , patients, review
print(Base.metadata.tables.keys())
# ساخت جدول‌ها
#Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clinic Appointment System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(schedule.router)
app.include_router(appointments.router)
app.include_router(visit_records.router)
app.include_router(users.router)
app.include_router(specialty.router)
app.include_router(patients.router)
app.include_router(review.router)

@app.get("/")
def root():
    return {"message": "Clinic Appointment System API"}