"""Contrato de colunas do modelo. Reflete exatamente o notebook Churn_tuning.ipynb."""

TARGET = "Churn"
ID_COLUMN = "customerID"

NUMERIC = ["tenure", "MonthlyCharges", "TotalCharges"]

# SeniorCitizen e 0/1 e passa direto pelo ColumnTransformer (remainder='passthrough').
PASSTHROUGH = ["SeniorCitizen"]

# Valores aceitos de cada coluna categorica, como aparecem nos dados brutos.
# A limpeza (src/data/clean.py) colapsa "No phone service" e "No internet service" em "No".
_YES_NO = ("Yes", "No")
_INTERNET_SERVICE = ("Yes", "No", "No internet service")

CATEGORIES = {
    "gender": ("Female", "Male"),
    "Partner": _YES_NO,
    "Dependents": _YES_NO,
    "PhoneService": _YES_NO,
    "MultipleLines": ("Yes", "No", "No phone service"),
    "InternetService": ("DSL", "Fiber optic", "No"),
    "OnlineSecurity": _INTERNET_SERVICE,
    "OnlineBackup": _INTERNET_SERVICE,
    "DeviceProtection": _INTERNET_SERVICE,
    "TechSupport": _INTERNET_SERVICE,
    "StreamingTV": _INTERNET_SERVICE,
    "StreamingMovies": _INTERNET_SERVICE,
    "Contract": ("Month-to-month", "One year", "Two year"),
    "PaperlessBilling": _YES_NO,
    "PaymentMethod": (
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)",
    ),
}

CATEGORICAL = list(CATEGORIES)

# Ordem original das colunas de entrada no CSV (sem customerID e Churn).
FEATURES = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService",
    "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges",
]

assert set(FEATURES) == set(NUMERIC + PASSTHROUGH + CATEGORICAL)
