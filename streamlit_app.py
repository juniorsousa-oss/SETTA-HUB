import base64, copy, html
from urllib.parse import urlparse
import streamlit as st

st.set_page_config(page_title="SETTA HUB | Central de Aplicativos", page_icon="🟨", layout="wide", initial_sidebar_state="expanded")

DEFAULT_CONFIG={
"logo_top":"","logo_footer":"",
"hero_image":"https://gruposetta.com.br/wp-content/uploads/2026/03/entradaG9.jpg-2-1-scaled-e1774901671839.png",
"titulo":"CENTRAL DE APLICATIVOS","subtitulo":"Acesso rápido aos sistemas operacionais",
"descricao":"Soluções integradas que impulsionam a eficiência,\nconectam pessoas e constroem grandes resultados.",
"slogan":"TECNOLOGIA\nQUE CONSTRÓI\nO AMANHÃ","usuario":"Olá, Usuário",
"rodape_esquerdo":"TECNOLOGIA A SERVIÇO DE GRANDES RESULTADOS","rodape_direito":"JUNTOS, CONSTRUÍMOS O AMANHÃ",
"apps":[
{"nome":"Gestão Almoxarifado","descricao":"Gestão completa da operação","icone":"📦","status":"Online","url":"#"},
{"nome":"Dashboard Operacional","descricao":"Indicadores e resultados","icone":"📊","status":"Online","url":"#"},
{"nome":"MRP","descricao":"Demanda e necessidade de materiais","icone":"📋","status":"Ativo","url":"#"},
{"nome":"Entregas","descricao":"Controle de OPs e cronograma","icone":"🚚","status":"Online","url":"#"},
{"nome":"Compra Fácil","descricao":"Compras e histórico de preços","icone":"🛒","status":"Ativo","url":"#"},
{"nome":"Gestão de Equipe","descricao":"Colaboradores e plano de carreira","icone":"👥","status":"Online","url":"#"}]}

if "hub_config" not in st.session_state: st.session_state.hub_config=copy.deepcopy(DEFAULT_CONFIG)
if "upload_version" not in st.session_state: st.session_state.upload_version=0

def data_uri(f):
    if f is None:return ""
    return f"data:{f.type or 'image/png'};base64,{base64.b64encode(f.getvalue()).decode()}"

def safe_url(v):
    v=(v or "").strip()
    if not v or v=="#": return "#"
    p=urlparse(v)
    return v if p.scheme in {"http","https"} and p.netloc else "#"

def esc(v): return html.escape(str(v or ""),quote=True)

cfg=st.session_state.hub_config; uv=st.session_state.upload_version
with st.sidebar:
    st.title("⚙️ Configurações")
    st.caption("Personalize o SETTA HUB sem alterar as dimensões do layout.")
    with st.form("hub_settings_form"):
        st.subheader("Identidade visual")
        lt=st.file_uploader("Logo superior",type=["png","jpg","jpeg","webp"],key=f"lt_{uv}")
        lf=st.file_uploader("Logo inferior",type=["png","jpg","jpeg","webp"],key=f"lf_{uv}")
        hi=st.file_uploader("Imagem principal",type=["png","jpg","jpeg","webp"],key=f"hi_{uv}")
        dlt=st.checkbox("Usar logo superior padrão"); dlf=st.checkbox("Usar logo inferior padrão"); dhi=st.checkbox("Usar imagem principal padrão")
        st.divider(); st.subheader("Textos da página")
        titulo=st.text_input("Título",cfg["titulo"]); subtitulo=st.text_input("Subtítulo",cfg["subtitulo"])
        descricao=st.text_area("Descrição",cfg["descricao"],height=90); slogan=st.text_area("Texto sobre a imagem",cfg["slogan"],height=90)
        usuario=st.text_input("Usuário do cabeçalho",cfg["usuario"]); re=st.text_input("Texto inferior esquerdo",cfg["rodape_esquerdo"]); rd=st.text_input("Texto inferior direito",cfg["rodape_direito"])
        st.divider(); st.subheader("Cartões e redirecionamentos")
        apps=[]
        for i,a in enumerate(cfg["apps"]):
            with st.expander(f"{i+1}. {a['nome']}"):
                apps.append({"nome":st.text_input("Nome do cartão",a["nome"],key=f"n{i}_{uv}"),"descricao":st.text_input("Descrição",a["descricao"],key=f"d{i}_{uv}"),"icone":st.text_input("Ícone",a["icone"],key=f"ic{i}_{uv}"),"status":st.text_input("Status",a["status"],key=f"s{i}_{uv}"),"url":st.text_input("Link de destino",a["url"],key=f"u{i}_{uv}",placeholder="https://seu-app.streamlit.app")})
        apply=st.form_submit_button("Aplicar alterações",use_container_width=True)
    if apply:
        n=copy.deepcopy(cfg)
        if dlt:n["logo_top"]=""
        elif lt:n["logo_top"]=data_uri(lt)
        if dlf:n["logo_footer"]=""
        elif lf:n["logo_footer"]=data_uri(lf)
        if dhi:n["hero_image"]=DEFAULT_CONFIG["hero_image"]
        elif hi:n["hero_image"]=data_uri(hi)
        n.update(titulo=titulo,subtitulo=subtitulo,descricao=descricao,slogan=slogan,usuario=usuario,rodape_esquerdo=re,rodape_direito=rd,apps=apps)
        st.session_state.hub_config=n; st.rerun()
    if st.button("Restaurar tudo ao padrão",use_container_width=True):
        st.session_state.hub_config=copy.deepcopy(DEFAULT_CONFIG); st.session_state.upload_version+=1; st.rerun()

