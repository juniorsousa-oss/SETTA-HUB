import base64, copy, html
from datetime import datetime, timezone
from io import BytesIO
from urllib.parse import urlparse
import requests, streamlit as st
from PIL import Image

st.set_page_config(page_title="SETTA HUB | Central de Aplicativos",page_icon="🟨",layout="wide",initial_sidebar_state="expanded")
SB_URL="https://cuixazpxkvniqldmmnth.supabase.co"; SB_KEY="sb_publishable_ZTqIgmA9Ez6AVQsoXa0P8Q_6CYHDFye"; SB_TABLE="setta_hub_config"; SB_ID="main"
DEFAULT_CONFIG={"logo_top":"","logo_footer":"","hero_image":"https://gruposetta.com.br/wp-content/uploads/2026/03/entradaG9.jpg-2-1-scaled-e1774901671839.png","titulo":"CENTRAL DE APLICATIVOS","subtitulo":"Acesso rápido aos sistemas operacionais","descricao":"Soluções integradas que impulsionam a eficiência,\nconectam pessoas e constroem grandes resultados.","slogan":"TECNOLOGIA\nQUE CONSTRÓI\nO AMANHÃ","usuario":"Olá, Usuário","rodape_esquerdo":"TECNOLOGIA A SERVIÇO DE GRANDES RESULTADOS","rodape_direito":"JUNTOS, CONSTRUÍMOS O AMANHÃ","apps":[
{"nome":"Gestão Almoxarifado","descricao":"Gestão completa da operação","icone":"📦","icone_png":"","status":"Online","url":"#"},{"nome":"Dashboard Operacional","descricao":"Indicadores e resultados","icone":"📊","icone_png":"","status":"Online","url":"#"},{"nome":"MRP","descricao":"Demanda e necessidade de materiais","icone":"📋","icone_png":"","status":"Ativo","url":"#"},{"nome":"Entregas","descricao":"Controle de OPs e cronograma","icone":"🚚","icone_png":"","status":"Online","url":"#"},{"nome":"Compra Fácil","descricao":"Compras e histórico de preços","icone":"🛒","icone_png":"","status":"Ativo","url":"#"},{"nome":"Gestão de Equipe","descricao":"Colaboradores e plano de carreira","icone":"👥","icone_png":"","status":"Online","url":"#"}]}

def H(extra=None):
 h={"apikey":SB_KEY,"Authorization":f"Bearer {SB_KEY}","Content-Type":"application/json"}; h.update(extra or {}); return h

def merge(saved):
 c=copy.deepcopy(DEFAULT_CONFIG)
 if not isinstance(saved,dict): return c
 for k in ("logo_top","logo_footer","hero_image","titulo","subtitulo","descricao","slogan","usuario","rodape_esquerdo","rodape_direito"):
  if k in saved: c[k]=saved[k]
 if isinstance(saved.get("apps"),list) and saved["apps"]:
  c["apps"]=[]
  for x in saved["apps"]:
   a=dict(x) if isinstance(x,dict) else {}; a.setdefault("nome","Aplicativo"); a.setdefault("descricao",""); a.setdefault("icone","🔗"); a.setdefault("icone_png",""); a.setdefault("status","Ativo"); a.setdefault("url","#"); c["apps"].append(a)
 return c

def save_db(c):
 p={"id":SB_ID,"config":c,"updated_at":datetime.now(timezone.utc).isoformat()}; r=requests.post(f"{SB_URL}/rest/v1/{SB_TABLE}",headers=H({"Prefer":"resolution=merge-duplicates,return=minimal"}),params={"on_conflict":"id"},json=p,timeout=25); r.raise_for_status()

def load_db():
 r=requests.get(f"{SB_URL}/rest/v1/{SB_TABLE}",headers=H(),params={"id":f"eq.{SB_ID}","select":"config","limit":"1"},timeout=12); r.raise_for_status(); rows=r.json()
 if rows:return merge(rows[0].get("config"))
 save_db(DEFAULT_CONFIG); return copy.deepcopy(DEFAULT_CONFIG)

def data_uri(f,max_mb=4):
 if f is None:return ""
 if f.size>max_mb*1024*1024:raise ValueError(f"Imagem acima de {max_mb} MB.")
 return f"data:{f.type or 'image/png'};base64,{base64.b64encode(f.getvalue()).decode()}"

