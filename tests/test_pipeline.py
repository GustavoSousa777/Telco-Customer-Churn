import json
from pathlib import Path

import joblib
import pandas as pd
import pytest
from fastapi.testclient import TestClient

from src.app.main import app
from src.data.clean import clean
from src.data.validate import validate
from src.features import FEATURES

CSV = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
client = TestClient(app)

BASE = {
    "gender": "Female", "SeniorCitizen": 0, "Partner": "No", "Dependents": "No",
    "tenure": 2, "PhoneService": "Yes", "MultipleLines": "No", "InternetService": "Fiber optic",
    "OnlineSecurity": "No", "OnlineBackup": "No", "DeviceProtection": "No", "TechSupport": "No",
    "StreamingTV": "No", "StreamingMovies": "No", "Contract": "Month-to-month",
    "PaperlessBilling": "Yes", "PaymentMethod": "Electronic check", "MonthlyCharges": 80.5,
}
SAFE = {**BASE, "Contract": "Two year", "tenure": 60, "InternetService": "DSL", "TotalCharges": 3000.0}


# ---------- dados ----------
def test_validate_accepts_raw_csv():
    validate(pd.read_csv(CSV))


def test_validate_rejects_bad_contract():
    df = pd.read_csv(CSV)
    df.loc[0, "Contract"] = "Weekly"
    with pytest.raises(ValueError, match="Contract"):
        validate(df)


def test_clean_rules():
    df = pd.DataFrame([{**BASE, "tenure": 0, "TotalCharges": " ", "MultipleLines": "No phone service",
                        "OnlineSecurity": "No internet service"}])
    out = clean(df)
    assert out.loc[0, "TotalCharges"] == 0.0
    assert out.loc[0, "MultipleLines"] == "No"
    assert out.loc[0, "OnlineSecurity"] == "No"


# ---------- modelo ----------
def test_model_accepts_raw_columns():
    model = joblib.load("model/model.joblib")
    X = pd.read_csv(CSV)[FEATURES].head(5)  # TotalCharges ainda como texto, como na API
    proba = model.predict_proba(X)[:, 1]
    assert ((proba >= 0) & (proba <= 1)).all()


def test_metadata_has_threshold():
    meta = json.loads(Path("model/metadata.json").read_text())
    assert 0 < meta["threshold"] < 1


def test_sanity_risk_ordering():
    risky = client.post("/predict", json=BASE).json()["churn_probability"]
    safe = client.post("/predict", json=SAFE).json()["churn_probability"]
    assert risky > safe


# ---------- API ----------
def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_predict_ok_without_total_charges():
    r = client.post("/predict", json=BASE)
    assert r.status_code == 200
    body = r.json()
    assert 0 <= body["churn_probability"] <= 1
    assert body["churn_prediction"] == (body["churn_probability"] >= body["threshold"])


def test_predict_rejects_invalid_input():
    assert client.post("/predict", json={**BASE, "Contract": "Weekly"}).status_code == 422
    assert client.post("/predict", json={**BASE, "tenure": -1}).status_code == 422


def test_ui_and_docs_available():
    assert client.get("/docs").status_code == 200
    assert client.get("/ui/").status_code == 200
