import gradio as gr

from src.app.service import predict
from src.features import CATEGORIES


def _predict_ui(**kwargs):
    r = predict(kwargs)
    p = r["churn_probability"]
    veredito = "Risco alto de churn" if r["churn_prediction"] else "Risco baixo de churn"
    texto = f"**{veredito}**. Probabilidade {p:.1%} (corte do modelo: {r['threshold']:.1%})."
    return {"Churn": p, "Permanece": 1 - p}, texto


def build_ui() -> gr.Blocks:
    def dd(nome, padrao):
        return gr.Dropdown(list(CATEGORIES[nome]), value=padrao, label=nome)

    campos = [
        dd("gender", "Female"),
        gr.Radio([0, 1], value=0, label="SeniorCitizen"),
        dd("Partner", "No"),
        dd("Dependents", "No"),
        gr.Slider(0, 72, value=12, step=1, label="tenure (meses)"),
        dd("PhoneService", "Yes"),
        dd("MultipleLines", "No"),
        dd("InternetService", "Fiber optic"),
        dd("OnlineSecurity", "No"),
        dd("OnlineBackup", "No"),
        dd("DeviceProtection", "No"),
        dd("TechSupport", "No"),
        dd("StreamingTV", "No"),
        dd("StreamingMovies", "No"),
        dd("Contract", "Month-to-month"),
        dd("PaperlessBilling", "Yes"),
        dd("PaymentMethod", "Electronic check"),
        gr.Slider(18, 120, value=70, step=0.05, label="MonthlyCharges"),
        gr.Number(value=None, label="TotalCharges (opcional)"),
    ]
    nomes = [c.label.split(" ")[0] for c in campos]

    def fn(*valores):
        return _predict_ui(**dict(zip(nomes, valores)))

    with gr.Blocks(title="Telco Churn") as demo:
        gr.Markdown("# Previsão de churn de clientes (Telco)\nPreencha os dados do cliente e veja a probabilidade de cancelamento.")
        with gr.Row():
            with gr.Column():
                for c in campos:
                    c.render()
                btn = gr.Button("Prever", variant="primary")
            with gr.Column():
                saida_label = gr.Label(label="Probabilidade")
                saida_txt = gr.Markdown()
        btn.click(fn, inputs=campos, outputs=[saida_label, saida_txt])
    return demo
