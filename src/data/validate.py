"""Contrato de dados do CSV bruto. Falha com a lista de todas as regras quebradas."""
import pandas as pd

from src.features import CATEGORIES, FEATURES, ID_COLUMN, TARGET


def validate(df: pd.DataFrame) -> pd.DataFrame:
    erros = []

    faltando = [c for c in FEATURES + [ID_COLUMN, TARGET] if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas ausentes: {faltando}")

    if df[ID_COLUMN].duplicated().any():
        erros.append(f"{ID_COLUMN} duplicado em {int(df[ID_COLUMN].duplicated().sum())} linhas")

    for col, validos in CATEGORIES.items():
        invalidos = sorted(set(df[col].dropna().unique()) - set(validos))
        if invalidos or df[col].isna().any():
            erros.append(f"{col}: valores fora do contrato {invalidos} ou nulos")

    if set(df[TARGET].dropna().unique()) - {"Yes", "No"} or df[TARGET].isna().any():
        erros.append(f"{TARGET} deve ser Yes ou No, sem nulos")

    if set(df["SeniorCitizen"].dropna().unique()) - {0, 1}:
        erros.append("SeniorCitizen deve ser 0 ou 1")

    tenure = pd.to_numeric(df["tenure"], errors="coerce")
    if tenure.isna().any() or not tenure.between(0, 120).all():
        erros.append("tenure deve estar entre 0 e 120 meses")

    mensal = pd.to_numeric(df["MonthlyCharges"], errors="coerce")
    if mensal.isna().any() or not mensal.between(0, 500).all():
        erros.append("MonthlyCharges deve estar entre 0 e 500")

    total = pd.to_numeric(df["TotalCharges"], errors="coerce")
    if (total.isna() & (tenure != 0)).any():
        erros.append("TotalCharges vazio so e aceito quando tenure == 0")
    if (total < 0).any():
        erros.append("TotalCharges negativo")

    if erros:
        raise ValueError("Falha na validacao dos dados:\n- " + "\n- ".join(erros))
    return df
