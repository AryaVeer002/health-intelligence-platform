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


class HealthRecordCreate(BaseModel):
    record_date: date
    weight: float = Field(gt=0)
    height: float = Field(gt=0)
    heart_rate: int = Field(gt=0)


class HealthRecordResponse(BaseModel):
    id: int
    user_id: int
    record_date: date
    weight: float
    height: float
    heart_rate: int