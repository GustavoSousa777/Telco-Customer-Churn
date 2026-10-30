from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.features import CATEGORIES


def _lit(coluna: str):
    return Literal[CATEGORIES[coluna]]


class Customer(BaseModel):
    """Um cliente com as colunas brutas do dataset Telco."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "gender": "Female", "SeniorCitizen": 0, "Partner": "No", "Dependents": "No",
                "tenure": 2, "PhoneService": "Yes", "MultipleLines": "No",
                "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No",
                "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
                "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check", "MonthlyCharges": 80.5, "TotalCharges": 160.0,
            }
        }
    )

    gender: _lit("gender")
    SeniorCitizen: Literal[0, 1]
    Partner: _lit("Partner")
    Dependents: _lit("Dependents")
    tenure: int = Field(ge=0, le=120, description="Meses como cliente")
    PhoneService: _lit("PhoneService")
    MultipleLines: _lit("MultipleLines")
    InternetService: _lit("InternetService")
    OnlineSecurity: _lit("OnlineSecurity")
    OnlineBackup: _lit("OnlineBackup")
    DeviceProtection: _lit("DeviceProtection")
    TechSupport: _lit("TechSupport")
    StreamingTV: _lit("StreamingTV")
    StreamingMovies: _lit("StreamingMovies")
    Contract: _lit("Contract")
    PaperlessBilling: _lit("PaperlessBilling")
    PaymentMethod: _lit("PaymentMethod")
    MonthlyCharges: float = Field(ge=0, le=500)
    TotalCharges: Optional[float] = Field(
        default=None, ge=0, description="Se omitido, usa tenure * MonthlyCharges (0 quando tenure = 0)"
    )


class Prediction(BaseModel):
    churn_probability: float = Field(ge=0, le=1)
    churn_prediction: bool
    threshold: float
