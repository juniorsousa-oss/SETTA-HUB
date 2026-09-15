import base64, copy, html
from datetime import datetime, timezone
from urllib.parse import urlparse
import requests, streamlit as st

st.set_page_config(page_title="SETTA HUB | Central de Aplicativos", page_icon="🟨", layout="wide", initial_sidebar_state="expanded")

SB_URL="https://cuixazpxkvniqldmmnth.supabase.co"
SB_KEY="sb_publishable_ZTqIgmA9Ez6AVQsoXa0P8Q_6CYHDFye"
SB_TABLE="setta_hub_config"
SB_ID="main"

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

def headers(extra=None):
    h={"apikey":SB_KEY,"Authorization":f"Bearer {SB_KEY}","Content-Type":"application/json"}
    if extra:h.update(extra)
    return h

def merge(saved):
    c=copy.deepcopy(DEFAULT_CONFIG)
    if not isinstance(saved,dict):return c
    for k in ("logo_top","logo_footer","hero_image","titulo","subtitulo","descricao","slogan","usuario","rodape_esquerdo","rodape_direito"):
        if k in saved:c[k]=saved[k]
    if isinstance(saved.get("apps"),list) and saved["apps"]:c["apps"]=saved["apps"]
    return c

def load_db():
    r=requests.get(f"{SB_URL}/rest/v1/{SB_TABLE}",headers=headers(),params={"id":f"eq.{SB_ID}","select":"config","limit":"1"},timeout=12)
    r.raise_for_status(); rows=r.json()
    if rows:return merge(rows[0].get("config"))
    save_db(DEFAULT_CONFIG); return copy.deepcopy(DEFAULT_CONFIG)

def save_db(cfg):
    payload={"id":SB_ID,"config":cfg,"updated_at":datetime.now(timezone.utc).isoformat()}
    r=requests.post(f"{SB_URL}/rest/v1/{SB_TABLE}",headers=headers({"Prefer":"resolution=merge-duplicates,return=minimal"}),params={"on_conflict":"id"},json=payload,timeout=20)
    r.raise_for_status()

def data_uri(f,max_mb=4):
    if f is None:return ""
    if f.size>max_mb*1024*1024:raise ValueError(f"A imagem deve ter no máximo {max_mb} MB.")
    return f"data:{f.type or 'image/png'};base64,{base64.b64encode(f.getvalue()).decode()}"

def safe_url(v):
    v=(v or "").strip()
    if not v or v=="#":return "#"
    p=urlparse(v); return v if p.scheme in {"http","https"} and p.netloc else "#"

def esc(v):return html.escape(str(v or ""),quote=True)

if "hub_config" not in st.session_state:
    try:
        st.session_state.hub_config=load_db(); st.session_state.db_ok=True
    except Exception:
        st.session_state.hub_config=copy.deepcopy(DEFAULT_CONFIG); st.session_state.db_ok=False
if "upload_version" not in st.session_state:st.session_state.upload_version=0
if "save_notice" not in st.session_state:st.session_state.save_notice=""
cfg=st.session_state.hub_config; uv=st.session_state.upload_version

