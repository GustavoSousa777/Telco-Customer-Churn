import gradio as gr

from src.app.assets import CRYSTALS_SVG, LOGO_SVG
from src.app.service import predict
from src.features import CATEGORIES

GITHUB_URL = "https://github.com/GustavoSousa777/Telco-Customer-Churn"

HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script>
const u = new URL(window.location.href);
if (u.searchParams.get('__theme') !== 'dark') {
  u.searchParams.set('__theme', 'dark');
  window.location.replace(u.toString());
}
</script>
"""

PRIMARY_GRADIENT = "linear-gradient(90deg, #FC0065 0%, #8B5CF6 100%)"
PRIMARY_GRADIENT_HOVER = "linear-gradient(90deg, #E00059 0%, #7C3AED 100%)"

THEME = gr.themes.Base(
    primary_hue=gr.themes.colors.pink,
    secondary_hue=gr.themes.colors.violet,
    neutral_hue=gr.themes.colors.slate,
    radius_size=gr.themes.sizes.radius_lg,
    font=["Sora", "Inter", "ui-sans-serif", "system-ui", "sans-serif"],
).set(
    body_background_fill="#0D1634",
    body_background_fill_dark="#0D1634",
    background_fill_primary="#0D1634",
    background_fill_primary_dark="#0D1634",
    background_fill_secondary="#142048",
    background_fill_secondary_dark="#142048",
    body_text_color="#FFFFFF",
    body_text_color_dark="#FFFFFF",
    body_text_color_subdued="#A9B4D6",
    body_text_color_subdued_dark="#A9B4D6",
    block_background_fill="transparent",
    block_background_fill_dark="transparent",
    block_border_width="0px",
    block_shadow="none",
    block_label_background_fill="transparent",
    block_label_background_fill_dark="transparent",
    block_label_text_color="#C9D2EE",
    block_label_text_color_dark="#C9D2EE",
    block_title_text_color="#C9D2EE",
    block_title_text_color_dark="#C9D2EE",
    block_label_text_weight="600",
    input_background_fill="#0D1634",
    input_background_fill_dark="#0D1634",
    input_background_fill_focus="#0D1634",
    input_background_fill_focus_dark="#0D1634",
    input_border_color="rgba(255,255,255,0.14)",
    input_border_color_dark="rgba(255,255,255,0.14)",
    input_border_color_focus="#FC0065",
    input_border_color_focus_dark="#FC0065",
    input_border_width="1px",
    input_shadow="none",
    border_color_primary="rgba(255,255,255,0.12)",
    border_color_primary_dark="rgba(255,255,255,0.12)",
    slider_color="#FC0065",
    slider_color_dark="#FC0065",
    checkbox_background_color_selected="#FC0065",
    checkbox_background_color_selected_dark="#FC0065",
    checkbox_border_color_selected="#FC0065",
    checkbox_border_color_selected_dark="#FC0065",
    button_primary_background_fill=PRIMARY_GRADIENT,
    button_primary_background_fill_dark=PRIMARY_GRADIENT,
    button_primary_background_fill_hover=PRIMARY_GRADIENT_HOVER,
    button_primary_background_fill_hover_dark=PRIMARY_GRADIENT_HOVER,
    button_primary_text_color="#FFFFFF",
    button_primary_text_color_dark="#FFFFFF",
    button_primary_border_color="transparent",
    button_primary_border_color_dark="transparent",
    button_secondary_background_fill="rgba(255,255,255,0.05)",
    button_secondary_background_fill_dark="rgba(255,255,255,0.05)",
    button_secondary_background_fill_hover="rgba(255,255,255,0.1)",
    button_secondary_background_fill_hover_dark="rgba(255,255,255,0.1)",
    button_secondary_border_color="rgba(255,255,255,0.2)",
    button_secondary_border_color_dark="rgba(255,255,255,0.2)",
    button_secondary_text_color="#FFFFFF",
    button_secondary_text_color_dark="#FFFFFF",
)

CSS = """
:root {
  --bg: #0D1634;
  --panel: #111C44;
  --line: rgba(255,255,255,.1);
  --text: #FFFFFF;
  --muted: #A9B4D6;
  --accent: #FC0065;
  --violet: #8B5CF6;
  --cyan: #22D3EE;
}
body, .gradio-container {
  background: var(--bg) !important;
  color: var(--text);
  font-family: 'Sora', 'Inter', system-ui, sans-serif !important;
}
.gradio-container {
  max-width: 1240px !important;
  margin: 0 auto !important;
  padding: 0 28px 40px !important;
}
.gradio-container .prose, .gradio-container label, .gradio-container input, .gradio-container button {
  font-family: 'Sora', 'Inter', system-ui, sans-serif !important;
}
#topbar { display: flex; align-items: center; justify-content: space-between; padding: 24px 0 0; gap: 16px; }
#topbar .logo svg { height: 62px; width: auto; display: block; }
#topbar nav { display: flex; gap: 10px; }
#topbar nav a {
  color: var(--text); text-decoration: none; font-size: 13px; font-weight: 600;
  padding: 9px 16px; border: 1px solid rgba(255,255,255,.2); border-radius: 999px; transition: border-color .2s, background .2s;
}
#topbar nav a:hover { border-color: var(--accent); background: rgba(252,0,101,.08); }
#intro { display: grid; grid-template-columns: 1.25fr 0.75fr; gap: 24px; align-items: center; padding: 36px 0 32px; }
#intro h1 { font-size: 36px; line-height: 1.15; font-weight: 800; letter-spacing: -.02em; color: var(--text); margin: 0 0 14px; }
#intro h1 span { background: linear-gradient(90deg, #FC0065, #8B5CF6 55%, #22D3EE); -webkit-background-clip: text; background-clip: text; color: transparent; }
#intro p { font-size: 16px; line-height: 1.65; color: var(--muted); max-width: 620px; margin: 0 0 18px; }
#intro ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }
#intro li { display: flex; align-items: center; gap: 12px; font-size: 14.5px; color: var(--text); }
#intro li::before {
  content: "\\2713"; flex: none; width: 22px; height: 22px; border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center;
  color: var(--accent); font-weight: 800; font-size: 13px; background: rgba(252,0,101,.14); border: 1px solid rgba(252,0,101,.45);
}
#intro .art svg { width: 100%; max-height: 270px; height: auto; display: block; }
.fl { animation: floaty 7s ease-in-out infinite; transform-box: fill-box; }
.fl-b { animation-duration: 9s; animation-delay: -2s; }
.fl-c { animation-duration: 8s; animation-delay: -4s; }
@keyframes floaty { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
@media (prefers-reduced-motion: reduce) { .fl { animation: none; } }
.panel, #result-wrap {
  background: var(--panel) !important; border: 1px solid var(--line) !important; border-radius: 20px !important;
  padding: 26px !important; gap: 16px !important;
}
.panel-head { align-items: center !important; flex-wrap: wrap !important; gap: 10px !important; margin-bottom: 4px !important; }
.panel-head .block, .panel .block, .panel .form { background: transparent !important; border: 0 !important; box-shadow: none !important; }
.panel-title h2 { margin: 0; font-size: 20px; font-weight: 700; color: var(--text); }
.panel-title p { margin: 4px 0 0; font-size: 13px; color: var(--muted); }
.panel-head button { border-radius: 999px !important; font-weight: 600 !important; font-size: 13px !important; flex: none !important; min-width: 0 !important; }
.group { display: flex; align-items: center; gap: 10px; font-size: 12px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); padding-top: 8px; }
.group::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--accent); }
.panel input, .panel .wrap-inner, .panel select { border-radius: 12px !important; color: var(--text) !important; }
.panel .options, .panel ul.options { background: #142048 !important; border: 1px solid var(--line) !important; }
.panel .options li { color: var(--text) !important; }
.panel .options li:hover, .panel .options li.active { background: rgba(252,0,101,.18) !important; }
.panel input[type=range] { accent-color: var(--accent); }
.panel input[type=radio] { accent-color: var(--accent); }
#result-col { position: sticky; top: 20px; align-self: flex-start; }
#result-wrap { gap: 18px !important; }
#result-card { text-align: center; padding: 8px 0 4px; }
#result-card .kicker { font-size: 12px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }
#result-card .ring { position: relative; width: 180px; height: 180px; margin: 20px auto 16px; }
#result-card .ring svg { width: 100%; height: 100%; transform: rotate(-90deg); }
#result-card .ring .pct {
  position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center;
  font-size: 36px; font-weight: 800; letter-spacing: -.02em; color: var(--text);
}
#result-card .ring .pct small { font-size: 12px; font-weight: 600; color: var(--muted); letter-spacing: 0; }
#result-card .badge { display: inline-block; font-size: 14px; font-weight: 700; padding: 9px 18px; border-radius: 999px; }
#result-card .badge.high { background: rgba(252,0,101,.16); color: #FF5C98; border: 1px solid rgba(252,0,101,.5); }
#result-card .badge.low { background: rgba(34,211,238,.12); color: #67E8F9; border: 1px solid rgba(34,211,238,.4); }
#result-card p.note { font-size: 13.5px; line-height: 1.6; color: var(--muted); margin: 16px 0 0; }
#result-card .empty-art { width: 130px; margin: 16px auto 4px; }
#result-card h4 { font-size: 17px; font-weight: 700; color: var(--text); margin: 12px 0 6px; }
#footer { margin-top: 28px; text-align: center; color: var(--muted); font-size: 12.5px; }
#footer a { color: var(--text); font-weight: 600; text-decoration: none; margin: 0 6px; }
@media (max-width: 900px) {
  #intro { grid-template-columns: 1fr; padding: 24px 0; }
  #intro h1 { font-size: 28px; }
  #intro .art { display: none; }
  #result-col { position: static; }
  #topbar .logo svg { height: 52px; }
}
"""

HEADER_HTML = f"""
<div id="topbar">
  <div class="logo">{LOGO_SVG}</div>
  <nav>
    <a href="/docs" target="_blank" rel="noopener">API</a>
    <a href="{GITHUB_URL}" target="_blank" rel="noopener">GitHub</a>
  </nav>
