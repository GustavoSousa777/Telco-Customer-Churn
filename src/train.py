"""Treino reproduzindo o notebook: mesma divisao, mesmo modelo, mesma regra de corte.

Uso: python -m src.train [--csv caminho] [--no-mlflow]
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
import xgboost
from sklearn.metrics import (
    average_precision_score, precision_recall_curve, precision_score,
    recall_score, roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split

from src.data.validate import validate
from src.features import FEATURES, ID_COLUMN, TARGET
from src.pipeline import BEST_PARAMS, SEED, build_pipeline

RECALL_ALVO = 0.80
MODEL_DIR = Path("model")
DEFAULT_CSV = "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"


def escolher_corte(modelo, X, y, cv, recall_alvo=RECALL_ALVO):
    """Maior corte cujo recall out-of-fold no treino ainda atinge o alvo (mesma regra do notebook)."""
    proba_oof = cross_val_predict(modelo, X, y, cv=cv, method="predict_proba")[:, 1]
    prec, rec, thr = precision_recall_curve(y, proba_oof)
    validos = np.where(rec[:-1] >= recall_alvo)[0]
    i = validos[-1]
    return float(thr[i]), float(rec[i]), float(prec[i])


def main(csv: str = DEFAULT_CSV, use_mlflow: bool = True) -> dict:
    df = validate(pd.read_csv(csv))
    x = df[FEATURES]
    y = df[TARGET].map({"No": 0, "Yes": 1})

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, stratify=y, random_state=SEED
    )
    peso_pos = float((y_train == 0).sum() / (y_train == 1).sum())
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

    corte, recall_oof, precisao_oof = escolher_corte(build_pipeline(peso_pos), x_train, y_train, cv)

    pipeline = build_pipeline(peso_pos).fit(x_train, y_train)
    proba = pipeline.predict_proba(x_test)[:, 1]
    pred = (proba >= corte).astype(int)
    metricas = {
        "roc_auc": float(roc_auc_score(y_test, proba)),
        "pr_auc": float(average_precision_score(y_test, proba)),
        "recall": float(recall_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred)),
    }

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_DIR / "model.joblib")
    metadata = {
        "model": "XGBoost (Optuna)",
        "threshold": corte,
        "threshold_rule": f"maior corte com recall OOF >= {RECALL_ALVO} no treino",
        "threshold_oof": {"recall": recall_oof, "precision": precisao_oof},
        "test_metrics_at_threshold": metricas,
        "params": {**BEST_PARAMS, "scale_pos_weight": peso_pos},
        "n_train": int(len(x_train)),
        "n_test": int(len(x_test)),
        "features": FEATURES,
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "versions": {"scikit-learn": sklearn.__version__, "xgboost": xgboost.__version__, "pandas": pd.__version__},
    }
    (MODEL_DIR / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

    if use_mlflow:
        import mlflow

        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        mlflow.set_experiment("telco-churn")
        with mlflow.start_run(run_name="xgboost-optuna"):
            mlflow.log_params(metadata["params"])
            mlflow.log_param("threshold", corte)
            mlflow.log_metrics({**metricas, "recall_oof_train": recall_oof, "precision_oof_train": precisao_oof})
            mlflow.log_artifact(str(MODEL_DIR / "metadata.json"))
            mlflow.sklearn.log_model(pipeline, name="model", serialization_format="cloudpickle")

    print(json.dumps({"threshold": round(corte, 3), **{k: round(v, 3) for k, v in metricas.items()}}, indent=2))
    return metadata


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=DEFAULT_CSV)
    ap.add_argument("--no-mlflow", action="store_true")
    a = ap.parse_args()
    main(a.csv, use_mlflow=not a.no_mlflow)
