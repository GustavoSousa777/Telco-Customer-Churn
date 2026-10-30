"""Pipeline unico: recebe colunas brutas e devolve probabilidade de churn."""
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

from src.data.clean import clean
from src.features import CATEGORICAL, NUMERIC

SEED = 42

# Melhores hiperparametros do Optuna (XGBoost, 50 trials, PR-AUC em CV) no notebook.
BEST_PARAMS = {
    "n_estimators": 380,
    "learning_rate": 0.042391376805302236,
    "max_depth": 2,
    "min_child_weight": 10,
    "subsample": 0.6379679919943347,
    "colsample_bytree": 0.6914050302113515,
    "gamma": 3.7700194150442408,
    "reg_alpha": 6.452509986240249,
    "reg_lambda": 1.6347113042007797,
}


def novo_preprocessador() -> ColumnTransformer:
    return ColumnTransformer(
        [
            ("num", StandardScaler(), NUMERIC),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), CATEGORICAL),
        ],
        remainder="passthrough",
        verbose_feature_names_out=False,
    ).set_output(transform="pandas")


def build_pipeline(scale_pos_weight: float, params: dict | None = None) -> Pipeline:
    clf = XGBClassifier(
        scale_pos_weight=scale_pos_weight,
        eval_metric="logloss",
        random_state=SEED,
        n_jobs=-1,
        **(params or BEST_PARAMS),
    )
    return Pipeline(
        [
            ("clean", FunctionTransformer(clean)),
            ("prep", novo_preprocessador()),
            ("clf", clf),
        ]
    )
