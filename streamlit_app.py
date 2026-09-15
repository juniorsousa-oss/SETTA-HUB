import base64
import copy
import html
from datetime import datetime, timezone
from io import BytesIO
from urllib.parse import urlparse

import requests
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="SETTA HUB | Central de Aplicativos",
    page_icon="🟨",
    layout="wide",
    initial_sidebar_state="expanded",
)

SB_URL = "https://cuixazpxkvniqldmmnth.supabase.co"
SB_KEY = "sb_publishable_ZTqIgmA9Ez6AVQsoXa0P8Q_6CYHDFye"
SB_TABLE = "setta_hub_config"
SB_ID = "main"

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
        {"nome": "Gestão Almoxarifado", "descricao": "Gestão completa da operação", "icone": "📦", "icone_png": "", "status": "Online", "url": "#"},
        {"nome": "Dashboard Operacional", "descricao": "Indicadores e resultados", "icone": "📊", "icone_png": "", "status": "Online", "url": "#"},
        {"nome": "MRP", "descricao": "Demanda e necessidade de materiais", "icone": "📋", "icone_png": "", "status": "Ativo", "url": "#"},
        {"nome": "Entregas", "descricao": "Controle de OPs e cronograma", "icone": "🚚", "icone_png": "", "status": "Online", "url": "#"},
        {"nome": "Compra Fácil", "descricao": "Compras e histórico de preços", "icone": "🛒", "icone_png": "", "status": "Ativo", "url": "#"},
        {"nome": "Gestão de Equipe", "descricao": "Colaboradores e plano de carreira", "icone": "👥", "icone_png": "", "status": "Online", "url": "#"},
    ],
}


def sb_headers(extra=None):
    headers = {
        "apikey": SB_KEY,
        "Authorization": f"Bearer {SB_KEY}",
        "Content-Type": "application/json",
    }
    headers.update(extra or {})
    return headers


def merge_config(saved):
    cfg = copy.deepcopy(DEFAULT_CONFIG)
    if not isinstance(saved, dict):
        return cfg

    for key in (
        "logo_top",
        "logo_footer",
        "hero_image",
        "titulo",
        "subtitulo",
        "descricao",
        "slogan",
        "usuario",
        "rodape_esquerdo",
        "rodape_direito",
    ):
        if key in saved:
            cfg[key] = saved[key]

    if isinstance(saved.get("apps"), list) and saved["apps"]:
        cfg["apps"] = []
        for item in saved["apps"]:
            app = dict(item) if isinstance(item, dict) else {}
            app.setdefault("nome", "Aplicativo")
            app.setdefault("descricao", "")
            app.setdefault("icone", "🔗")
            app.setdefault("icone_png", "")
            app.setdefault("status", "Ativo")
            app.setdefault("url", "#")
            cfg["apps"].append(app)
    return cfg


