import base64
import copy
import html
import hashlib
import hmac
from datetime import datetime, timezone
from io import BytesIO
from urllib.parse import urlparse

import requests
import streamlit as st
from PIL import Image

favicon = Image.open("favicon.png.png")

st.set_page_config(
    page_title="ALMOXHUB | SETTA",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="collapsed",
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
    "user_avatar": "",
    "rodape_esquerdo": "TECNOLOGIA A SERVIÇO DE GRANDES RESULTADOS",
    "rodape_direito": "JUNTOS, CONSTRUÍMOS O AMANHÃ",
    "apps": [
        {"nome": "Gestão Almoxarifado", "descricao": "Gestão completa da operação", "icone": "📦", "icone_png": "", "status": "Online", "url": "#"},
        {"nome": "Dashboard Operacional", "descricao": "Indicadores e resultados", "icone": "📊", "icone_png": "", "status": "Online", "url": "#"},
        {"nome": "MRP", "descricao": "Demanda e necessidade de materiais", "icone": "📋", "icone_png": "", "status": "Ativo", "url": "#"},
        {"nome": "Entregas", "descricao": "Controle de OPs e cronograma", "icone": "🚚", "icone_png": "", "status": "Online", "url": "#"},
        {"nome": "Compra Fácil", "descricao": "Compras e histórico de preços", "icone": "🛒", "icone_png": "", "status": "Ativo", "url": "#"},
        {"nome": "Gestão de Equipe", "descricao": "Colaboradores e plano de carreira", "icone": "👥", "icone_png": "", "status": "Online", "url": "#"},
        {"nome": "Novo Aplicativo 7", "descricao": "Espaço disponível para novo aplicativo", "icone": "➕", "icone_png": "", "status": "Disponível", "url": "#"},
        {"nome": "Novo Aplicativo 8", "descricao": "Espaço disponível para novo aplicativo", "icone": "➕", "icone_png": "", "status": "Disponível", "url": "#"},
        {"nome": "Novo Aplicativo 9", "descricao": "Espaço disponível para novo aplicativo", "icone": "➕", "icone_png": "", "status": "Disponível", "url": "#"},
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
        "user_avatar",
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

        # Mantém os cartões já salvos e completa automaticamente até o total padrão.
        while len(cfg["apps"]) < len(DEFAULT_CONFIG["apps"]):
            idx = len(cfg["apps"])
            cfg["apps"].append(copy.deepcopy(DEFAULT_CONFIG["apps"][idx]))
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


def user_avatar_image(uploaded_file):
    if uploaded_file is None:
        return ""
    if uploaded_file.size > 2 * 1024 * 1024:
        raise ValueError("Imagem do usuário acima de 2 MB.")

    image = Image.open(BytesIO(uploaded_file.getvalue())).convert("RGBA")
    side = min(image.width, image.height)
    left = (image.width - side) // 2
    top = (image.height - side) // 2
    image = image.crop((left, top, left + side, top + side))
    image = image.resize((128, 128), Image.Resampling.LANCZOS)

    output = BytesIO()
    image.save(output, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(output.getvalue()).decode()


def safe_url(value):
    value = (value or "").strip()
    parsed = urlparse(value)
    return value if value != "#" and parsed.scheme in {"http", "https"} and parsed.netloc else "#"


def esc(value):
    return html.escape(str(value or ""), quote=True)


ADMIN_PASSWORD_FALLBACK_HASH = "c554a2703714f35c0c629ee4e73f84fd360220d6e3b7c65ba81b29343affc50d"


def admin_password_valid(password):
    try:
        configured = str(st.secrets.get("SETTA_HUB_ADMIN_PASSWORD", "")).strip()
    except Exception:
        configured = ""

    if configured:
        return hmac.compare_digest(str(password), configured)

    digest = hashlib.sha256(str(password).encode("utf-8")).hexdigest()
    return hmac.compare_digest(digest, ADMIN_PASSWORD_FALLBACK_HASH)


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
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

cfg = st.session_state.hub_config
uv = st.session_state.uv

with st.sidebar:
    if not st.session_state.admin_authenticated:
        st.markdown(
            '<div class="admin-login-head">'
            '<div class="admin-login-kicker">🔐 ÁREA ADMINISTRATIVA</div>'
            '<div class="admin-login-title">Acesso às configurações</div>'
            '<div class="admin-login-subtitle">Digite a senha para liberar a personalização do SETTA HUB.</div>'
            '<div class="admin-login-accent"></div>'
            '</div>',
            unsafe_allow_html=True,
        )

        with st.form("admin_login", clear_on_submit=False):
            admin_password = st.text_input(
                "Senha",
                type="password",
                placeholder="Digite a senha administrativa",
                autocomplete="current-password",
            )
            login = st.form_submit_button(
                "Entrar nas configurações",
                use_container_width=True,
                type="primary",
            )

        st.markdown(
            '<div class="admin-login-note">'
            'A tela principal continua acessível normalmente. Apenas a área de configuração exige autenticação.'
            '</div>',
            unsafe_allow_html=True,
        )

        if login:
            if admin_password_valid(admin_password):
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Senha incorreta. Verifique e tente novamente.")
    else:
        if st.button("🔒 Sair das configurações", use_container_width=True):
            st.session_state.admin_authenticated = False
            st.rerun()
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
            user_avatar_upload = st.file_uploader(
                "Imagem do usuário",
                type=["png", "jpg", "jpeg", "webp"],
                key=f"avatar{uv}",
                help="A imagem será recortada automaticamente e exibida dentro do círculo do usuário.",
            )

            clear_top = st.checkbox("Remover logo superior e usar texto Setta")
            clear_footer = st.checkbox("Usar logo inferior padrão")
            clear_hero = st.checkbox("Usar imagem principal padrão")
            clear_user_avatar = st.checkbox("Remover imagem do usuário e usar ícone padrão")

            if cfg.get("logo_top"):
                st.caption("Logo superior atual")
                st.image(cfg["logo_top"], width=150)

            if cfg.get("user_avatar"):
                st.caption("Imagem atual do usuário")
                st.image(cfg["user_avatar"], width=72)

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

                if clear_user_avatar:
                    new_cfg["user_avatar"] = ""
                elif user_avatar_upload:
                    new_cfg["user_avatar"] = user_avatar_image(user_avatar_upload)

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
html,body,[data-testid="stAppViewContainer"]{min-height:100%;width:100%;max-width:100%;overflow-x:hidden}
.stApp{background:linear-gradient(180deg,#fff,#F8FAFD)}

header[data-testid="stHeader"]{
  position:fixed!important;
  top:0!important;
  left:0!important;
  right:0!important;
  width:100vw!important;
  max-width:none!important;
  margin:0!important;
  border-radius:0!important;
  background:var(--y)!important;
  height:64px!important;
  border-bottom:1px solid rgba(0,0,0,.06)!important;
  z-index:100000!important;
}
header[data-testid="stHeader"] *{color:var(--ink)!important}
[data-testid="stToolbar"]{background:transparent!important}
[data-testid="stDecoration"],footer{display:none!important}
#MainMenu,
span[data-testid="stMainMenu"]{
  display:flex!important;
  visibility:visible!important;
  pointer-events:auto!important;
}
span[data-testid="stMainMenu"] button{
  color:var(--ink)!important;
}
span[data-testid="stMainMenu"] svg{
  fill:var(--ink)!important;
  color:var(--ink)!important;
}
/* Remove somente o botão Share do toolbar do Community Cloud */
[data-testid="stToolbarActions"] > [data-testid="stToolbarActionButton"]:first-child,
.stToolbarActions > .stToolbarActionButton:first-child{
  display:none!important;
}
[data-testid="stSidebar"]{border-right:1px solid var(--line)!important;background:#fff!important;z-index:100005!important}
[data-testid="stSidebar"]>div:first-child{background:#fff!important}
.block-container{max-width:100%!important;padding:0!important;margin:0!important}

.hub-header-content{
  position:fixed;
  top:0;
  left:0;
  right:auto;
  width:100vw;
  max-width:none;
  height:64px;
  display:flex;
  align-items:center;
  padding:0 0 0 clamp(62px,4vw,78px);
  z-index:100002;
  pointer-events:none;
}

.page-root{
  padding-top:64px;
  min-height:100dvh;
  display:flex;
  flex-direction:column;
}

.brand-slot{width:170px;height:50px;display:flex;align-items:center;overflow:hidden}
.brand-text{color:var(--ink);font-size:clamp(34px,2.2vw,40px);font-style:italic;font-weight:900;letter-spacing:-3px}
.brand-logo{width:170px;height:48px;max-width:170px;max-height:48px;object-fit:contain;object-position:left center}
.user{position:absolute;top:50%;right:clamp(175px,12vw,230px);transform:translateY(-50%);color:var(--ink);font-size:clamp(13px,.85vw,15px);font-weight:700;display:flex;gap:8px;align-items:center;white-space:nowrap;line-height:1}
.user-badge{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#fff;border:1px solid rgba(30,35,46,.16);box-shadow:0 2px 8px rgba(20,35,58,.08);flex:0 0 32px;overflow:hidden}
.user-badge svg{display:block;width:18px;height:18px;min-width:18px;min-height:18px;fill:#23324A;stroke:none}
.user-badge img{display:block;width:100%;height:100%;object-fit:cover;object-position:center;border-radius:50%}

/* Botão nativo do Streamlit Community Cloud: Gerenciar aplicativo */
[data-testid="manage_app_button"],
button[data-testid="manage_app_button"],
[class*="viewerBadge"] button,
[class*="viewerBadge"] a{
  background:var(--y)!important;
  color:var(--ink)!important;
  border-color:#DFA817!important;
  box-shadow:0 4px 12px rgba(31,45,73,.12)!important;
}
[data-testid="manage_app_button"] *,
button[data-testid="manage_app_button"] *,
[class*="viewerBadge"] button *,
[class*="viewerBadge"] a *{
  color:var(--ink)!important;
  fill:var(--ink)!important;
  stroke:var(--ink)!important;
}

/* Login administrativo com a mesma linguagem visual do SETTA HUB */
[data-testid="stSidebar"] .admin-login-head{
  margin:8px 0 14px;
  padding:18px 16px 16px;
  border:1px solid #E4EAF2;
  border-radius:16px;
  background:linear-gradient(180deg,#FFFFFF 0%,#FBFCFE 100%);
  box-shadow:0 8px 22px rgba(31,45,73,.06);
}
[data-testid="stSidebar"] .admin-login-kicker{
  display:inline-flex;
  align-items:center;
  gap:7px;
  padding:6px 9px;
  border-radius:999px;
  background:#FFF7E2;
  color:#8D6200;
  font-size:10px;
  font-weight:800;
  letter-spacing:1.2px;
}
[data-testid="stSidebar"] .admin-login-title{
  margin-top:13px;
  color:#13203B;
  font-size:24px;
  line-height:1.08;
  font-weight:900;
  letter-spacing:-.4px;
}
[data-testid="stSidebar"] .admin-login-subtitle{
  margin-top:8px;
  color:#6C7891;
  font-size:13px;
  line-height:1.5;
}
[data-testid="stSidebar"] .admin-login-accent{
  width:54px;
  height:4px;
  margin-top:14px;
  border-radius:999px;
  background:var(--y2);
}
[data-testid="stSidebar"] .admin-login-note{
  margin-top:12px;
  padding:10px 12px;
  border:1px dashed #D7E0EC;
  border-radius:12px;
  background:#F8FAFD;
  color:#72809A;
  font-size:11px;
  line-height:1.45;
}
[data-testid="stSidebar"] [data-testid="stForm"]{
  border:1px solid #E4EAF2;
  border-radius:16px;
  padding:14px;
  background:#FFFFFF;
  box-shadow:0 6px 18px rgba(31,45,73,.04);
}
[data-testid="stSidebar"] .stTextInput label{
  color:#13203B!important;
  font-weight:700!important;
}
[data-testid="stSidebar"] .stTextInput input{
  min-height:44px!important;
  border:1px solid #D7E0EC!important;
  border-radius:11px!important;
  background:#F8FAFD!important;
  color:#13203B!important;
  box-shadow:none!important;
}
[data-testid="stSidebar"] .stTextInput input:focus{
  border-color:#E5AA13!important;
  box-shadow:0 0 0 1px #E5AA13!important;
}
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"],
[data-testid="stSidebar"] button[kind="primary"]{
  min-height:44px!important;
  border:1px solid #DFA817!important;
  border-radius:11px!important;
  background:var(--y)!important;
  color:#13203B!important;
  font-weight:800!important;
  box-shadow:none!important;
}
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"]:hover,
[data-testid="stSidebar"] button[kind="primary"]:hover{
  background:#F7BD2A!important;
  border-color:#D39B09!important;
  color:#13203B!important;
}

.hero{
  display:grid;
  grid-template-columns:minmax(0,.95fr) minmax(420px,1.05fr);
  gap:clamp(24px,2.2vw,40px);
  padding:clamp(22px,2.4vw,34px) var(--page-pad) clamp(16px,1.8vw,26px);
  background:#fff;
  align-items:center;
}
.hero-copy{padding:0;background:transparent;align-self:center}
.hero-eyebrow{margin-bottom:8px;color:#73809B;font-size:clamp(10px,.66vw,12px);font-weight:800;letter-spacing:4px;text-transform:uppercase}
.hero h1{margin:0;color:var(--ink);font-size:clamp(34px,2.55vw,46px);line-height:1.02;letter-spacing:-2px;font-weight:900}
.hero h2{margin:7px 0 0;color:#66728B;font-size:clamp(19px,1.42vw,25px);line-height:1.2;font-weight:500}
.hero p{margin:clamp(12px,1vw,16px) 0 0;color:#73809B;font-size:clamp(12px,.84vw,14px);line-height:1.55;max-width:560px}
.hero-accent{width:64px;height:4px;background:var(--y2);border-radius:10px;margin-top:16px}
.hero-image{height:clamp(185px,21vh,225px);min-height:185px;background-size:cover;background-position:center 48%;position:relative;border-radius:12px;overflow:hidden;box-shadow:0 8px 24px rgba(27,41,68,.08)}
.hero-image:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,transparent 48%,rgba(9,21,45,.08) 100%);pointer-events:none}
.hero-slogan{position:absolute;right:5%;bottom:18px;max-width:190px;color:white;text-shadow:0 1px 8px rgba(0,0,0,.35);font-size:clamp(11px,.75vw,13px);letter-spacing:1px;line-height:1.25;font-weight:800;z-index:2}
.hero-slogan:after{content:"";display:block;width:34px;height:3px;background:var(--y2);margin-top:9px;border-radius:8px}

.apps-wrap{width:100%;padding:clamp(8px,.8vw,12px) var(--page-pad) clamp(14px,1.3vw,22px);position:relative;z-index:5;flex:1 0 auto}
.apps-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(12px,1vw,18px)}
.app-card{position:relative;min-height:150px;display:flex;flex-direction:column;justify-content:space-between;text-decoration:none!important;color:inherit!important;background:radial-gradient(circle at 108% 112%,rgba(253,195,59,.13) 0 28%,transparent 29%),#fff;border:1px solid var(--line);border-radius:15px;padding:20px 22px 17px;box-shadow:0 6px 18px rgba(44,62,92,.045);transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease}
.app-card:hover{transform:translateY(-3px);box-shadow:0 12px 26px rgba(44,62,92,.10);border-color:#D9DEE7}
.card-content{display:grid;grid-template-columns:64px minmax(0,1fr);gap:16px;align-items:start;padding-right:90px}
.app-icon{width:64px;height:64px;border-radius:14px;display:flex;align-items:center;justify-content:center;background:#FFF7E2;overflow:hidden;flex:0 0 64px}
.app-icon img{width:50px;height:50px;object-fit:contain}
.app-icon-emoji{font-size:32px}
.card-copy{min-width:0;padding-top:4px}
.status{position:absolute;top:18px;right:20px;display:flex;align-items:center;gap:7px;background:#E9F9EF;color:#15883F;font-size:clamp(10px,.7vw,12px);font-weight:700;border-radius:999px;padding:6px 10px;white-space:nowrap}
.dot{width:9px;height:9px;border-radius:50%;background:var(--green);flex:0 0 9px}
.app-title{color:#111A36;font-weight:900;font-size:clamp(18px,1.08vw,21px);line-height:1.16}
.app-desc{margin-top:5px;color:#71809B;font-size:clamp(12px,.78vw,14px);line-height:1.35;max-width:95%}
.access{margin-top:14px;color:#F1A000;font-size:clamp(13px,.82vw,15px);font-weight:800;display:flex;align-items:center;gap:8px}
.access-arrow{font-size:18px;line-height:1;transition:transform .18s ease}
.app-card:hover .access-arrow{transform:translateX(3px)}

.page-footer{min-height:40px;border-top:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 var(--page-pad);background:#fff;color:#97A2B8;font-size:clamp(8px,.58vw,10px);letter-spacing:1.8px;text-transform:uppercase;margin-top:auto}
.footer-brand{display:flex;align-items:center;gap:10px;min-width:0}
.footer-logo-slot{width:64px;height:24px;display:flex;align-items:center;flex:0 0 64px}
.footer-brand-text{color:var(--ink);font-size:18px;font-style:italic;font-weight:900}
.footer-logo{width:64px;height:24px;object-fit:contain}
.footer-line{width:28px;height:3px;background:var(--y2);display:inline-block;margin-left:9px}

@media (min-width:1200px) and (max-height:900px){
  header[data-testid="stHeader"]{height:58px!important}
  .hub-header-content{height:58px}
  .page-root{padding-top:58px}
  .brand-slot{height:46px}
  .brand-logo{height:43px;max-height:43px}
  .brand-text{font-size:34px}
  .user-badge{width:30px;height:30px;flex-basis:30px}
  .user-badge svg{width:17px;height:17px;min-width:17px;min-height:17px}
  .user{font-size:12px}
  .hero{padding-top:18px;padding-bottom:12px}
  .hero-image{height:178px;min-height:178px}
  .hero h1{font-size:36px}
  .hero h2{font-size:20px}
  .hero p{font-size:12px;margin-top:10px}
  .hero-accent{margin-top:12px;height:3px}
  .apps-wrap{padding-top:6px;padding-bottom:10px}
  .apps-grid{gap:12px}
  .app-card{min-height:140px;padding:16px 18px 14px}
  .card-content{grid-template-columns:58px minmax(0,1fr);gap:13px;padding-right:82px}
  .app-icon{width:58px;height:58px;flex-basis:58px}
  .app-icon img{width:46px;height:46px}
  .app-title{font-size:18px}
  .app-desc{font-size:12px}
  .status{top:15px;right:16px;padding:5px 9px}
  .access{margin-top:10px;font-size:13px}
  .page-footer{min-height:34px}
  .footer-logo-slot{height:20px}
  .footer-logo{height:20px}
  .footer-brand-text{font-size:16px}
}
@media (max-width:1320px){
  :root{--page-pad:clamp(20px,3vw,42px)}
  .user{right:165px}
  .hero{grid-template-columns:minmax(0,.95fr) minmax(380px,1.05fr);gap:22px}
  .app-card{padding-left:18px;padding-right:18px}
  .card-content{padding-right:78px}
}
@media (max-width:1120px){
  .apps-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .user{display:none}
  .hero{grid-template-columns:1fr 1fr}
  .hero h1{font-size:36px}
}
@media (max-width:820px){
  .hero{grid-template-columns:1fr;gap:18px}
  .hero-image{height:190px}
}
@media (max-width:760px){
  header[data-testid="stHeader"]{height:62px!important}
  .hub-header-content{height:62px;padding:0 20px 0 62px}
  .page-root{padding-top:62px;min-height:100dvh}
  .brand-slot{width:145px;height:48px}
  .brand-logo{width:145px;height:44px}
  .brand-text{font-size:34px}
  .hero{grid-template-columns:1fr;padding:28px 20px 16px}
  .hero h1{font-size:32px}
  .hero h2{font-size:19px}
  .hero-image{height:180px;min-height:180px}
  .apps-wrap{padding:12px 18px 18px}
  .apps-grid{grid-template-columns:1fr}
  .app-card{min-height:145px;padding:18px}
  .card-content{grid-template-columns:60px minmax(0,1fr);padding-right:70px}
  .app-icon{width:60px;height:60px;flex-basis:60px}
  .app-icon img{width:48px;height:48px}
  .page-footer{flex-direction:column;gap:8px;padding:10px 18px;text-align:center}
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

user_avatar_html = (
    f'<img src="{cfg["user_avatar"]}" alt="Usuário">'
    if cfg.get("user_avatar")
    else '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="8" r="4"></circle><path d="M4.5 20c.45-4.05 3.18-6.2 7.5-6.2s7.05 2.15 7.5 6.2H4.5z"></path></svg>'
)


def icon_html(app):
    if app.get("icone_png"):
        return f'<img src="{app.get("icone_png")}" alt="Ícone">'
    return f'<span class="app-icon-emoji">{esc(app.get("icone", "🔗"))}</span>'


cards = ""
for app in cfg["apps"]:
    cards += (
        f'<a class="app-card" href="{esc(safe_url(app.get("url", "#")))}" target="_blank" rel="noopener noreferrer">'
        f'<div class="card-content">'
        f'<div class="app-icon">{icon_html(app)}</div>'
        f'<div class="card-copy"><div class="app-title">{esc(app.get("nome", "Aplicativo"))}</div>'
        f'<div class="app-desc">{esc(app.get("descricao", ""))}</div></div></div>'
        f'<div class="status"><span class="dot"></span>{esc(app.get("status", "Ativo"))}</div>'
        f'<div class="access">Acessar <span class="access-arrow">→</span></div></a>'
    )

page = (
    f'<div class="hub-header-content"><div class="brand-slot">{logo_top}</div>'
    f'<div class="user"><div class="user-badge">{user_avatar_html}</div><span>{esc(cfg["usuario"])}</span></div></div>'
    f'<div class="page-root"><section class="hero"><div class="hero-copy">'
    f'<div class="hero-eyebrow">BEM-VINDO(A) AO</div>'
    f'<h1>{esc(cfg["titulo"])}</h1><h2>{esc(cfg["subtitulo"])}</h2>'
    f'<p>{esc(cfg["descricao"]).replace(chr(10), "<br>")}</p><div class="hero-accent"></div></div>'
    f'<div class="hero-image" style="background-image:url(\'{esc(cfg["hero_image"])}\')">'
    f'<div class="hero-slogan">{esc(cfg["slogan"]).replace(chr(10), "<br>")}</div></div></section>'
    f'<div class="apps-wrap"><div class="apps-grid">{cards}</div></div>'
    f'<div class="page-footer"><div class="footer-brand"><div class="footer-logo-slot">{logo_footer}</div>'
    f'<span>|</span><span>{esc(cfg["rodape_esquerdo"])}</span></div>'
    f'<div>{esc(cfg["rodape_direito"])}<span class="footer-line"></span></div></div></div>'
)

st.html(page)
