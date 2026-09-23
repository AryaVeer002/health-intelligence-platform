from datetime import date

from pydantic import BaseModel, Field


class HealthProfileCreate(BaseModel):
    age: int = Field(gt=0)
    weight: float = Field(gt=0)
    height: float = Field(gt=0)


class HealthProfileResponse(BaseModel):
    id: int
    user_id: int
    age: int
    weight: float
    height: float


class HealthRecord(BaseModel):
    record_date: date
    weight: float = Field(gt=0)
    height: float = Field(gt=0)
    heart_rate: int = Field(gt=0)