with st.sidebar:
    st.title("⚙️ Configurações")
    st.success("Salvamento permanente ativo") if st.session_state.get("db_ok") else st.warning("Modo temporário: banco indisponível")
    if st.session_state.get("save_notice"):
        st.info(st.session_state.save_notice); st.session_state.save_notice=""
    st.caption("As alterações ficam salvas no Supabase, inclusive após atualizar ou reiniciar o app.")
    with st.form("hub_settings_form"):
        st.subheader("Identidade visual")
        lt=st.file_uploader("Logo superior",type=["png","jpg","jpeg","webp"],key=f"lt_{uv}")
        lf=st.file_uploader("Logo inferior",type=["png","jpg","jpeg","webp"],key=f"lf_{uv}")
        hi=st.file_uploader("Imagem principal",type=["png","jpg","jpeg","webp"],key=f"hi_{uv}",help="Limite: 4 MB.")
        dlt=st.checkbox("Usar logo superior padrão"); dlf=st.checkbox("Usar logo inferior padrão"); dhi=st.checkbox("Usar imagem principal padrão")
        st.divider(); st.subheader("Textos da página")
        titulo=st.text_input("Título",cfg["titulo"]); subtitulo=st.text_input("Subtítulo",cfg["subtitulo"])
        descricao=st.text_area("Descrição",cfg["descricao"],height=90); slogan=st.text_area("Texto sobre a imagem",cfg["slogan"],height=90)
        usuario=st.text_input("Usuário do cabeçalho",cfg["usuario"]); re=st.text_input("Texto inferior esquerdo",cfg["rodape_esquerdo"]); rd=st.text_input("Texto inferior direito",cfg["rodape_direito"])
        st.divider(); st.subheader("Cartões e redirecionamentos")
        apps=[]
        for i,a in enumerate(cfg["apps"]):
            with st.expander(f"{i+1}. {a.get('nome','Aplicativo')}"):
                apps.append({"nome":st.text_input("Nome do cartão",a.get("nome",""),key=f"n{i}_{uv}"),"descricao":st.text_input("Descrição",a.get("descricao",""),key=f"d{i}_{uv}"),"icone":st.text_input("Ícone",a.get("icone","🔗"),key=f"ic{i}_{uv}"),"status":st.text_input("Status",a.get("status","Ativo"),key=f"s{i}_{uv}"),"url":st.text_input("Link de destino",a.get("url","#"),key=f"u{i}_{uv}",placeholder="https://seu-app.streamlit.app")})
        apply=st.form_submit_button("Salvar alterações",use_container_width=True,type="primary")
    if apply:
        try:
            n=copy.deepcopy(cfg)
            if dlt:n["logo_top"]=""
            elif lt:n["logo_top"]=data_uri(lt)
            if dlf:n["logo_footer"]=""
            elif lf:n["logo_footer"]=data_uri(lf)
            if dhi:n["hero_image"]=DEFAULT_CONFIG["hero_image"]
            elif hi:n["hero_image"]=data_uri(hi)
            n.update(titulo=titulo,subtitulo=subtitulo,descricao=descricao,slogan=slogan,usuario=usuario,rodape_esquerdo=re,rodape_direito=rd,apps=apps)
            save_db(n); st.session_state.hub_config=n; st.session_state.db_ok=True; st.session_state.save_notice="Alterações salvas permanentemente."; st.rerun()
        except Exception as e:st.error(f"Não foi possível salvar: {e}")
    if st.button("Recarregar do banco",use_container_width=True):
        try:
            st.session_state.hub_config=load_db(); st.session_state.upload_version+=1; st.session_state.db_ok=True; st.session_state.save_notice="Dados recarregados do Supabase."; st.rerun()
        except Exception as e:st.error(f"Não foi possível recarregar: {e}")
    if st.button("Restaurar tudo ao padrão",use_container_width=True):
        try:
            d=copy.deepcopy(DEFAULT_CONFIG); save_db(d); st.session_state.hub_config=d; st.session_state.upload_version+=1; st.session_state.db_ok=True; st.session_state.save_notice="Padrão restaurado e salvo."; st.rerun()
        except Exception as e:st.error(f"Não foi possível restaurar: {e}")

