from datetime import date

from pydantic import BaseModel, Field


class TrendResponse(BaseModel):
    metric: str
    start_value: float
    end_value: float
    change: float
    direction: str


class AnomalyResponse(BaseModel):
    metric: str
    value: float
    expected_value: float
    severity: str
    detected_at: date


class RiskResponse(BaseModel):
    risk_type: str
    risk_score: float = Field(ge=0, le=1)
    risk_level: str
    contributing_factors: list[str]



class RiskAssessmentRequest(BaseModel):
    bmi: float = Field(gt=0)
    age_group: int = Field(ge=1, le=14)
    sex: int = Field(ge=1, le=2)
    general_health: int = Field(ge=1, le=2)
    physical_health_days: int = Field(ge=0, le=30)
    physical_activity: int = Field(ge=1, le=2)
    smoking: int = Field(ge=1, le=2)
    alcohol: int = Field(ge=1, le=2)