</div>
<section id="intro">
  <div>
    <h1>Descubra quais clientes <span>estão prestes a cancelar</span></h1>
    <p>O site usa um modelo de machine learning, treinado com dados reais de uma operadora de telecomunicações, para estimar a probabilidade de um cliente cancelar o serviço (churn). Preencha os dados abaixo e veja o risco na hora.</p>
    <ul>
      <li>Modelo XGBoost com ROC-AUC de 0,85 e recall de 80% no teste</li>
      <li>Resultado em tempo real, calculado por uma API na nuvem</li>
      <li>API REST documentada e pronta para integração</li>
    </ul>
  </div>
  <div class="art">{CRYSTALS_SVG}</div>
</section>
"""

FOOTER_HTML = f"""
<div id="footer">
  Projeto de ciência de dados de ponta a ponta: treino, API, testes, CI/CD, Docker e Azure Container Apps.
  <a href="/docs" target="_blank" rel="noopener">Documentação da API</a><a href="{GITHUB_URL}" target="_blank" rel="noopener">Código</a>
</div>
"""

EMPTY_HTML = """
<div id="result-card">
  <div class="kicker">Resultado</div>
  <svg class="empty-art" viewBox="0 0 150 130" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="ea" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#67E8F9"/><stop offset="1" stop-color="#7C3AED"/></linearGradient>
    </defs>
    <polygon points="75,6 135,65 75,124 15,65" fill="url(#ea)" fill-opacity="0.7" stroke="#fff" stroke-width="2"/>
    <polygon points="75,6 15,65 75,65" fill="#fff" fill-opacity="0.3"/>
    <polygon points="75,34 105,65 75,96 45,65" fill="none" stroke="#fff" stroke-opacity="0.9" stroke-width="1.5"/>
  </svg>
  <h4>Aguardando os dados</h4>
  <p class="note">Preencha o perfil do cliente e clique em Calcular risco para ver a probabilidade de cancelamento.</p>
