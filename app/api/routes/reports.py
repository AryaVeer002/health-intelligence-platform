from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.report import Report
from app.models.user import User
from app.models.health_measurement import HealthMeasurement
from app.services.report_extractor import report_extractor
from app.services.health_data_extractor import (
    health_data_extractor
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


UPLOAD_DIR = Path("data/reports")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.get("/test")
def reports_test():
    return {
        "message": "Reports API is working"
    }


@router.post("/users/{user_id}/upload")
async def upload_report(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user_statement = select(User).where(
        User.id == user_id
    )

    user_result = db.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    allowed_extensions = {
        ".pdf",
        ".txt",
        ".csv"
    }

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    safe_filename = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_filename

    contents = await file.read()

    file_path.write_bytes(contents)

    now = datetime.now(timezone.utc)

    report = Report(
        user_id=user_id,
        filename=safe_filename,
        report_type=extension.replace(".", "").upper(),
        report_date=now,
        uploaded_at=now,
        status="uploaded"
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "message": "Report uploaded successfully",
        "report_id": report.id,
        "filename": report.filename,
        "report_type": report.report_type,
        "status": report.status
    }


@router.post("/{report_id}/extract")
def extract_report_text(
    report_id: int,
    db: Session = Depends(get_db)
):
    statement = select(Report).where(
        Report.id == report_id
    )

    result = db.execute(statement)
    report = result.scalar_one_or_none()

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    file_path = UPLOAD_DIR / report.filename

    try:
        text = report_extractor.extract_text(
            file_path
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Report file not found"
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    report.status = "processed"

    db.commit()

    return {
        "report_id": report.id,
        "filename": report.filename,
        "status": report.status,
        "text": text
    }


@router.post("/{report_id}/analyze")
def analyze_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    statement = select(Report).where(
        Report.id == report_id
    )

    result = db.execute(statement)
    report = result.scalar_one_or_none()

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    file_path = UPLOAD_DIR / report.filename

    try:
        text = report_extractor.extract_text(
            file_path
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Report file not found"
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    health_data = health_data_extractor.extract(
        text
    )

    existing_statement = select(
        HealthMeasurement
    ).where(
        HealthMeasurement.report_id == report.id
    )

    existing_result = db.execute(
        existing_statement
    )

    existing_measurements = (
        existing_result.scalars().all()
    )

    if existing_measurements:
        return {
            "report_id": report.id,
            "filename": report.filename,
            "status": report.status,
            "extracted_data": health_data,
            "measurements_saved": 0,
            "message": "Report has already been analyzed"
        }

    measured_at = report.report_date

    if "report_date" in health_data:
        measured_at = datetime.strptime(
            health_data["report_date"],
            "%Y-%m-%d"
        )

    measurements = []

    if "bmi" in health_data:
        measurements.append(
            HealthMeasurement(
                user_id=report.user_id,
                report_id=report.id,
                metric="BMI",
                value=health_data["bmi"],
                unit="kg/m²",
                measured_at=measured_at
            )
        )

    if "heart_rate" in health_data:
        measurements.append(
            HealthMeasurement(
                user_id=report.user_id,
                report_id=report.id,
                metric="Heart Rate",
                value=health_data["heart_rate"],
                unit="bpm",
                measured_at=measured_at
            )
        )

    blood_pressure = health_data.get(
        "blood_pressure"
    )

    if blood_pressure:
        if "systolic" in blood_pressure:
            measurements.append(
                HealthMeasurement(
                    user_id=report.user_id,
                    report_id=report.id,
                    metric="Blood Pressure - Systolic",
                    value=blood_pressure["systolic"],
                    unit="mmHg",
                    measured_at=measured_at
                )
            )

        if "diastolic" in blood_pressure:
            measurements.append(
                HealthMeasurement(
                    user_id=report.user_id,
                    report_id=report.id,
                    metric="Blood Pressure - Diastolic",
                    value=blood_pressure["diastolic"],
                    unit="mmHg",
                    measured_at=measured_at
                )
            )

    if measurements:
        db.add_all(measurements)

    report.status = "analyzed"

    db.commit()

    return {
        "report_id": report.id,
        "filename": report.filename,
        "status": report.status,
        "extracted_data": health_data,
        "measurements_saved": len(measurements)
    }