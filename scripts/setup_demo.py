from datetime import datetime, timedelta
from pathlib import Path
import sys

# Allow imports from the project root when running this script directly.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import select

from app.database.database import Base, engine
from app.database.session import SessionLocal

# Import every model so SQLAlchemy knows about all tables.
from app.models.user import User
from app.models.health_profile import HealthProfile
from app.models.risk_profile import RiskProfile
from app.models.report import Report
from app.models.health_measurement import HealthMeasurement

from app.services.auth_service import hash_password


DEMO_EMAIL = "demo@healthplatform.com"
DEMO_PASSWORD = "Demo@12345"


def setup_database():
    """Create all database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)


def setup_demo_data():
    """Create a reusable demo account and health data."""
    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # 1. Find or create demo user
        # ---------------------------------------------------------
        statement = select(User).where(User.email == DEMO_EMAIL)
        user = db.execute(statement).scalar_one_or_none()

        if user is None:
            user = User(
                name="Demo User",
                email=DEMO_EMAIL,
                password_hash=hash_password(DEMO_PASSWORD),
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            print("Created demo user.")
        else:
            # Make sure an existing demo account can still log in.
            user.password_hash = hash_password(DEMO_PASSWORD)
            user.is_deleted = False
            user.deleted_at = None

            db.commit()
            db.refresh(user)

            print("Demo user already exists. Login credentials refreshed.")

        # ---------------------------------------------------------
        # 2. Health profile
        # ---------------------------------------------------------
        health_profile = db.execute(
            select(HealthProfile).where(
                HealthProfile.user_id == user.id
            )
        ).scalar_one_or_none()

        if health_profile is None:
            health_profile = HealthProfile(
                user_id=user.id,
                age=22,
                weight=70.0,
                height=175.0,
            )

            db.add(health_profile)
            print("Created demo health profile.")
        else:
            print("Demo health profile already exists.")

        # ---------------------------------------------------------
        # 3. Risk profile
        # ---------------------------------------------------------
        risk_profile = db.execute(
            select(RiskProfile).where(
                RiskProfile.user_id == user.id
            )
        ).scalar_one_or_none()

        if risk_profile is None:
            risk_profile = RiskProfile(
                user_id=user.id,
                sex=1,
                general_health=1,
                physical_health_days=2,
                physical_activity=1,
                smoking=0,
                alcohol=0,
            )

            db.add(risk_profile)
            print("Created demo risk profile.")
        else:
            print("Demo risk profile already exists.")

        db.commit()

        # ---------------------------------------------------------
        # 4. Demo report
        # ---------------------------------------------------------
        report_filename = "hackathon_demo_report.txt"

        report = db.execute(
            select(Report).where(
                Report.user_id == user.id,
                Report.filename == report_filename,
            )
        ).scalar_one_or_none()

        if report is None:
            report = Report(
                user_id=user.id,
                filename=report_filename,
                file_hash=None,
                report_type="Health Checkup",
                report_date=datetime.now(),
                uploaded_at=datetime.now(),
                status="analyzed",
            )

            db.add(report)
            db.commit()
            db.refresh(report)

            print("Created demo report.")
        else:
            print("Demo report already exists.")

        # ---------------------------------------------------------
        # 5. Demo measurements
        # ---------------------------------------------------------
        existing_measurements = db.execute(
            select(HealthMeasurement).where(
                HealthMeasurement.report_id == report.id
            )
        ).scalars().all()

        if not existing_measurements:
            measurement_date = datetime.now() - timedelta(days=7)

            measurements = [
                HealthMeasurement(
                    user_id=user.id,
                    report_id=report.id,
                    metric="BMI",
                    value=22.9,
                    unit="kg/m²",
                    measured_at=measurement_date,
                ),
                HealthMeasurement(
                    user_id=user.id,
                    report_id=report.id,
                    metric="Heart Rate",
                    value=72,
                    unit="bpm",
                    measured_at=measurement_date,
                ),
                HealthMeasurement(
                    user_id=user.id,
                    report_id=report.id,
                    metric="Systolic Blood Pressure",
                    value=120,
                    unit="mmHg",
                    measured_at=measurement_date,
                ),
                HealthMeasurement(
                    user_id=user.id,
                    report_id=report.id,
                    metric="Diastolic Blood Pressure",
                    value=80,
                    unit="mmHg",
                    measured_at=measurement_date,
                ),
            ]

            db.add_all(measurements)
            db.commit()

            print("Created demo health measurements.")
        else:
            print("Demo measurements already exist.")

        print()
        print("=" * 55)
        print("HEALTH INTELLIGENCE PLATFORM - DEMO SETUP")
        print("=" * 55)
        print(f"Demo email:    {DEMO_EMAIL}")
        print(f"Demo password: {DEMO_PASSWORD}")
        print(f"User ID:       {user.id}")
        print(f"Report ID:     {report.id}")
        print("=" * 55)

    finally:
        db.close()


if __name__ == "__main__":
    setup_database()
    setup_demo_data()