</div>
"""


def formatar_pct(valor, casas=1):
    return f"{valor * 100:.{casas}f}".replace(".", ",") + "%"


def render_resultado(r):
    p = r["churn_probability"]
    corte = r["threshold"]
    alto = bool(r["churn_prediction"])
    circunferencia = 351.86
    tracado = circunferencia * p
    cor_ini, cor_fim = ("#FC0065", "#8B5CF6") if alto else ("#22D3EE", "#8B5CF6")
    classe = "high" if alto else "low"
    veredito = "Risco alto de churn" if alto else "Risco baixo de churn"
    if alto:
        nota = (
            f"A probabilidade está acima do corte do modelo ({formatar_pct(corte)}). "
            "Este cliente é um bom candidato a uma ação de retenção."
        )
    else:
        nota = (
            f"A probabilidade está abaixo do corte do modelo ({formatar_pct(corte)}). "
            "Não há sinal forte de cancelamento para este perfil."
        )
    return f"""
<div id="result-card">
  <div class="kicker">Probabilidade de cancelamento</div>
  <div class="ring">
    <svg viewBox="0 0 140 140">
      <defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{cor_ini}"/><stop offset="1" stop-color="{cor_fim}"/></linearGradient></defs>
      <circle cx="70" cy="70" r="56" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="14"/>
      <circle cx="70" cy="70" r="56" fill="none" stroke="url(#rg)" stroke-width="14" stroke-linecap="round" stroke-dasharray="{tracado:.2f} {circunferencia}"/>
    </svg>
    <div class="pct">{formatar_pct(p)}<small>chance de churn</small></div>
  </div>
  <span class="badge {classe}">{veredito}</span>
  <p class="note">{nota}</p>
