# Telco Customer Churn: modelo em produção

Previsão de cancelamento de clientes de telecom, do notebook ao serviço no ar: validação de dados, pipeline único, tracking com MLflow, API FastAPI, interface Gradio e container Docker, com o modelo publicado no Hugging Face Hub.

- **Demo (app no ar):** `COLE_AQUI_A_URL_DO_APP`
- **Modelo no Hugging Face Hub:** https://huggingface.co/GustavoSousa/telco-churn-xgboost
- **Vídeo:** `COLE_AQUI_O_LINK_DO_VIDEO`

## Problema de negócio

Perder um cliente custa mais do que fazer uma oferta de retenção para quem ia ficar. Por isso o modelo é calibrado para **capturar cerca de 80% dos clientes que vão cancelar**, aceitando que parte dos alertas serão falsos positivos.

## Fluxo

```mermaid
flowchart LR
    A[CSV bruto] --> B[validate.py]
    B --> C[train.py]
    C --> D[(model.joblib + metadata.json)]
    C --> E[MLflow]
    D --> F[FastAPI /predict]
    F --> G[Gradio /ui]
    D --> I[Hugging Face Hub]
    H[GitHub Actions] -->|pytest| F
    F --> J[Container Docker no host]
```

## Modelo

XGBoost com hiperparâmetros otimizados via Optuna (50 trials, PR-AUC em validação cruzada). O pipeline salvo recebe as **colunas brutas** e faz sozinho a limpeza, o one-hot, a padronização e a predição, então treino e inferência não divergem.

**Resultados no conjunto de teste (1.409 clientes), no corte de decisão escolhido:**

| Métrica | Valor |
|---|---|
| Recall (churn) | 0,799 |
| Precisão (churn) | 0,513 |
| ROC-AUC | 0,848 |
| PR-AUC | 0,661 |

**Por que XGBoost.** Na validação cruzada aninhada, o XGBoost teve o melhor PR-AUC (0,672 ± 0,018), à frente de Random Forest (0,666) e Regressão Logística (0,661). A diferença para os outros dois fica dentro do ruído (os intervalos do bootstrap no teste contêm zero). O XGBoost foi mantido por ter as melhores médias em ROC-AUC e PR-AUC, e a Regressão Logística continua uma alternativa mais simples de explicar.

**Por que esse corte.** O corte (0,512) é o maior valor cujo recall out-of-fold no treino ainda atinge 0,80. Ele é calculado no treino e salvo em `model/metadata.json`, e a API lê esse arquivo. O corte nunca foi ajustado olhando o conjunto de teste.

## Como rodar localmente

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

python -m src.train          # treina, salva em model/ e registra no MLflow
mlflow ui --backend-store-uri sqlite:///mlflow.db    # http://localhost:5000
python -m pytest -q
uvicorn src.app.main:app --port 7860                 # /docs e /ui
```

Docker:

```bash
docker build -t telco-churn .
docker run --rm -p 7860:7860 telco-churn
```

Publicar o modelo no Hugging Face Hub (precisa de um token de escrita na variável `HF_TOKEN`):

```bash
python -m src.publish_model --repo-id GustavoSousa/telco-churn-xgboost --github-url https://github.com/GustavoSousa777/Telco-Customer-Churn
```

## API

```bash
curl -X POST localhost:7860/predict -H "Content-Type: application/json" -d '{
  "gender": "Female", "SeniorCitizen": 0, "Partner": "No", "Dependents": "No",
  "tenure": 2, "PhoneService": "Yes", "MultipleLines": "No",
  "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No",
  "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
  "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check", "MonthlyCharges": 80.5
}'
```

Resposta: `{"churn_probability": 0.864, "churn_prediction": true, "threshold": 0.5119}`. `TotalCharges` é opcional (se omitido, usa `tenure * MonthlyCharges`).

## Estrutura

```
src/features.py        contrato de colunas e valores aceitos
src/data/validate.py   validação do CSV bruto
src/data/clean.py      limpeza usada no treino e na API
src/pipeline.py        Pipeline único (limpeza, pré-processamento, XGBoost)
src/train.py           treino, corte, métricas e MLflow
src/app/               API FastAPI e interface Gradio
tests/                 dados, modelo e API
src/publish_model.py   publica o modelo e o model card no Hugging Face Hub
model/                 model.joblib e metadata.json (versionados)
notebooks/             análise e tuning originais
```

## Monitoramento

Cada predição gera uma linha JSON nos logs do host (contrato, tenure, probabilidade, decisão, latência), sem dados pessoais completos. Para detectar drift, o plano é comparar periodicamente a distribuição das entradas em produção (tenure, MonthlyCharges, contrato, tipo de internet) com a do treino, e a taxa de alertas com a taxa esperada. Se divergirem de forma persistente, retreinar com dados novos. Hoje o monitoramento é por logs, e relatórios automáticos (por exemplo com Evidently) são o próximo passo.

## Limitações

O dataset é público e de um único período, então o modelo não captura sazonalidade nem mudanças de preço. A precisão de 51% significa que quase metade dos alertas é falso positivo, o que só compensa se a ação de retenção for barata.