def save_db(cfg):
    payload = {
        "id": SB_ID,
        "config": cfg,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    response = requests.post(
        f"{SB_URL}/rest/v1/{SB_TABLE}",
        headers=sb_headers({"Prefer": "resolution=merge-duplicates,return=minimal"}),
        params={"on_conflict": "id"},
        json=payload,
        timeout=25,
    )
    response.raise_for_status()


def load_db():
    response = requests.get(
        f"{SB_URL}/rest/v1/{SB_TABLE}",
        headers=sb_headers(),
        params={"id": f"eq.{SB_ID}", "select": "config", "limit": "1"},
        timeout=12,
    )
    response.raise_for_status()
    rows = response.json()
    if rows:
        return merge_config(rows[0].get("config"))
    save_db(DEFAULT_CONFIG)
    return copy.deepcopy(DEFAULT_CONFIG)


def data_uri(uploaded_file, max_mb=4):
    if uploaded_file is None:
        return ""
    if uploaded_file.size > max_mb * 1024 * 1024:
        raise ValueError(f"Imagem acima de {max_mb} MB.")
    mime = uploaded_file.type or "image/png"
    return f"data:{mime};base64,{base64.b64encode(uploaded_file.getvalue()).decode()}"


def icon_png(uploaded_file):
    if uploaded_file is None:
        return ""
    if uploaded_file.size > 2 * 1024 * 1024:
        raise ValueError("Ícone PNG acima de 2 MB.")

    image = Image.open(BytesIO(uploaded_file.getvalue())).convert("RGBA")
    image.thumbnail((104, 104), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (128, 128), (255, 255, 255, 0))
    canvas.alpha_composite(image, ((128 - image.width) // 2, (128 - image.height) // 2))
    output = BytesIO()
    canvas.save(output, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(output.getvalue()).decode()


def safe_url(value):
    value = (value or "").strip()
    parsed = urlparse(value)
    return value if value != "#" and parsed.scheme in {"http", "https"} and parsed.netloc else "#"


def esc(value):
    return html.escape(str(value or ""), quote=True)


if "hub_config" not in st.session_state:
    try:
        st.session_state.hub_config = load_db()
        st.session_state.db_ok = True
    except Exception:
        st.session_state.hub_config = copy.deepcopy(DEFAULT_CONFIG)
        st.session_state.db_ok = False

if "uv" not in st.session_state:
    st.session_state.uv = 0
if "notice" not in st.session_state:
    st.session_state.notice = ""

cfg = st.session_state.hub_config
uv = st.session_state.uv

with st.sidebar:
    st.title("⚙️ Configurações")
    if st.session_state.get("db_ok"):
        st.success("Salvamento permanente ativo")
    else:
        st.warning("Modo temporário: banco indisponível")

    if st.session_state.notice:
        st.info(st.session_state.notice)
        st.session_state.notice = ""

    with st.form("cfg"):
        st.subheader("Identidade visual")
        logo_top_upload = st.file_uploader(
            "Logo do menu superior",
            type=["png", "jpg", "jpeg", "webp"],
            key=f"lt{uv}",
            help="Ajuste automático sem deformar.",
        )
        logo_footer_upload = st.file_uploader(
            "Logo inferior",
            type=["png", "jpg", "jpeg", "webp"],
            key=f"lf{uv}",
        )
        hero_upload = st.file_uploader(
            "Imagem principal",
            type=["png", "jpg", "jpeg", "webp"],
            key=f"h{uv}",
        )

        clear_top = st.checkbox("Remover logo superior e usar texto Setta")
        clear_footer = st.checkbox("Usar logo inferior padrão")
        clear_hero = st.checkbox("Usar imagem principal padrão")

        if cfg.get("logo_top"):
            st.caption("Logo superior atual")
            st.image(cfg["logo_top"], width=150)

        st.divider()
        st.subheader("Textos da página")
        titulo = st.text_input("Título", cfg["titulo"])
        subtitulo = st.text_input("Subtítulo", cfg["subtitulo"])
        descricao = st.text_area("Descrição", cfg["descricao"], height=90)
        slogan = st.text_area("Texto sobre a imagem", cfg["slogan"], height=90)
        usuario = st.text_input("Usuário do cabeçalho", cfg["usuario"])
        rodape_esquerdo = st.text_input("Texto inferior esquerdo", cfg["rodape_esquerdo"])
        rodape_direito = st.text_input("Texto inferior direito", cfg["rodape_direito"])

        st.divider()
        st.subheader("Cartões e redirecionamentos")
        st.caption("PNG padronizado: canvas 128×128, conteúdo até 104×104 e exibição 56×56 px.")

        apps = []
        uploads = []
        removes = []

        for i, app in enumerate(cfg["apps"]):
            with st.expander(f"{i + 1}. {app.get('nome', 'Aplicativo')}"):
                nome = st.text_input("Nome do cartão", app.get("nome", ""), key=f"n{i}_{uv}")
                desc = st.text_input("Descrição", app.get("descricao", ""), key=f"d{i}_{uv}")
                status = st.text_input("Status", app.get("status", "Ativo"), key=f"s{i}_{uv}")
                url = st.text_input("Link de destino", app.get("url", "#"), key=f"u{i}_{uv}")
                upload = st.file_uploader(
                    "Ícone PNG",
                    type=["png"],
                    key=f"p{i}_{uv}",
                    help="Máximo 2 MB. Redimensionamento automático.",
                )
                remove = st.checkbox("Remover PNG e voltar para emoji", key=f"r{i}_{uv}")
                emoji = st.text_input("Emoji de fallback", app.get("icone", "🔗"), key=f"e{i}_{uv}")

                if app.get("icone_png"):
                    st.image(app["icone_png"], width=72)

            apps.append(
                {
                    "nome": nome,
                    "descricao": desc,
                    "icone": emoji,
                    "icone_png": app.get("icone_png", ""),
                    "status": status,
                    "url": url,
                }
            )
            uploads.append(upload)
            removes.append(remove)

        apply_changes = st.form_submit_button("Salvar alterações", use_container_width=True, type="primary")

    if apply_changes:
        try:
            new_cfg = copy.deepcopy(cfg)

            if clear_top:
                new_cfg["logo_top"] = ""
            elif logo_top_upload:
                new_cfg["logo_top"] = data_uri(logo_top_upload, 3)

            if clear_footer:
                new_cfg["logo_footer"] = ""
            elif logo_footer_upload:
                new_cfg["logo_footer"] = data_uri(logo_footer_upload, 3)

            if clear_hero:
                new_cfg["hero_image"] = DEFAULT_CONFIG["hero_image"]
            elif hero_upload:
                new_cfg["hero_image"] = data_uri(hero_upload, 4)

            for i, app in enumerate(apps):
                if removes[i]:
                    app["icone_png"] = ""
                elif uploads[i]:
                    app["icone_png"] = icon_png(uploads[i])

            new_cfg.update(
                titulo=titulo,
                subtitulo=subtitulo,
                descricao=descricao,
                slogan=slogan,
                usuario=usuario,
                rodape_esquerdo=rodape_esquerdo,
                rodape_direito=rodape_direito,
                apps=apps,
            )
            save_db(new_cfg)
            st.session_state.hub_config = new_cfg
            st.session_state.db_ok = True
            st.session_state.uv += 1
            st.session_state.notice = "Alterações salvas permanentemente."
            st.rerun()
        except Exception as exc:
            st.error(f"Não foi possível salvar: {exc}")

    if st.button("Recarregar do banco", use_container_width=True):
        try:
            st.session_state.hub_config = load_db()
            st.session_state.uv += 1
            st.session_state.db_ok = True
            st.session_state.notice = "Dados recarregados."
            st.rerun()
        except Exception as exc:
            st.error(str(exc))

    if st.button("Restaurar tudo ao padrão", use_container_width=True):
        try:
            default_cfg = copy.deepcopy(DEFAULT_CONFIG)
            save_db(default_cfg)
            st.session_state.hub_config = default_cfg
            st.session_state.uv += 1
            st.session_state.notice = "Padrão restaurado."
            st.rerun()
        except Exception as exc:
            st.error(str(exc))

cfg = st.session_state.hub_config

CSS = r'''<style>
:root{
  --y:#FDC33B;
  --y2:#F9B719;
  --ink:#1E232E;
  --line:#E7EBF1;
  --green:#0FAF4D;
  --page-pad:clamp(18px,4vw,76px);
}

*{box-sizing:border-box}
html,body,[data-testid="stAppViewContainer"]{min-height:100%}
.stApp{background:linear-gradient(180deg,#fff,#F8FAFD)}

header[data-testid="stHeader"]{
  background:var(--y)!important;
  height:68px!important;
  border-bottom:1px solid rgba(0,0,0,.06)!important;
  z-index:100000!important;
}
header[data-testid="stHeader"] *{color:var(--ink)!important}
[data-testid="stToolbar"]{background:transparent!important}
[data-testid="stDecoration"],#MainMenu,footer{display:none!important}
[data-testid="stSidebar"]{border-right:1px solid var(--line)!important;background:#fff!important;z-index:100005!important}
[data-testid="stSidebar"]>div:first-child{background:#fff!important}
.block-container{max-width:100%!important;padding:0!important;margin:0!important}

.hub-header-content{
  position:fixed;
  top:0;left:0;right:0;
  height:68px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 clamp(170px,12vw,230px) 0 clamp(62px,4vw,78px);
  z-index:100002;
  pointer-events:none;
}

.page-root{
  padding-top:68px;
  min-height:100dvh;
  display:flex;
  flex-direction:column;
}

.brand-slot{width:180px;height:58px;display:flex;align-items:center;overflow:hidden}
.brand-text{color:var(--ink);font-size:clamp(35px,2.35vw,43px);font-style:italic;font-weight:900;letter-spacing:-3px}
.brand-logo{width:180px;height:54px;max-width:180px;max-height:54px;object-fit:contain;object-position:left center}
.user{color:var(--ink);font-size:clamp(13px,.85vw,15px);font-weight:700;display:flex;gap:10px;align-items:center;white-space:nowrap}
.user-badge{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:#fff;border:1px solid rgba(30,35,46,.2)}

.hero{
  display:grid;
  grid-template-columns:minmax(0,1.02fr) minmax(0,1fr);
  min-height:clamp(240px,30vh,310px);
  background:#fff;
  overflow:hidden;
}
.hero-copy{
  padding:clamp(38px,4vw,62px) var(--page-pad) clamp(32px,3vw,44px);
  z-index:2;
  background:linear-gradient(120deg,#fff 0%,#fff 72%,rgba(255,255,255,.92) 78%,rgba(255,255,255,0) 79%);
}
.hero h1{margin:0;color:var(--ink);font-size:clamp(34px,2.6vw,48px);line-height:1.03;letter-spacing:-2px;font-weight:900}
.hero h2{margin:8px 0 0;color:#66728B;font-size:clamp(20px,1.55vw,27px);line-height:1.2;font-weight:500}
.hero p{margin:clamp(14px,1.25vw,20px) 0 0;color:#73809B;font-size:clamp(13px,.92vw,16px);line-height:1.55;max-width:620px}
.hero-image{min-height:clamp(240px,30vh,310px);background-size:cover;background-position:center;position:relative}
.hero-slogan{position:absolute;right:7%;top:clamp(24px,3vw,38px);color:#60708F;font-size:clamp(10px,.7vw,12px);letter-spacing:4px;line-height:1.7;font-weight:700}
.hero-slogan:after{content:"";display:block;width:42px;height:3px;background:var(--y2);margin-top:8px}

.apps-wrap{
  width:100%;
  padding:clamp(8px,1vw,14px) var(--page-pad) clamp(22px,2vw,32px);
  margin-top:clamp(-12px,-.65vw,-6px);
  position:relative;
  z-index:5;
  flex:1 0 auto;
}
.apps-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:clamp(14px,1.1vw,22px);
}
.app-card{
  min-height:clamp(182px,22vh,220px);
  display:flex;
  flex-direction:column;
  justify-content:space-between;
  text-decoration:none!important;
  color:inherit!important;
  background:radial-gradient(circle at 108% 110%,rgba(253,195,59,.16) 0 27%,transparent 28%),#fff;
  border:1px solid var(--line);
  border-radius:16px;
  padding:clamp(20px,1.45vw,26px) clamp(22px,1.7vw,32px);
  box-shadow:0 8px 24px rgba(44,62,92,.06);
  transition:.18s;
}
.app-card:hover{transform:translateY(-4px);box-shadow:0 16px 34px rgba(44,62,92,.12)}
.card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}
.app-icon{width:72px;height:72px;border-radius:16px;display:flex;align-items:center;justify-content:center;background:#FFF7E2;overflow:hidden;flex:0 0 72px}
.app-icon img{width:56px;height:56px;object-fit:contain}
.app-icon-emoji{font-size:34px}
.status{display:flex;align-items:center;gap:7px;background:#E9F9EF;color:#15883F;font-size:clamp(11px,.75vw,13px);font-weight:700;border-radius:999px;padding:7px 12px;white-space:nowrap}
.dot{width:10px;height:10px;border-radius:50%;background:var(--green);flex:0 0 10px}
.app-title{margin-top:10px;color:#101738;font-weight:900;font-size:clamp(20px,1.3vw,24px);line-height:1.16}
.app-desc{margin-top:5px;color:#77839B;font-size:clamp(13px,.85vw,15px);line-height:1.4}
.access{margin-top:18px;color:#F1A000;font-size:clamp(14px,.9vw,16px);font-weight:800;display:flex;gap:10px}

.page-footer{
  min-height:52px;
  border-top:1px solid var(--line);
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 var(--page-pad);
  background:#fff;
  color:#97A2B8;
  font-size:clamp(9px,.65vw,11px);
  letter-spacing:2px;
  text-transform:uppercase;
  margin-top:auto;
}
.footer-brand{display:flex;align-items:center;gap:12px;min-width:0}
.footer-logo-slot{width:72px;height:30px;display:flex;align-items:center;flex:0 0 72px}
.footer-brand-text{color:var(--ink);font-size:21px;font-style:italic;font-weight:900}
.footer-logo{width:72px;height:30px;object-fit:contain}
.footer-line{width:32px;height:3px;background:var(--y2);display:inline-block;margin-left:10px}

@media (min-width:1200px) and (max-height:900px){
  header[data-testid="stHeader"]{height:62px!important}
  .hub-header-content{height:62px}
  .page-root{padding-top:62px}

  .brand-slot{height:50px}
  .brand-logo{height:46px;max-height:46px}
  .brand-text{font-size:36px}
  .user-badge{width:30px;height:30px}
  .user{font-size:13px}

  .hero{min-height:230px}
  .hero-image{min-height:230px}
  .hero-copy{padding-top:32px;padding-bottom:24px}
  .hero h1{font-size:38px}
  .hero h2{font-size:22px}
  .hero p{margin-top:12px;font-size:13px}

  .apps-wrap{padding-top:8px;padding-bottom:14px;margin-top:-6px}
  .apps-grid{gap:14px}
  .app-card{min-height:176px;padding:18px 22px}
  .app-icon{width:68px;height:68px;flex-basis:68px}
  .app-icon img{width:54px;height:54px}
  .app-title{font-size:20px;margin-top:8px}
  .app-desc{font-size:13px;margin-top:4px}
  .access{margin-top:12px;font-size:14px}
  .status{padding:6px 10px;font-size:11px}

  .page-footer{min-height:44px}
  .footer-logo-slot{height:24px}
  .footer-logo{height:24px}
  .footer-brand-text{font-size:18px}
}

@media (max-width:1320px){
  :root{--page-pad:clamp(18px,3vw,42px)}
  .hub-header-content{padding-right:170px}
  .hero{grid-template-columns:1fr 1fr}
  .app-card{padding:20px 22px}
  .app-title{font-size:20px}
}

@media (max-width:1120px){
  .apps-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .user{display:none}
  .hero h1{font-size:40px}
}

@media (max-width:760px){
  header[data-testid="stHeader"]{height:66px!important}
  .hub-header-content{height:66px;padding:0 20px 0 62px}
  .page-root{padding-top:66px;min-height:100dvh}
  .brand-slot{width:150px;height:50px}
  .brand-logo{width:150px;height:46px}
  .brand-text{font-size:35px}
  .hero{grid-template-columns:1fr;min-height:auto}
  .hero-copy{padding:34px 22px 28px;background:#fff}
  .hero h1{font-size:34px}
  .hero h2{font-size:20px}
  .hero-image{min-height:190px}
  .apps-wrap{padding:18px;margin-top:0}
  .apps-grid{grid-template-columns:1fr}
  .app-card{min-height:180px;padding:22px}
  .page-footer{flex-direction:column;gap:10px;padding:16px 18px;text-align:center}
  .footer-brand{justify-content:center;flex-wrap:wrap}
}
</style>'''

st.html(CSS)

logo_top = (
    f'<img class="brand-logo" src="{cfg["logo_top"]}" alt="Logo">'
    if cfg.get("logo_top")
    else '<div class="brand-text">Setta</div>'
)
logo_footer = (
    f'<img class="footer-logo" src="{cfg["logo_footer"]}" alt="Logo">'
    if cfg.get("logo_footer")
    else '<div class="footer-brand-text">Setta</div>'
)


def icon_html(app):
    if app.get("icone_png"):
        return f'<img src="{app.get("icone_png")}" alt="Ícone">'
    return f'<span class="app-icon-emoji">{esc(app.get("icone", "🔗"))}</span>'


cards = ""
for app in cfg["apps"]:
    cards += (
        f'<a class="app-card" href="{esc(safe_url(app.get("url", "#")))}" target="_blank">'
        f'<div><div class="card-top"><div class="app-icon">{icon_html(app)}</div>'
        f'<div class="status"><span class="dot"></span>{esc(app.get("status", "Ativo"))}</div></div>'
        f'<div class="app-title">{esc(app.get("nome", "Aplicativo"))}</div>'
        f'<div class="app-desc">{esc(app.get("descricao", ""))}</div></div>'
        f'<div class="access">Acessar →</div></a>'
    )

page = (
    f'<div class="hub-header-content"><div class="brand-slot">{logo_top}</div>'
    f'<div class="user"><div class="user-badge">●</div><span>{esc(cfg["usuario"])}</span></div></div>'
    f'<div class="page-root"><section class="hero"><div class="hero-copy">'
    f'<h1>{esc(cfg["titulo"])}</h1><h2>{esc(cfg["subtitulo"])}</h2>'
    f'<p>{esc(cfg["descricao"]).replace(chr(10), "<br>")}</p></div>'
    f'<div class="hero-image" style="background-image:url(\'{esc(cfg["hero_image"])}\')">'
    f'<div class="hero-slogan">{esc(cfg["slogan"]).replace(chr(10), "<br>")}</div></div></section>'
    f'<div class="apps-wrap"><div class="apps-grid">{cards}</div></div>'
    f'<div class="page-footer"><div class="footer-brand"><div class="footer-logo-slot">{logo_footer}</div>'
    f'<span>|</span><span>{esc(cfg["rodape_esquerdo"])}</span></div>'
    f'<div>{esc(cfg["rodape_direito"])}<span class="footer-line"></span></div></div></div>'
)

st.html(page)
