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


class RiskProfileCreate(BaseModel):
    sex: int = Field(ge=1, le=2)
    general_health: int = Field(ge=1, le=2)
    physical_health_days: int = Field(ge=0, le=30)
    physical_activity: int = Field(ge=1, le=2)
    smoking: int = Field(ge=1, le=2)
    alcohol: int = Field(ge=1, le=2)


class RiskProfileResponse(BaseModel):
    id: int
    user_id: int
    sex: int
    general_health: int
    physical_health_days: int
    physical_activity: int
    smoking: int
    alcohol: int
    