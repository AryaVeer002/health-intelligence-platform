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