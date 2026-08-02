from datetime import datetime, timedelta, date

from app.database.session import SessionLocal
from app import models
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.specialty import Specialty
from app.models.schedule import Schedule
from app.core.security import hash_password


db = SessionLocal()


def seed_specialties():
    specialties = [
        ("CAR", "Cardiology"),
        ("DER", "Dermatology"),
        ("DEN", "Dentistry"),
        ("NEU", "Neurology"),
        ("ORT", "Orthopedics"),
        ("PED", "Pediatrics"),
        ("PSY", "Psychiatry"),
    ]

    for code, title in specialties:
        existing = db.query(Specialty).filter(
            Specialty.code == code
        ).first()

        if not existing:
            db.add(
                Specialty(
                    code=code,
                    title=title
                )
            )

    db.commit()


def seed_admin():
    existing = db.query(User).filter(
        User.mobile == "09111111111"
    ).first()

    if existing:
        return

    admin = User(
        first_name="System",
        last_name="Admin",
        mobile="09111111111",
        email="admin@clinic.com",
        hashed_password=hash_password("admin123"),
        role="admin",
        gender="male",
        birth_date=date(1990, 1, 1)
    )

    db.add(admin)
    db.commit()


def seed_doctors():
    doctors_data = [
        {
            "first_name": "Fatemeh",
            "last_name": "Rezai",
            "mobile": "09120000001",
            "email": "doctor1@clinic.com",
            "specialty": "DER",
            "experience": 8
        },
        {
            "first_name": "Ali",
            "last_name": "Mohammadi",
            "mobile": "09120000002",
            "email": "doctor2@clinic.com",
            "specialty": "CAR",
            "experience": 12
        },
        {
            "first_name": "Sara",
            "last_name": "Ahmadi",
            "mobile": "09120000003",
            "email": "doctor3@clinic.com",
            "specialty": "NEU",
            "experience": 6
        }
    ]

    for item in doctors_data:

        user = db.query(User).filter(
            User.mobile == item["mobile"]
        ).first()

        if not user:

            user = User(
                first_name=item["first_name"],
                last_name=item["last_name"],
                mobile=item["mobile"],
                email=item["email"],
                hashed_password=hash_password("123456"),
                role="doctor",
                gender="female"
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        doctor = db.query(Doctor).filter(
            Doctor.user_id == user.id
        ).first()

        if not doctor:

            db.add(
                Doctor(
                    user_id=user.id,
                    specialty_code=item["specialty"],
                    experience_years=item["experience"]
                )
            )

            db.commit()


def seed_patients():

    patients = [
        {
            "first_name": "Aylin",
            "last_name": "Parvizi",
            "mobile": "09130000001",
            "email": "patient1@gmail.com"
        },
        {
            "first_name": "Reza",
            "last_name": "Karimi",
            "mobile": "09130000002",
            "email": "patient2@gmail.com"
        },
        {
            "first_name": "Maryam",
            "last_name": "Hosseini",
            "mobile": "09130000003",
            "email": "patient3@gmail.com"
        },
        {
            "first_name": "Nima",
            "last_name": "Safari",
            "mobile": "09130000004",
            "email": "patient4@gmail.com"
        },
        {
            "first_name": "Zahra",
            "last_name": "Jafari",
            "mobile": "09130000005",
            "email": "patient5@gmail.com"
        }
    ]

    for item in patients:

        user = db.query(User).filter(
            User.mobile == item["mobile"]
        ).first()

        if not user:

            user = User(
                first_name=item["first_name"],
                last_name=item["last_name"],
                mobile=item["mobile"],
                email=item["email"],
                hashed_password=hash_password("123456"),
                role="patient"
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        patient = db.query(Patient).filter(
            Patient.user_id == user.id
        ).first()

        if not patient:

            db.add(
                Patient(
                    user_id=user.id,
                    medical_history="None",
                    medications="None"
                )
            )

            db.commit()


def seed_schedules():

    doctors = db.query(Doctor).all()

    tomorrow = datetime.now() + timedelta(days=1)

    for doctor in doctors:

        for i in range(5):

            start = tomorrow.replace(
                hour=9 + i,
                minute=0,
                second=0,
                microsecond=0
            )

            end = start + timedelta(minutes=30)

            exists = db.query(Schedule).filter(
                Schedule.doctor_id == doctor.id,
                Schedule.start_time == start
            ).first()

            if not exists:

                db.add(
                    Schedule(
                        doctor_id=doctor.id,
                        start_time=start,
                        end_time=end,
                        status="available"
                    )
                )

    db.commit()


if __name__ == "__main__":

    seed_specialties()
    seed_admin()
    seed_doctors()
    seed_patients()
    seed_schedules()

    print("Seed completed successfully.")