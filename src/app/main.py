import json
import logging
import time

import gradio as gr
from fastapi import FastAPI

from src.app.schemas import Customer, Prediction
from src.app.service import load_artifacts, predict
from src.app.ui import CSS, HEAD, THEME, build_ui

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("churn-api")

app = FastAPI(title="Telco Churn API", version="1.0.0")


@app.get("/")
def root():
    _, meta = load_artifacts()
    return {"service": "telco-churn", "docs": "/docs", "ui": "/ui", "model": meta["model"]}


@app.get("/health")
def health():
    load_artifacts()
    return {"status": "ok"}


@app.post("/predict", response_model=Prediction)
def predict_endpoint(customer: Customer):
    t0 = time.perf_counter()
    result = predict(customer.model_dump())
    # Log resumido em JSON: sem identificadores nem dados pessoais completos.
    log.info(json.dumps({
        "event": "prediction",
        "contract": customer.Contract,
        "tenure": customer.tenure,
        "probability": result["churn_probability"],
        "prediction": result["churn_prediction"],
        "latency_ms": round((time.perf_counter() - t0) * 1000, 2),
    }))
    return result


app = gr.mount_gradio_app(app, build_ui(), path="/ui", theme=THEME, css=CSS, head=HEAD, footer_links=[])
