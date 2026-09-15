import base64
import copy
import html
from urllib.parse import urlparse

import streamlit as st

st.set_page_config(
    page_title="SETTA HUB | Central de Aplicativos",
    page_icon="🟨",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_CONFIG = {
    "logo_top": "",
    "logo_footer": "",
    "hero_image": "https://gruposetta.com.br/wp-content/uploads/2026/03/entradaG9.jpg-2-1-scaled-e1774901671839.png",
    "titulo": "CENTRAL DE APLICATIVOS",
    "subtitulo": "Acesso rápido aos sistemas operacionais",
    "descricao": "Soluções integradas que impulsionam a eficiência,\nconectam pessoas e constroem grandes resultados.",
    "slogan": "TECNOLOGIA\nQUE CONSTRÓI\nO AMANHÃ",
    "usuario": "Olá, Usuário",
    "rodape_esquerdo": "TECNOLOGIA A SERVIÇO DE GRANDES RESULTADOS",
    "rodape_direito": "JUNTOS, CONSTRUÍMOS O AMANHÃ",
    "apps": [
        {"nome": "Gestão Almoxarifado", "descricao": "Gestão completa da operação", "icone": "📦", "status": "Online", "url": "#"},
        {"nome": "Dashboard Operacional", "descricao": "Indicadores e resultados", "icone": "📊", "status": "Online", "url": "#"},
        {"nome": "MRP", "descricao": "Demanda e necessidade de materiais", "icone": "📋", "status": "Ativo", "url": "#"},
        {"nome": "Entregas", "descricao": "Controle de OPs e cronograma", "icone": "🚚", "status": "Online", "url": "#"},
        {"nome": "Compra Fácil", "descricao": "Compras e histórico de preços", "icone": "🛒", "status": "Ativo", "url": "#"},
        {"nome": "Gestão de Equipe", "descricao": "Colaboradores e plano de carreira", "icone": "👥", "status": "Online", "url": "#"},
    ],
}

if "hub_config" not in st.session_state:
    st.session_state.hub_config = copy.deepcopy(DEFAULT_CONFIG)
if "upload_version" not in st.session_state:
    st.session_state.upload_version = 0


def upload_to_data_uri(uploaded_file):
    if uploaded_file is None:
        return ""
    mime = uploaded_file.type or "image/png"
    encoded = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def safe_url(value):
    value = (value or "").strip()
    if not value or value == "#":
        return "#"
    parsed = urlparse(value)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return value
    return "#"


def esc(value):
    return html.escape(str(value or ""), quote=True)


cfg = st.session_state.hub_config
uv = st.session_state.upload_version

# ============================================================
# MENU LATERAL DE CONFIGURAÇÕES
# ============================================================
with st.sidebar:
    st.title("⚙️ Configurações")
    st.caption("Personalize o SETTA HUB sem alterar as dimensões do layout.")

    with st.form("hub_settings_form"):
        st.subheader("Identidade visual")

        logo_top_file = st.file_uploader(
            "Logo superior",
            type=["png", "jpg", "jpeg", "webp"],
            key=f"logo_top_{uv}",
            help="A nova imagem será ajustada automaticamente ao mesmo espaço da logo atual.",
        )
        logo_footer_file = st.file_uploader(
            "Logo inferior",
            type=["png", "jpg", "jpeg", "webp"],
            key=f"logo_footer_{uv}",
            help="A nova imagem será ajustada automaticamente ao mesmo espaço da logo atual.",
        )
        hero_file = st.file_uploader(
            "Imagem principal",
            type=["png", "jpg", "jpeg", "webp"],
            key=f"hero_{uv}",
            help="A nova imagem ocupará exatamente a mesma área da imagem principal atual.",
        )

        clear_logo_top = st.checkbox("Usar logo superior padrão")
        clear_logo_footer = st.checkbox("Usar logo inferior padrão")
        restore_hero = st.checkbox("Usar imagem principal padrão")

        st.divider()
        st.subheader("Textos da página")
        titulo = st.text_input("Título", value=cfg["titulo"])
        subtitulo = st.text_input("Subtítulo", value=cfg["subtitulo"])
        descricao = st.text_area("Descrição", value=cfg["descricao"], height=90)
        slogan = st.text_area("Texto sobre a imagem", value=cfg["slogan"], height=90)
        usuario = st.text_input("Usuário do cabeçalho", value=cfg["usuario"])
        rodape_esquerdo = st.text_input("Texto inferior esquerdo", value=cfg["rodape_esquerdo"])
        rodape_direito = st.text_input("Texto inferior direito", value=cfg["rodape_direito"])

        st.divider()
        st.subheader("Cartões e redirecionamentos")
        edited_apps = []

        for i, app in enumerate(cfg["apps"], start=1):
            with st.expander(f"{i}. {app['nome']}"):
                nome = st.text_input("Nome do cartão", value=app["nome"], key=f"nome_{i}_{uv}")
                descricao_app = st.text_input("Descrição", value=app["descricao"], key=f"desc_{i}_{uv}")
                icone = st.text_input("Ícone", value=app["icone"], key=f"icon_{i}_{uv}")
                status = st.text_input("Status", value=app["status"], key=f"status_{i}_{uv}")
                url = st.text_input(
                    "Link de destino",
                    value=app["url"],
                    key=f"url_{i}_{uv}",
                    placeholder="https://seu-app.streamlit.app",
                )
                edited_apps.append(
                    {
                        "nome": nome,
                        "descricao": descricao_app,
                        "icone": icone,
                        "status": status,
                        "url": url,
                    }
                )

        apply_changes = st.form_submit_button("Aplicar alterações", use_container_width=True)

    if apply_changes:
        new_cfg = copy.deepcopy(cfg)

        if clear_logo_top:
            new_cfg["logo_top"] = ""
        elif logo_top_file is not None:
            new_cfg["logo_top"] = upload_to_data_uri(logo_top_file)

        if clear_logo_footer:
            new_cfg["logo_footer"] = ""
        elif logo_footer_file is not None:
            new_cfg["logo_footer"] = upload_to_data_uri(logo_footer_file)

        if restore_hero:
            new_cfg["hero_image"] = DEFAULT_CONFIG["hero_image"]
        elif hero_file is not None:
            new_cfg["hero_image"] = upload_to_data_uri(hero_file)

        new_cfg["titulo"] = titulo
        new_cfg["subtitulo"] = subtitulo
        new_cfg["descricao"] = descricao
        new_cfg["slogan"] = slogan
        new_cfg["usuario"] = usuario
        new_cfg["rodape_esquerdo"] = rodape_esquerdo
        new_cfg["rodape_direito"] = rodape_direito
        new_cfg["apps"] = edited_apps

        st.session_state.hub_config = new_cfg
        st.success("Configurações aplicadas.")
        st.rerun()

    if st.button("Restaurar tudo ao padrão", use_container_width=True):
        st.session_state.hub_config = copy.deepcopy(DEFAULT_CONFIG)
        st.session_state.upload_version += 1
        st.rerun()

cfg = st.session_state.hub_config

# ============================================================
# ESTILO
# ============================================================
st.html(
    """
<style>
    :root{
        --setta-yellow:#FDC33B;
        --setta-yellow-2:#F9B719;
        --setta-ink:#1E232E;
        --setta-muted:#6B7792;
        --setta-line:#E7EBF1;
        --setta-bg:#F8FAFD;
        --setta-green:#0FAF4D;
    }

    .stApp{
        background:linear-gradient(180deg,#FFFFFF 0%,#F8FAFD 100%);
    }

    header[data-testid="stHeader"]{
        background:transparent !important;
        height:0 !important;
        overflow:visible !important;
        z-index:99999 !important;
    }

    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    #MainMenu,
    footer{
        display:none !important;
    }

    [data-testid="stSidebar"]{
        border-right:1px solid #E7EBF1 !important;
        background:#FFFFFF !important;
    }

    [data-testid="stSidebar"] > div:first-child{
        background:#FFFFFF !important;
    }

    /* Mantém o controle para reabrir o menu sempre visível. */
    [data-testid="stSidebarCollapsedControl"]{
        display:flex !important;
        visibility:visible !important;
        opacity:1 !important;
        position:fixed !important;
        top:16px !important;
        left:16px !important;
        z-index:100000 !important;
        width:40px !important;
        height:40px !important;
        align-items:center !important;
        justify-content:center !important;
        background:#FFFFFF !important;
        border:1px solid rgba(30,35,46,.12) !important;
        border-radius:10px !important;
        box-shadow:0 4px 14px rgba(30,35,46,.12) !important;
    }

    .block-container{
        max-width:100% !important;
        padding:0 !important;
        margin:0 !important;
    }

    .topbar{
        height:82px;
        background:linear-gradient(90deg,var(--setta-yellow) 0%,#FFC83E 62%,var(--setta-yellow) 100%);
        display:flex;
        align-items:center;
        justify-content:space-between;
        padding:0 5%;
        border-bottom:1px solid rgba(0,0,0,.05);
    }

    .brand-slot{
        width:165px;
        height:58px;
        display:flex;
        align-items:center;
        justify-content:flex-start;
        overflow:hidden;
    }

    .brand-text{
        color:var(--setta-ink);
        font-size:43px;
        font-style:italic;
        font-weight:900;
        letter-spacing:-3px;
        line-height:1;
        white-space:nowrap;
    }

    .brand-logo{
        width:165px;
        height:58px;
        object-fit:contain;
        object-position:left center;
        display:block;
    }

    .user{
        color:var(--setta-ink);
        font-size:15px;
        font-weight:700;
        display:flex;
        gap:10px;
        align-items:center;
    }

    .user-badge{
        width:34px;
        height:34px;
        border-radius:50%;
        display:grid;
        place-items:center;
        background:#fff;
        border:1px solid rgba(30,35,46,.2);
        font-size:16px;
    }

    .hero{
        display:grid;
        grid-template-columns:1.02fr 1fr;
        min-height:290px;
        background:#fff;
        overflow:hidden;
    }

    .hero-copy{
        position:relative;
        padding:62px 5% 44px 5%;
        z-index:2;
        background:linear-gradient(120deg,#FFFFFF 0%,#FFFFFF 72%,rgba(255,255,255,.92) 78%,rgba(255,255,255,0) 79%);
    }

    .hero h1{
        margin:0;
        color:var(--setta-ink);
        font-size:48px;
        line-height:1.03;
        letter-spacing:-2px;
        font-weight:900;
    }

    .hero h2{
        margin:8px 0 0 0;
        color:#66728B;
        font-size:27px;
        line-height:1.2;
        font-weight:500;
    }

    .hero p{
        margin:20px 0 0 0;
        color:#73809B;
        font-size:16px;
        line-height:1.55;
        max-width:600px;
    }

    .hero-image{
        min-height:290px;
        background-size:cover;
        background-position:center;
        position:relative;
    }

    .hero-image::before{
        content:"";
        position:absolute;
        left:-70px;
        top:0;
        width:120px;
        height:100%;
        transform:skewX(-25deg);
        background:linear-gradient(180deg,rgba(253,195,59,.16),rgba(255,255,255,.8));
        z-index:1;
    }

    .hero-slogan{
        position:absolute;
        right:7%;
        top:38px;
        color:#60708F;
        font-size:12px;
        letter-spacing:4px;
        line-height:1.7;
        font-weight:700;
        text-align:left;
        z-index:2;
    }

    .hero-slogan::after{
        content:"";
        display:block;
        width:42px;
        height:3px;
        border-radius:6px;
        background:var(--setta-yellow-2);
        margin-top:8px;
    }

    .apps-wrap{
        padding:0 4% 28px 4%;
        margin-top:-10px;
        position:relative;
        z-index:5;
    }

    .apps-grid{
        display:grid;
        grid-template-columns:repeat(3,minmax(0,1fr));
        gap:20px;
    }

    .app-card{
        min-height:190px;
        display:flex;
        flex-direction:column;
        justify-content:space-between;
        text-decoration:none !important;
        color:inherit !important;
        background:radial-gradient(circle at 108% 110%,rgba(253,195,59,.16) 0 27%,transparent 28%),#FFFFFF;
        border:1px solid var(--setta-line);
        border-radius:16px;
        padding:24px 30px 22px 30px;
        box-shadow:0 8px 24px rgba(44,62,92,.06);
        transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease;
    }

    .app-card:hover{
        transform:translateY(-4px);
        box-shadow:0 16px 34px rgba(44,62,92,.12);
        border-color:#D9DDE5;
    }

    .card-top{
        display:flex;
        align-items:flex-start;
        justify-content:space-between;
        gap:16px;
    }

    .app-icon{
        width:66px;
        height:66px;
        border-radius:15px;
        display:grid;
        place-items:center;
        font-size:34px;
        background:#FFF7E2;
        overflow:hidden;
    }

    .status{
        display:flex;
        align-items:center;
        gap:7px;
        background:#E9F9EF;
        color:#15883F;
        font-size:13px;
        font-weight:700;
        border-radius:999px;
        padding:7px 12px;
        white-space:nowrap;
    }

    .dot{
        width:10px;
        height:10px;
        border-radius:50%;
        background:var(--setta-green);
        box-shadow:0 0 0 3px rgba(15,175,77,.08);
    }

    .app-title{
        margin-top:10px;
        color:#101738;
        font-weight:900;
        font-size:24px;
        line-height:1.15;
    }

    .app-desc{
        margin-top:4px;
        color:#77839B;
        font-size:15px;
        line-height:1.35;
    }

    .access{
        margin-top:20px;
        color:#F1A000;
        font-size:16px;
        font-weight:800;
        display:flex;
        align-items:center;
        gap:10px;
    }

    .arrow{
        font-size:22px;
        transition:transform .18s ease;
    }

    .app-card:hover .arrow{
        transform:translateX(4px);
    }

    .page-footer{
        min-height:62px;
        border-top:1px solid var(--setta-line);
        display:flex;
        align-items:center;
        justify-content:space-between;
        padding:0 4%;
        background:#fff;
        color:#97A2B8;
        font-size:11px;
        letter-spacing:2px;
        text-transform:uppercase;
    }

    .footer-brand{
        display:flex;
        align-items:center;
        gap:12px;
        min-width:0;
    }

    .footer-logo-slot{
        width:72px;
        height:30px;
        display:flex;
        align-items:center;
        justify-content:flex-start;
        overflow:hidden;
        flex:0 0 72px;
    }

    .footer-brand-text{
        color:var(--setta-ink);
        font-size:21px;
        font-style:italic;
        font-weight:900;
        letter-spacing:-1px;
        text-transform:none;
        white-space:nowrap;
    }

    .footer-logo{
        width:72px;
        height:30px;
        object-fit:contain;
        object-position:left center;
        display:block;
    }

    .footer-line{
        width:32px;
        height:3px;
        border-radius:4px;
        background:var(--setta-yellow-2);
        display:inline-block;
        margin-left:10px;
    }

    @media(max-width:1100px){
        .hero h1{font-size:40px;}
        .hero h2{font-size:23px;}
        .apps-grid{grid-template-columns:repeat(2,minmax(0,1fr));}
    }

    @media(max-width:760px){
        .topbar{height:70px;padding:0 20px 0 70px;}
        .brand-slot{width:140px;height:50px;}
        .brand-logo{width:140px;height:50px;}
        .brand-text{font-size:35px;}
        .user span:last-child{display:none;}
        .hero{grid-template-columns:1fr;}
        .hero-copy{padding:38px 22px 32px 22px;background:#fff;}
        .hero h1{font-size:34px;letter-spacing:-1px;}
        .hero h2{font-size:20px;}
        .hero p{font-size:14px;}
        .hero-image{min-height:190px;}
        .apps-wrap{padding:18px 18px 28px 18px;margin-top:0;}
        .apps-grid{grid-template-columns:1fr;}
        .app-card{min-height:175px;padding:22px;}
        .page-footer{flex-direction:column;gap:10px;justify-content:center;text-align:center;padding:16px 18px;}
        .footer-brand{justify-content:center;flex-wrap:wrap;}
    }
</style>
"""
)

logo_top_html = (
    f'<img class="brand-logo" src="{cfg["logo_top"]}" alt="Logo superior">'
    if cfg["logo_top"]
    else '<div class="brand-text">Setta</div>'
)

logo_footer_html = (
    f'<img class="footer-logo" src="{cfg["logo_footer"]}" alt="Logo inferior">'
    if cfg["logo_footer"]
    else '<div class="footer-brand-text">Setta</div>'
)

hero_image = esc(cfg["hero_image"])
hero_style = f"background-image:url('{hero_image}');"
descricao_html = esc(cfg["descricao"]).replace("\n", "<br>")
slogan_html = esc(cfg["slogan"]).replace("\n", "<br>")

cards_html = ""
for app in cfg["apps"]:
    url = esc(safe_url(app["url"]))
    cards_html += f"""
    <a class="app-card" href="{url}" target="_blank" rel="noopener noreferrer">
        <div>
            <div class="card-top">
                <div class="app-icon">{esc(app["icone"])}</div>
                <div class="status"><span class="dot"></span>{esc(app["status"])}</div>
            </div>
            <div class="app-title">{esc(app["nome"])}</div>
            <div class="app-desc">{esc(app["descricao"])}</div>
        </div>
        <div class="access">Acessar <span class="arrow">→</span></div>
    </a>
    """

page_html = f"""
<div class="topbar">
    <div class="brand-slot">{logo_top_html}</div>
    <div class="user">
        <div class="user-badge">●</div>
        <span>{esc(cfg["usuario"])}</span>
        <span>⌄</span>
    </div>
</div>

<section class="hero">
    <div class="hero-copy">
        <h1>{esc(cfg["titulo"])}</h1>
        <h2>{esc(cfg["subtitulo"])}</h2>
        <p>{descricao_html}</p>
    </div>
    <div class="hero-image" style="{hero_style}">
        <div class="hero-slogan">{slogan_html}</div>
    </div>
</section>

<div class="apps-wrap">
    <div class="apps-grid">{cards_html}</div>
</div>

<div class="page-footer">
    <div class="footer-brand">
        <div class="footer-logo-slot">{logo_footer_html}</div>
        <span>|</span>
        <span>{esc(cfg["rodape_esquerdo"])}</span>
    </div>
    <div>
        {esc(cfg["rodape_direito"])} <span class="footer-line"></span>
    </div>
</div>
"""

st.html(page_html)
