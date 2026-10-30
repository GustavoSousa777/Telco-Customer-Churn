"""Limpeza aplicada no treino e na inferencia (mesmas regras da celula 31 do notebook)."""
import numpy as np
import pandas as pd

SERVICOS_INTERNET = [
    "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies",
]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Recebe colunas brutas e devolve colunas prontas para o ColumnTransformer.

    - TotalCharges vira numerico. Vazio com tenure == 0 vira 0 (regra do notebook).
      Vazio com tenure > 0 (so acontece na API) vira tenure * MonthlyCharges.
    - "No phone service" e "No internet service" viram "No".
    """
    df = df.copy()
    total = pd.to_numeric(df["TotalCharges"], errors="coerce")
    estimativa = np.where(df["tenure"] == 0, 0.0, df["tenure"] * df["MonthlyCharges"])
    df["TotalCharges"] = total.fillna(pd.Series(estimativa, index=df.index)).astype(float)

    df["MultipleLines"] = df["MultipleLines"].replace("No phone service", "No")
    df[SERVICOS_INTERNET] = df[SERVICOS_INTERNET].replace("No internet service", "No")
    return df
