"""Publica o modelo no Hugging Face Hub (repositorio de modelo, gratuito).

Uso:
    export HF_TOKEN=...        # Windows PowerShell: $env:HF_TOKEN="..."
    python -m src.publish_model --repo-id SEU_USUARIO/telco-churn-xgboost
    python -m src.publish_model --repo-id SEU_USUARIO/telco-churn-xgboost --dry-run
"""
import argparse
import json
import os
from pathlib import Path

MODEL_DIR = Path("model")


def build_model_card(meta: dict, github_url: str | None = None) -> str:
    m = meta["test_metrics_at_threshold"]
    v = meta["versions"]
    repo_line = f"- Código, API e interface: {github_url}\n" if github_url else ""
    return f"""---
library_name: scikit-learn
pipeline_tag: tabular-classification
tags:
  - tabular-classification
  - churn
  - xgboost
  - scikit-learn
language: pt
---

# Telco Customer Churn (XGBoost)

Modelo de previsão de cancelamento (churn) de clientes de telecom, treinado no dataset público Telco Customer Churn. O arquivo `model.joblib` é um `sklearn.Pipeline` único: recebe as colunas brutas e faz limpeza, one-hot, padronização e predição.

{repo_line}
## Uso pretendido

Priorizar clientes para ações de retenção. O corte de decisão foi escolhido para capturar cerca de 80% dos clientes que cancelam, aceitando falsos positivos.

## Resultados no conjunto de teste ({meta["n_test"]} clientes)

| Métrica | Valor |
|---|---|
| Corte de decisão | {meta["threshold"]:.3f} |
| Recall (churn) | {m["recall"]:.3f} |
| Precisão (churn) | {m["precision"]:.3f} |
| ROC-AUC | {m["roc_auc"]:.3f} |
| PR-AUC | {m["pr_auc"]:.3f} |

O corte é o maior valor cujo recall out-of-fold no treino ainda atinge 0,80, e foi definido sem olhar o conjunto de teste.

## Como carregar

O pipeline referencia a função de limpeza `src.data.clean.clean`, então é preciso ter o código do repositório no `PYTHONPATH` (clone o repositório acima e rode a partir da raiz dele).

```python
import joblib, json
import pandas as pd
from huggingface_hub import hf_hub_download

model = joblib.load(hf_hub_download("REPO_ID", "model.joblib"))
meta = json.load(open(hf_hub_download("REPO_ID", "metadata.json")))

cliente = pd.DataFrame([{{...}}])  # colunas brutas do dataset Telco, sem customerID e Churn
proba = model.predict_proba(cliente)[0, 1]
churn = proba >= meta["threshold"]
```

Versões usadas no treino (o arquivo depende delas): scikit-learn {v["scikit-learn"]}, xgboost {v["xgboost"]}, pandas {v["pandas"]}.

## Limitações

Dataset público de um único período, sem sazonalidade nem mudanças de preço. A precisão de {m["precision"]:.0%} significa que quase metade dos alertas é falso positivo. Não use para decisões automáticas sobre clientes sem revisão humana.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-id", required=True, help="usuario/nome-do-repo")
    ap.add_argument("--github-url", default=None)
    ap.add_argument("--private", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="so mostra o model card, nao envia nada")
    a = ap.parse_args()

    meta = json.loads((MODEL_DIR / "metadata.json").read_text())
    card = build_model_card(meta, a.github_url).replace("REPO_ID", a.repo_id)

    if a.dry_run:
        print(card)
        return

    token = os.getenv("HF_TOKEN")
    if not token:
        raise SystemExit("Defina a variavel de ambiente HF_TOKEN com um token de escrita do Hugging Face.")

    from huggingface_hub import HfApi

    api = HfApi(token=token)
    api.create_repo(repo_id=a.repo_id, repo_type="model", private=a.private, exist_ok=True)
    for nome in ("model.joblib", "metadata.json"):
        api.upload_file(path_or_fileobj=str(MODEL_DIR / nome), path_in_repo=nome, repo_id=a.repo_id, repo_type="model")
    api.upload_file(path_or_fileobj=card.encode("utf-8"), path_in_repo="README.md", repo_id=a.repo_id, repo_type="model")
    print(f"Modelo publicado: https://huggingface.co/{a.repo_id}")


if __name__ == "__main__":
    main()
