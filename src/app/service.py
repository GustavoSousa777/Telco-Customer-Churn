"""Carrega o modelo uma vez e faz a predicao. Usado pela API e pela interface."""
import json
import os
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

from src.features import FEATURES


@lru_cache(maxsize=1)
def load_artifacts():
    model_dir = Path(os.getenv("MODEL_DIR", "model"))
    model = joblib.load(model_dir / "model.joblib")
    metadata = json.loads((model_dir / "metadata.json").read_text())
    return model, metadata


def predict(record: dict) -> dict:
    model, metadata = load_artifacts()
    X = pd.DataFrame([record])[FEATURES]
    proba = float(model.predict_proba(X)[0, 1])
    threshold = float(metadata["threshold"])
    return {
        "churn_probability": round(proba, 4),
        "churn_prediction": proba >= threshold,
        "threshold": round(threshold, 4),
    }