</div>
"""


def _predict_ui(**kwargs):
    return render_resultado(predict(kwargs))


ROTULOS = {
    "Yes": "Sim",
    "No": "Não",
    "Female": "Feminino",
    "Male": "Masculino",
    "No phone service": "Sem serviço de telefone",
    "No internet service": "Sem internet",
    "DSL": "DSL",
    "Fiber optic": "Fibra óptica",
    "Month-to-month": "Mensal",
    "One year": "1 ano",
    "Two year": "2 anos",
    "Electronic check": "Cheque eletrônico",
    "Mailed check": "Cheque pelo correio",
    "Bank transfer (automatic)": "Transferência bancária (automática)",
    "Credit card (automatic)": "Cartão de crédito (automático)",
}

NOMES = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
    "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges",
]

EXEMPLO_RISCO_ALTO = [
    "Female", 0, "No", "No", 2,
    "Yes", "No", "Fiber optic", "No", "No",
    "No", "No", "No", "No",
    "Month-to-month", "Yes", "Electronic check", 85.0, None,
]

EXEMPLO_RISCO_BAIXO = [
    "Male", 0, "Yes", "Yes", 60,
    "Yes", "Yes", "DSL", "Yes", "Yes",
    "Yes", "Yes", "No", "No",
    "Two year", "No", "Credit card (automatic)", 62.0, None,
]


def build_ui() -> gr.Blocks:
    def dd(nome, rotulo, padrao):
        escolhas = [(ROTULOS.get(v, v), v) for v in CATEGORIES[nome]]
        return gr.Dropdown(escolhas, value=padrao, label=rotulo, elem_id=f"f-{nome}")

    with gr.Blocks(title="Gustavo Sousa | Previsão de churn de clientes") as demo:
        gr.HTML(HEADER_HTML)

        with gr.Row(equal_height=False):
            with gr.Column(scale=8, elem_classes="panel"):
                with gr.Row(elem_classes="panel-head"):
                    gr.HTML(
                        '<div class="panel-title"><h2>Dados do cliente</h2>'
                        "<p>Preencha os campos ou carregue um exemplo pronto.</p></div>"
                    )
                    btn_alto = gr.Button("Exemplo: risco alto", size="sm", scale=0)
                    btn_baixo = gr.Button("Exemplo: risco baixo", size="sm", scale=0)

                with gr.Row():
                    with gr.Column():
                        gr.HTML('<div class="group">Perfil</div>')
                        gender = dd("gender", "Gênero", "Female")
                        senior = gr.Radio([("Não", 0), ("Sim", 1)], value=0, label="Idoso (65 anos ou mais)")
                        partner = dd("Partner", "Possui parceiro(a)", "No")
                        dependents = dd("Dependents", "Possui dependentes", "No")
                        tenure = gr.Slider(0, 72, value=12, step=1, label="Tempo como cliente (meses)")
                    with gr.Column():
                        gr.HTML('<div class="group">Serviços</div>')
                        phone = dd("PhoneService", "Serviço de telefone", "Yes")
                        lines = dd("MultipleLines", "Múltiplas linhas", "No")
                        internet = dd("InternetService", "Tipo de internet", "Fiber optic")
                        security = dd("OnlineSecurity", "Segurança online", "No")
                        backup = dd("OnlineBackup", "Backup online", "No")
                    with gr.Column():
                        gr.HTML('<div class="group">Adicionais</div>')
                        protection = dd("DeviceProtection", "Proteção de dispositivo", "No")
                        support = dd("TechSupport", "Suporte técnico", "No")
                        tv = dd("StreamingTV", "Streaming de TV", "No")
                        movies = dd("StreamingMovies", "Streaming de filmes", "No")

                gr.HTML('<div class="group">Contrato e cobrança</div>')
                with gr.Row():
                    contract = dd("Contract", "Tipo de contrato", "Month-to-month")
                    paperless = dd("PaperlessBilling", "Fatura digital", "Yes")
                    payment = dd("PaymentMethod", "Forma de pagamento", "Electronic check")
                with gr.Row():
                    monthly = gr.Slider(18, 120, value=70, step=0.05, label="Mensalidade (US$)")
                    total = gr.Number(value=None, label="Total já pago (US$, opcional)")

            with gr.Column(scale=3, elem_id="result-col"):
                with gr.Column(elem_id="result-wrap"):
                    resultado = gr.HTML(EMPTY_HTML)
                    btn = gr.Button("Calcular risco de churn", variant="primary", size="lg")

        gr.HTML(FOOTER_HTML)

        campos = [
            gender, senior, partner, dependents, tenure,
            phone, lines, internet, security, backup,
            protection, support, tv, movies,
            contract, paperless, payment, monthly, total,
        ]

        def fn(*valores):
            return _predict_ui(**dict(zip(NOMES, valores)))

        btn.click(fn, inputs=campos, outputs=resultado)
        btn_alto.click(lambda: EXEMPLO_RISCO_ALTO, outputs=campos)
        btn_baixo.click(lambda: EXEMPLO_RISCO_BAIXO, outputs=campos)
    return demo