cfg=st.session_state.hub_config
st.html('''<style>
:root{--y:#FDC33B;--y2:#F9B719;--ink:#1E232E;--line:#E7EBF1;--green:#0FAF4D}.stApp{background:linear-gradient(180deg,#fff 0%,#F8FAFD 100%)}
header[data-testid="stHeader"]{background:transparent!important;height:64px!important;z-index:99999!important;pointer-events:none!important}
[data-testid="stToolbar"],[data-testid="stDecoration"],#MainMenu,footer{display:none!important}
[data-testid="stSidebarCollapsedControl"],[data-testid="collapsedControl"]{display:flex!important;visibility:visible!important;opacity:1!important;position:fixed!important;top:20px!important;left:18px!important;z-index:100001!important;width:38px!important;height:38px!important;min-width:38px!important;align-items:center!important;justify-content:center!important;background:#fff!important;border:1px solid rgba(30,35,46,.14)!important;border-radius:10px!important;box-shadow:0 4px 14px rgba(30,35,46,.14)!important;pointer-events:auto!important}
[data-testid="stSidebarCollapsedControl"] button,[data-testid="collapsedControl"] button{pointer-events:auto!important}
[data-testid="stSidebar"]{border-right:1px solid var(--line)!important;background:#fff!important;z-index:100002!important}[data-testid="stSidebar"]>div:first-child{background:#fff!important}
.block-container{max-width:100%!important;padding:0!important;margin:0!important}.topbar{height:82px;background:linear-gradient(90deg,var(--y),#FFC83E 62%,var(--y));display:flex;align-items:center;justify-content:space-between;padding:0 5% 0 calc(5% + 46px);border-bottom:1px solid rgba(0,0,0,.05)}
.brand-slot{width:165px;height:58px;display:flex;align-items:center;overflow:hidden}.brand-text{color:var(--ink);font-size:43px;font-style:italic;font-weight:900;letter-spacing:-3px;white-space:nowrap}.brand-logo{width:165px;height:58px;object-fit:contain;object-position:left center}.user{color:var(--ink);font-size:15px;font-weight:700;display:flex;gap:10px;align-items:center}.user-badge{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:#fff;border:1px solid rgba(30,35,46,.2)}
.hero{display:grid;grid-template-columns:1.02fr 1fr;min-height:290px;background:#fff;overflow:hidden}.hero-copy{padding:62px 5% 44px;z-index:2;background:linear-gradient(120deg,#fff 0%,#fff 72%,rgba(255,255,255,.92) 78%,rgba(255,255,255,0) 79%)}.hero h1{margin:0;color:var(--ink);font-size:48px;line-height:1.03;letter-spacing:-2px;font-weight:900}.hero h2{margin:8px 0 0;color:#66728B;font-size:27px;font-weight:500}.hero p{margin:20px 0 0;color:#73809B;font-size:16px;line-height:1.55;max-width:600px}.hero-image{min-height:290px;background-size:cover;background-position:center;position:relative}.hero-image:before{content:"";position:absolute;left:-70px;top:0;width:120px;height:100%;transform:skewX(-25deg);background:linear-gradient(180deg,rgba(253,195,59,.16),rgba(255,255,255,.8));z-index:1}.hero-slogan{position:absolute;right:7%;top:38px;color:#60708F;font-size:12px;letter-spacing:4px;line-height:1.7;font-weight:700;z-index:2}.hero-slogan:after{content:"";display:block;width:42px;height:3px;border-radius:6px;background:var(--y2);margin-top:8px}
.apps-wrap{padding:0 4% 28px;margin-top:-10px;position:relative;z-index:5}.apps-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.app-card{min-height:190px;display:flex;flex-direction:column;justify-content:space-between;text-decoration:none!important;color:inherit!important;background:radial-gradient(circle at 108% 110%,rgba(253,195,59,.16) 0 27%,transparent 28%),#fff;border:1px solid var(--line);border-radius:16px;padding:24px 30px 22px;box-shadow:0 8px 24px rgba(44,62,92,.06);transition:.18s}.app-card:hover{transform:translateY(-4px);box-shadow:0 16px 34px rgba(44,62,92,.12)}.card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}.app-icon{width:66px;height:66px;border-radius:15px;display:grid;place-items:center;font-size:34px;background:#FFF7E2}.status{display:flex;align-items:center;gap:7px;background:#E9F9EF;color:#15883F;font-size:13px;font-weight:700;border-radius:999px;padding:7px 12px}.dot{width:10px;height:10px;border-radius:50%;background:var(--green)}.app-title{margin-top:10px;color:#101738;font-weight:900;font-size:24px}.app-desc{margin-top:4px;color:#77839B;font-size:15px}.access{margin-top:20px;color:#F1A000;font-size:16px;font-weight:800;display:flex;gap:10px}.arrow{font-size:22px}
.page-footer{min-height:62px;border-top:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 4%;background:#fff;color:#97A2B8;font-size:11px;letter-spacing:2px;text-transform:uppercase}.footer-brand{display:flex;align-items:center;gap:12px}.footer-logo-slot{width:72px;height:30px;display:flex;align-items:center;overflow:hidden}.footer-brand-text{color:var(--ink);font-size:21px;font-style:italic;font-weight:900;letter-spacing:-1px;text-transform:none}.footer-logo{width:72px;height:30px;object-fit:contain;object-position:left center}.footer-line{width:32px;height:3px;border-radius:4px;background:var(--y2);display:inline-block;margin-left:10px}
@media(max-width:1100px){.hero h1{font-size:40px}.hero h2{font-size:23px}.apps-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:760px){header[data-testid="stHeader"]{height:58px!important}[data-testid="stSidebarCollapsedControl"],[data-testid="collapsedControl"]{top:15px!important;left:12px!important}.topbar{height:70px;padding:0 20px 0 64px}.brand-slot,.brand-logo{width:140px;height:50px}.brand-text{font-size:35px}.user span:last-child{display:none}.hero{grid-template-columns:1fr}.hero-copy{padding:38px 22px 32px;background:#fff}.hero h1{font-size:34px}.hero h2{font-size:20px}.hero p{font-size:14px}.hero-image{min-height:190px}.apps-wrap{padding:18px 18px 28px;margin-top:0}.apps-grid{grid-template-columns:1fr}.app-card{min-height:175px;padding:22px}.page-footer{flex-direction:column;gap:10px;justify-content:center;text-align:center;padding:16px 18px}.footer-brand{justify-content:center;flex-wrap:wrap}}
</style>''')

