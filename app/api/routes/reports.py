from datetime import datetime, timezone
from pathlib import Path
import hashlib

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
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
MAX_UPLOAD_SIZE = 10 * 1024 * 1024
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

def get_report_file_path(report: Report) -> Path:
    if report.file_hash:
        return UPLOAD_DIR / (
            f"{report.file_hash}{Path(report.filename).suffix.lower()}"
        )

    return UPLOAD_DIR / report.filename

@router.get("/test")
def reports_test():
    return {
        "message": "Reports API is working"
    }


@router.post("/users/{user_id}/upload")
async def upload_report(
    user_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this user's reports"
        )
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

    contents = await file.read()

    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum allowed size is 10 MB"
        )

    file_hash = hashlib.sha256(
        contents
    ).hexdigest()

    stored_filename = f"{file_hash}{Path(file.filename).suffix.lower()}"
    file_path = UPLOAD_DIR / stored_filename

    existing_report = db.execute(
        select(Report).where(
            Report.user_id == user_id,
            Report.file_hash == file_hash
        )
    ).scalar_one_or_none()

    if existing_report:
        raise HTTPException(
            status_code=409,
            detail="This report has already been uploaded"
        )

    file_path.write_bytes(contents)

    now = datetime.now(timezone.utc)

    report = Report(
        user_id=user_id,
        filename=safe_filename,
        file_hash=file_hash,
        report_type=extension.replace(
            ".",
            ""
        ).upper(),
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
    current_user: User = Depends(get_current_user),
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

    if report.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this report"
        )

    file_path = get_report_file_path(report)

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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # --------------------------------------------------
    # 1. Find report
    # --------------------------------------------------

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

    if report.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this report"
        )

    # --------------------------------------------------
    # 2. Extract report text
    # --------------------------------------------------

    file_path = get_report_file_path(report)

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

    # --------------------------------------------------
    # 3. Extract health data
    # --------------------------------------------------

    health_data = health_data_extractor.extract(
        text
    )

    # --------------------------------------------------
    # 4. Check whether this report was already analyzed
    # --------------------------------------------------

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

    # --------------------------------------------------
    # 5. Determine measurement date
    # --------------------------------------------------

    measured_at = report.report_date

    if "report_date" in health_data:
        measured_at = datetime.strptime(
            health_data["report_date"],
            "%Y-%m-%d"
        )

    # --------------------------------------------------
    # 6. Build extracted measurements
    # --------------------------------------------------

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

    # --------------------------------------------------
    # 7. Remove duplicate measurements
    # --------------------------------------------------

    new_measurements = []

    for measurement in measurements:

        duplicate_statement = select(
            HealthMeasurement
        ).where(
            HealthMeasurement.user_id == measurement.user_id,
            HealthMeasurement.metric == measurement.metric,
            HealthMeasurement.value == measurement.value
        )

        duplicate_result = db.execute(
            duplicate_statement
        )

        # Multiple matching measurements are possible.
        # We only need to know whether at least one exists.
        duplicate_measurement = (
            duplicate_result.scalars().first()
        )

        if duplicate_measurement is None:
            new_measurements.append(
                measurement
            )

    # --------------------------------------------------
    # 8. Save only new measurements
    # --------------------------------------------------

    if new_measurements:
        db.add_all(
            new_measurements
        )

    measurements_saved = len(
        new_measurements
    )

    # --------------------------------------------------
    # 9. Update report status
    # --------------------------------------------------

    report.status = "analyzed"

    db.commit()

    # --------------------------------------------------
    # 10. Response
    # --------------------------------------------------

    return {
        "report_id": report.id,
        "filename": report.filename,
        "status": report.status,
        "extracted_data": health_data,
        "measurements_saved": measurements_saved
    }