def icon_png(f):
 if f is None:return ""
 if f.size>2*1024*1024:raise ValueError("Ícone PNG acima de 2 MB.")
 im=Image.open(BytesIO(f.getvalue())).convert("RGBA"); im.thumbnail((88,88),Image.Resampling.LANCZOS); canvas=Image.new("RGBA",(128,128),(255,255,255,0)); canvas.alpha_composite(im,((128-im.width)//2,(128-im.height)//2)); out=BytesIO(); canvas.save(out,"PNG",optimize=True); return "data:image/png;base64,"+base64.b64encode(out.getvalue()).decode()

def safe_url(v):
 v=(v or "").strip(); p=urlparse(v); return v if v!="#" and p.scheme in {"http","https"} and p.netloc else "#"
def esc(v):return html.escape(str(v or ""),quote=True)

if "hub_config" not in st.session_state:
 try: st.session_state.hub_config=load_db(); st.session_state.db_ok=True
 except Exception: st.session_state.hub_config=copy.deepcopy(DEFAULT_CONFIG); st.session_state.db_ok=False
if "uv" not in st.session_state:st.session_state.uv=0
if "notice" not in st.session_state:st.session_state.notice=""
cfg=st.session_state.hub_config; uv=st.session_state.uv

with st.sidebar:
 st.title("⚙️ Configurações")
 if st.session_state.get("db_ok"): st.success("Salvamento permanente ativo")
 else: st.warning("Modo temporário: banco indisponível")
 if st.session_state.notice: st.info(st.session_state.notice); st.session_state.notice=""
 with st.form("cfg"):
  st.subheader("Identidade visual")
  ltop=st.file_uploader("Logo do menu superior",type=["png","jpg","jpeg","webp"],key=f"lt{uv}",help="Ajuste automático sem deformar.")
  lfoot=st.file_uploader("Logo inferior",type=["png","jpg","jpeg","webp"],key=f"lf{uv}")
  hero=st.file_uploader("Imagem principal",type=["png","jpg","jpeg","webp"],key=f"h{uv}")
  clear_top=st.checkbox("Remover logo superior e usar texto Setta"); clear_foot=st.checkbox("Usar logo inferior padrão"); clear_hero=st.checkbox("Usar imagem principal padrão")
  if cfg.get("logo_top"): st.caption("Logo superior atual"); st.image(cfg["logo_top"],width=150)
  st.divider(); st.subheader("Textos da página")
  titulo=st.text_input("Título",cfg["titulo"]); subtitulo=st.text_input("Subtítulo",cfg["subtitulo"]); desc=st.text_area("Descrição",cfg["descricao"],height=90); slogan=st.text_area("Texto sobre a imagem",cfg["slogan"],height=90); usuario=st.text_input("Usuário do cabeçalho",cfg["usuario"]); re=st.text_input("Texto inferior esquerdo",cfg["rodape_esquerdo"]); rd=st.text_input("Texto inferior direito",cfg["rodape_direito"])
  st.divider(); st.subheader("Cartões e redirecionamentos"); st.caption("PNG padronizado: canvas 128×128, conteúdo até 88×88 e exibição 48×48 px.")
  apps=[]; uploads=[]; removes=[]
  for i,a in enumerate(cfg["apps"]):
   with st.expander(f"{i+1}. {a.get('nome','Aplicativo')}"):
    n=st.text_input("Nome do cartão",a.get("nome",""),key=f"n{i}_{uv}"); d=st.text_input("Descrição",a.get("descricao",""),key=f"d{i}_{uv}"); s=st.text_input("Status",a.get("status","Ativo"),key=f"s{i}_{uv}"); u=st.text_input("Link de destino",a.get("url","#"),key=f"u{i}_{uv}"); up=st.file_uploader("Ícone PNG",type=["png"],key=f"p{i}_{uv}",help="Máximo 2 MB. Redimensionamento automático."); rm=st.checkbox("Remover PNG e voltar para emoji",key=f"r{i}_{uv}"); em=st.text_input("Emoji de fallback",a.get("icone","🔗"),key=f"e{i}_{uv}")
    if a.get("icone_png"): st.image(a["icone_png"],width=72)
    apps.append({"nome":n,"descricao":d,"icone":em,"icone_png":a.get("icone_png",""),"status":s,"url":u}); uploads.append(up); removes.append(rm)
  apply=st.form_submit_button("Salvar alterações",use_container_width=True,type="primary")
 if apply:
  try:
   ncfg=copy.deepcopy(cfg)
   if clear_top:ncfg["logo_top"]=""
   elif ltop:ncfg["logo_top"]=data_uri(ltop,3)
   if clear_foot:ncfg["logo_footer"]=""
   elif lfoot:ncfg["logo_footer"]=data_uri(lfoot,3)
   if clear_hero:ncfg["hero_image"]=DEFAULT_CONFIG["hero_image"]
   elif hero:ncfg["hero_image"]=data_uri(hero,4)
   for i,a in enumerate(apps):
    if removes[i]:a["icone_png"]=""
    elif uploads[i]:a["icone_png"]=icon_png(uploads[i])
   ncfg.update(titulo=titulo,subtitulo=subtitulo,descricao=desc,slogan=slogan,usuario=usuario,rodape_esquerdo=re,rodape_direito=rd,apps=apps); save_db(ncfg); st.session_state.hub_config=ncfg; st.session_state.db_ok=True; st.session_state.uv+=1; st.session_state.notice="Alterações salvas permanentemente."; st.rerun()
  except Exception as e:st.error(f"Não foi possível salvar: {e}")
 if st.button("Recarregar do banco",use_container_width=True):
  try:st.session_state.hub_config=load_db(); st.session_state.uv+=1; st.session_state.db_ok=True; st.session_state.notice="Dados recarregados."; st.rerun()
  except Exception as e:st.error(str(e))
 if st.button("Restaurar tudo ao padrão",use_container_width=True):
  try:d=copy.deepcopy(DEFAULT_CONFIG); save_db(d); st.session_state.hub_config=d; st.session_state.uv+=1; st.session_state.notice="Padrão restaurado."; st.rerun()
  except Exception as e:st.error(str(e))

cfg=st.session_state.hub_config
CSS='''<style>:root{--y:#FDC33B;--y2:#F9B719;--ink:#1E232E;--line:#E7EBF1;--green:#0FAF4D}.stApp{background:linear-gradient(180deg,#fff,#F8FAFD)}header[data-testid="stHeader"]{background:var(--y)!important;height:76px!important;border-bottom:1px solid rgba(0,0,0,.06)!important;z-index:100000!important}header[data-testid="stHeader"] *{color:var(--ink)!important}[data-testid="stToolbar"]{background:transparent!important}[data-testid="stDecoration"],#MainMenu,footer{display:none!important}[data-testid="stSidebar"]{border-right:1px solid var(--line)!important;background:#fff!important;z-index:100005!important}[data-testid="stSidebar"]>div:first-child{background:#fff!important}.block-container{max-width:100%!important;padding:0!important;margin:0!important}.hub-header-content{position:fixed;top:0;left:0;right:0;height:76px;display:flex;align-items:center;justify-content:space-between;padding:0 220px 0 72px;z-index:100002;pointer-events:none}.page-root{padding-top:76px}.brand-slot{width:180px;height:58px;display:flex;align-items:center;overflow:hidden}.brand-text{color:var(--ink);font-size:43px;font-style:italic;font-weight:900;letter-spacing:-3px}.brand-logo{width:180px;height:54px;max-width:180px;max-height:54px;object-fit:contain;object-position:left center}.user{color:var(--ink);font-size:15px;font-weight:700;display:flex;gap:10px;align-items:center}.user-badge{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:#fff;border:1px solid rgba(30,35,46,.2)}.hero{display:grid;grid-template-columns:1.02fr 1fr;min-height:290px;background:#fff;overflow:hidden}.hero-copy{padding:62px 5% 44px;z-index:2;background:linear-gradient(120deg,#fff 0%,#fff 72%,rgba(255,255,255,.92) 78%,rgba(255,255,255,0) 79%)}.hero h1{margin:0;color:var(--ink);font-size:48px;line-height:1.03;letter-spacing:-2px;font-weight:900}.hero h2{margin:8px 0 0;color:#66728B;font-size:27px;font-weight:500}.hero p{margin:20px 0 0;color:#73809B;font-size:16px;line-height:1.55;max-width:600px}.hero-image{min-height:290px;background-size:cover;background-position:center;position:relative}.hero-slogan{position:absolute;right:7%;top:38px;color:#60708F;font-size:12px;letter-spacing:4px;line-height:1.7;font-weight:700}.hero-slogan:after{content:"";display:block;width:42px;height:3px;background:var(--y2);margin-top:8px}.apps-wrap{padding:0 4% 28px;margin-top:-10px;position:relative;z-index:5}.apps-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.app-card{min-height:190px;display:flex;flex-direction:column;justify-content:space-between;text-decoration:none!important;color:inherit!important;background:radial-gradient(circle at 108% 110%,rgba(253,195,59,.16) 0 27%,transparent 28%),#fff;border:1px solid var(--line);border-radius:16px;padding:24px 30px 22px;box-shadow:0 8px 24px rgba(44,62,92,.06);transition:.18s}.app-card:hover{transform:translateY(-4px);box-shadow:0 16px 34px rgba(44,62,92,.12)}.card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}.app-icon{width:72px;height:72px;border-radius:16px;display:flex;align-items:center;justify-content:center;background:#FFF7E2;overflow:hidden;flex:0 0 72px}.app-icon img{width:48px;height:48px;object-fit:contain}.app-icon-emoji{font-size:34px}.status{display:flex;align-items:center;gap:7px;background:#E9F9EF;color:#15883F;font-size:13px;font-weight:700;border-radius:999px;padding:7px 12px}.dot{width:10px;height:10px;border-radius:50%;background:var(--green)}.app-title{margin-top:10px;color:#101738;font-weight:900;font-size:24px}.app-desc{margin-top:4px;color:#77839B;font-size:15px}.access{margin-top:20px;color:#F1A000;font-size:16px;font-weight:800;display:flex;gap:10px}.page-footer{min-height:62px;border-top:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 4%;background:#fff;color:#97A2B8;font-size:11px;letter-spacing:2px;text-transform:uppercase}.footer-brand{display:flex;align-items:center;gap:12px}.footer-logo-slot{width:72px;height:30px;display:flex;align-items:center}.footer-brand-text{color:var(--ink);font-size:21px;font-style:italic;font-weight:900}.footer-logo{width:72px;height:30px;object-fit:contain}.footer-line{width:32px;height:3px;background:var(--y2);display:inline-block;margin-left:10px}@media(max-width:1100px){.hero h1{font-size:40px}.apps-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.user{display:none}}@media(max-width:760px){header[data-testid="stHeader"]{height:66px!important}.hub-header-content{height:66px;padding:0 20px 0 62px}.page-root{padding-top:66px}.brand-slot{width:150px;height:50px}.brand-logo{width:150px;height:46px}.brand-text{font-size:35px}.hero{grid-template-columns:1fr}.hero-copy{padding:38px 22px 32px}.hero h1{font-size:34px}.hero h2{font-size:20px}.hero-image{min-height:190px}.apps-wrap{padding:18px}.apps-grid{grid-template-columns:1fr}.app-card{padding:22px}.page-footer{flex-direction:column;gap:10px;padding:16px 18px}}</style>'''
st.html(CSS)
logo_top=f'<img class="brand-logo" src="{cfg["logo_top"]}" alt="Logo">' if cfg.get("logo_top") else '<div class="brand-text">Setta</div>'; logo_footer=f'<img class="footer-logo" src="{cfg["logo_footer"]}" alt="Logo">' if cfg.get("logo_footer") else '<div class="footer-brand-text">Setta</div>'
def icon(a):return f'<img src="{a.get("icone_png")}" alt="Ícone">' if a.get("icone_png") else f'<span class="app-icon-emoji">{esc(a.get("icone","🔗"))}</span>'
cards=""
for a in cfg["apps"]:cards+=f'<a class="app-card" href="{esc(safe_url(a.get("url","#")))}" target="_blank"><div><div class="card-top"><div class="app-icon">{icon(a)}</div><div class="status"><span class="dot"></span>{esc(a.get("status","Ativo"))}</div></div><div class="app-title">{esc(a.get("nome","Aplicativo"))}</div><div class="app-desc">{esc(a.get("descricao",""))}</div></div><div class="access">Acessar →</div></a>'
page=f'<div class="hub-header-content"><div class="brand-slot">{logo_top}</div><div class="user"><div class="user-badge">●</div><span>{esc(cfg["usuario"])}</span></div></div><div class="page-root"><section class="hero"><div class="hero-copy"><h1>{esc(cfg["titulo"])}</h1><h2>{esc(cfg["subtitulo"])}</h2><p>{esc(cfg["descricao"]).replace(chr(10),"<br>")}</p></div><div class="hero-image" style="background-image:url(\'{esc(cfg["hero_image"])}\')"><div class="hero-slogan">{esc(cfg["slogan"]).replace(chr(10),"<br>")}</div></div></section><div class="apps-wrap"><div class="apps-grid">{cards}</div></div><div class="page-footer"><div class="footer-brand"><div class="footer-logo-slot">{logo_footer}</div><span>|</span><span>{esc(cfg["rodape_esquerdo"])}</span></div><div>{esc(cfg["rodape_direito"])}<span class="footer-line"></span></div></div></div>'
st.html(page)