lt=f'<img class="brand-logo" src="{cfg["logo_top"]}" alt="Logo superior">' if cfg["logo_top"] else '<div class="brand-text">Setta</div>'
lf=f'<img class="footer-logo" src="{cfg["logo_footer"]}" alt="Logo inferior">' if cfg["logo_footer"] else '<div class="footer-brand-text">Setta</div>'
dh=esc(cfg["descricao"]).replace("\n","<br>"); sh=esc(cfg["slogan"]).replace("\n","<br>")
cards=""
for a in cfg["apps"]:
    cards+=f'''<a class="app-card" href="{esc(safe_url(a['url']))}" target="_blank" rel="noopener noreferrer"><div><div class="card-top"><div class="app-icon">{esc(a['icone'])}</div><div class="status"><span class="dot"></span>{esc(a['status'])}</div></div><div class="app-title">{esc(a['nome'])}</div><div class="app-desc">{esc(a['descricao'])}</div></div><div class="access">Acessar <span class="arrow">→</span></div></a>'''

page=f'''<div class="topbar"><div class="brand-slot">{lt}</div><div class="user"><div class="user-badge">●</div><span>{esc(cfg['usuario'])}</span><span>⌄</span></div></div><section class="hero"><div class="hero-copy"><h1>{esc(cfg['titulo'])}</h1><h2>{esc(cfg['subtitulo'])}</h2><p>{dh}</p></div><div class="hero-image" style="background-image:url('{esc(cfg['hero_image'])}');"><div class="hero-slogan">{sh}</div></div></section><div class="apps-wrap"><div class="apps-grid">{cards}</div></div><div class="page-footer"><div class="footer-brand"><div class="footer-logo-slot">{lf}</div><span>|</span><span>{esc(cfg['rodape_esquerdo'])}</span></div><div>{esc(cfg['rodape_direito'])}<span class="footer-line"></span></div></div>'''
st.html(page)