cfg=st.session_state.hub_config
st.html('''<style>
:root{--y:#FDC33B;--y2:#F9B719;--ink:#1E232E;--line:#E7EBF1;--green:#0FAF4D}.stApp{background:linear-gradient(180deg,#fff 0%,#F8FAFD 100%)}
header[data-testid="stHeader"]{background:var(--y)!important;height:76px!important;border-bottom:1px solid rgba(0,0,0,.06)!important;z-index:100000!important}header[data-testid="stHeader"] *{color:var(--ink)!important}[data-testid="stToolbar"]{background:transparent!important}[data-testid="stDecoration"],#MainMenu,footer{display:none!important}
[data-testid="stSidebar"]{border-right:1px solid var(--line)!important;background:#fff!important;z-index:100001!important}[data-testid="stSidebar"]>div:first-child{background:#fff!important}.block-container{max-width:100%!important;padding:0!important;margin:0!important}
.hub-header-content{position:fixed;top:0;left:0;right:0;height:76px;display:flex;align-items:center;justify-content:space-between;padding:0 220px 0 72px;z-index:99999;pointer-events:none;background:transparent}.page-root{padding-top:76px}.brand-slot{width:165px;height:58px;display:flex;align-items:center;overflow:hidden}.brand-text{color:var(--ink);font-size:43px;font-style:italic;font-weight:900;letter-spacing:-3px;white-space:nowrap}.brand-logo{width:165px;height:58px;object-fit:contain;object-position:left center}.user{color:var(--ink);font-size:15px;font-weight:700;display:flex;gap:10px;align-items:center}.user-badge{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:#fff;border:1px solid rgba(30,35,46,.2)}
.hero{display:grid;grid-template-columns:1.02fr 1fr;min-height:290px;background:#fff;overflow:hidden}.hero-copy{padding:62px 5% 44px;z-index:2;background:linear-gradient(120deg,#fff 0%,#fff 72%,rgba(255,255,255,.92) 78%,rgba(255,255,255,0) 79%)}.hero h1{margin:0;color:var(--ink);font-size:48px;line-height:1.03;letter-spacing:-2px;font-weight:900}.hero h2{margin:8px 0 0;color:#66728B;font-size:27px;font-weight:500}.hero p{margin:20px 0 0;color:#73809B;font-size:16px;line-height:1.55;max-width:600px}.hero-image{min-height:290px;background-size:cover;background-position:center;position:relative}.hero-image:before{content:"";position:absolute;left:-70px;top:0;width:120px;height:100%;transform:skewX(-25deg);background:linear-gradient(180deg,rgba(253,195,59,.16),rgba(255,255,255,.8));z-index:1}.hero-slogan{position:absolute;right:7%;top:38px;color:#60708F;font-size:12px;letter-spacing:4px;line-height:1.7;font-weight:700;z-index:2}.hero-slogan:after{content:"";display:block;width:42px;height:3px;border-radius:6px;background:var(--y2);margin-top:8px}
.apps-wrap{padding:0 4% 28px;margin-top:-10px;position:relative;z-index:5}.apps-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.app-card{min-height:190px;display:flex;flex-direction:column;justify-content:space-between;text-decoration:none!important;color:inherit!important;background:radial-gradient(circle at 108% 110%,rgba(253,195,59,.16) 0 27%,transparent 28%),#fff;border:1px solid var(--line);border-radius:16px;padding:24px 30px 22px;box-shadow:0 8px 24px rgba(44,62,92,.06);transition:.18s}.app-card:hover{transform:translateY(-4px);box-shadow:0 16px 34px rgba(44,62,92,.12)}.card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}.app-icon{width:66px;height:66px;border-radius:15px;display:grid;place-items:center;font-size:34px;background:#FFF7E2}.status{display:flex;align-items:center;gap:7px;background:#E9F9EF;color:#15883F;font-size:13px;font-weight:700;border-radius:999px;padding:7px 12px}.dot{width:10px;height:10px;border-radius:50%;background:var(--green)}.app-title{margin-top:10px;color:#101738;font-weight:900;font-size:24px}.app-desc{margin-top:4px;color:#77839B;font-size:15px}.access{margin-top:20px;color:#F1A000;font-size:16px;font-weight:800;display:flex;gap:10px}.arrow{font-size:22px}
.page-footer{min-height:62px;border-top:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 4%;background:#fff;color:#97A2B8;font-size:11px;letter-spacing:2px;text-transform:uppercase}.footer-brand{display:flex;align-items:center;gap:12px}.footer-logo-slot{width:72px;height:30px;display:flex;align-items:center;overflow:hidden}.footer-brand-text{color:var(--ink);font-size:21px;font-style:italic;font-weight:900;letter-spacing:-1px;text-transform:none}.footer-logo{width:72px;height:30px;object-fit:contain;object-position:left center}.footer-line{width:32px;height:3px;border-radius:4px;background:var(--y2);display:inline-block;margin-left:10px}
@media(max-width:1100px){.hero h1{font-size:40px}.hero h2{font-size:23px}.apps-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.user{display:none}.hub-header-content{padding-right:130px}}@media(max-width:760px){header[data-testid="stHeader"]{height:66px!important}.hub-header-content{height:66px;padding:0 20px 0 62px}.page-root{padding-top:66px}.brand-slot,.brand-logo{width:140px;height:50px}.brand-text{font-size:35px}.hero{grid-template-columns:1fr}.hero-copy{padding:38px 22px 32px;background:#fff}.hero h1{font-size:34px}.hero h2{font-size:20px}.hero p{font-size:14px}.hero-image{min-height:190px}.apps-wrap{padding:18px 18px 28px;margin-top:0}.apps-grid{grid-template-columns:1fr}.app-card{min-height:175px;padding:22px}.page-footer{flex-direction:column;gap:10px;justify-content:center;text-align:center;padding:16px 18px}.footer-brand{justify-content:center;flex-wrap:wrap}}
</style>''')
lt=f'<img class="brand-logo" src="{cfg["logo_top"]}" alt="Logo superior">' if cfg["logo_top"] else '<div class="brand-text">Setta</div>'
lf=f'<img class="footer-logo" src="{cfg["logo_footer"]}" alt="Logo inferior">' if cfg["logo_footer"] else '<div class="footer-brand-text">Setta</div>'
dh=esc(cfg["descricao"]).replace("\n","<br>"); sh=esc(cfg["slogan"]).replace("\n","<br>")
cards=""
for a in cfg["apps"]:
    cards+=f'''<a class="app-card" href="{esc(safe_url(a.get('url','#')))}" target="_blank" rel="noopener noreferrer"><div><div class="card-top"><div class="app-icon">{esc(a.get('icone','🔗'))}</div><div class="status"><span class="dot"></span>{esc(a.get('status','Ativo'))}</div></div><div class="app-title">{esc(a.get('nome','Aplicativo'))}</div><div class="app-desc">{esc(a.get('descricao',''))}</div></div><div class="access">Acessar <span class="arrow">→</span></div></a>'''
page=f'''<div class="hub-header-content"><div class="brand-slot">{lt}</div><div class="user"><div class="user-badge">●</div><span>{esc(cfg['usuario'])}</span><span>⌄</span></div></div><div class="page-root"><section class="hero"><div class="hero-copy"><h1>{esc(cfg['titulo'])}</h1><h2>{esc(cfg['subtitulo'])}</h2><p>{dh}</p></div><div class="hero-image" style="background-image:url('{esc(cfg['hero_image'])}');"><div class="hero-slogan">{sh}</div></div></section><div class="apps-wrap"><div class="apps-grid">{cards}</div></div><div class="page-footer"><div class="footer-brand"><div class="footer-logo-slot">{lf}</div><span>|</span><span>{esc(cfg['rodape_esquerdo'])}</span></div><div>{esc(cfg['rodape_direito'])}<span class="footer-line"></span></div></div></div>'''
st.html(page)
