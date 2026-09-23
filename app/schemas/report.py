from datetime import datetime

from pydantic import BaseModel, Field


class ReportMetadata(BaseModel):
    report_type: str = Field(min_length=2, max_length=100)
    report_date: datetime
    source: str | None = Field(default=None, max_length=200)


class ReportResponse(BaseModel):
    id: int
    filename: str
    report_type: str
    report_date: datetime
    uploaded_at: datetime
    status: str