import streamlit as st

st.set_page_config(
    page_title="SETTA HUB | Central de Aplicativos",
    page_icon="🟨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CONFIGURAÇÃO DOS APLICATIVOS
# Para adicionar um novo card futuramente, basta inserir um novo
# dicionário nesta lista.
# ============================================================
APPS = [
    {
        "nome": "Gestão Almoxarifado",
        "descricao": "Gestão completa da operação",
        "icone": "📦",
        "status": "Online",
        "url": "#",
    },
    {
        "nome": "Dashboard Operacional",
        "descricao": "Indicadores e resultados",
        "icone": "📊",
        "status": "Online",
        "url": "#",
    },
    {
        "nome": "MRP",
        "descricao": "Demanda e necessidade de materiais",
        "icone": "📋",
        "status": "Ativo",
        "url": "#",
    },
    {
        "nome": "Entregas",
        "descricao": "Controle de OPs e cronograma",
        "icone": "🚚",
        "status": "Online",
        "url": "#",
    },
    {
        "nome": "Compra Fácil",
        "descricao": "Compras e histórico de preços",
        "icone": "🛒",
        "status": "Ativo",
        "url": "#",
    },
    {
        "nome": "Gestão de Equipe",
        "descricao": "Colaboradores e plano de carreira",
        "icone": "👥",
        "status": "Online",
        "url": "#",
    },
]

HERO_IMAGE_URL = "https://gruposetta.com.br/wp-content/uploads/2026/03/entradaG9.jpg-2-1-scaled-e1774901671839.png"

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
        background:transparent;
        height:0;
    }

    [data-testid="stToolbar"], [data-testid="stDecoration"],
    #MainMenu, footer{
        display:none !important;
    }

    .block-container{
        max-width:100% !important;
        padding:0 !important;
        margin:0 !important;
    }

    .topbar{
        height:82px;
        background:linear-gradient(90deg,var(--setta-yellow) 0%, #FFC83E 62%, var(--setta-yellow) 100%);
        display:flex;
        align-items:center;
        justify-content:space-between;
        padding:0 5%;
        border-bottom:1px solid rgba(0,0,0,.05);
    }

    .brand{
        color:var(--setta-ink);
        font-size:43px;
        font-style:italic;
        font-weight:900;
        letter-spacing:-3px;
        line-height:1;
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
        background:
          linear-gradient(120deg,#FFFFFF 0%,#FFFFFF 72%,rgba(255,255,255,.92) 78%,rgba(255,255,255,0) 79%);
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
        background:
           radial-gradient(circle at 108% 110%, rgba(253,195,59,.16) 0 27%, transparent 28%),
           #FFFFFF;
        border:1px solid var(--setta-line);
        border-radius:16px;
        padding:24px 30px 22px 30px;
        box-shadow:0 8px 24px rgba(44,62,92,.06);
        transition:transform .18s ease, box-shadow .18s ease, border-color .18s ease;
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
    }

    .footer-brand strong{
        color:var(--setta-ink);
        font-size:21px;
        font-style:italic;
        letter-spacing:-1px;
        text-transform:none;
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
        .topbar{
            height:70px;
            padding:0 20px;
        }
        .brand{font-size:35px;}
        .user span:last-child{display:none;}
        .hero{
            grid-template-columns:1fr;
        }
        .hero-copy{
            padding:38px 22px 32px 22px;
            background:#fff;
        }
        .hero h1{
            font-size:34px;
            letter-spacing:-1px;
        }
        .hero h2{font-size:20px;}
        .hero p{font-size:14px;}
        .hero-image{
            min-height:190px;
        }
        .apps-wrap{
            padding:18px 18px 28px 18px;
            margin-top:0;
        }
        .apps-grid{grid-template-columns:1fr;}
        .app-card{
            min-height:175px;
            padding:22px;
        }
        .page-footer{
            flex-direction:column;
            gap:8px;
            justify-content:center;
            text-align:center;
            padding:16px 18px;
        }
    }
</style>
"""
)

hero_style = f'background-image:url("{HERO_IMAGE_URL}");'

cards_html = ""
for app in APPS:
    cards_html += f"""
    <a class="app-card" href="{app['url']}" target="_blank" rel="noopener noreferrer">
        <div>
            <div class="card-top">
                <div class="app-icon">{app['icone']}</div>
                <div class="status"><span class="dot"></span>{app['status']}</div>
            </div>
            <div class="app-title">{app['nome']}</div>
            <div class="app-desc">{app['descricao']}</div>
        </div>
        <div class="access">Acessar <span class="arrow">→</span></div>
    </a>
    """

html = f"""
<div class="topbar">
    <div class="brand">Setta</div>
    <div class="user">
        <div class="user-badge">●</div>
        <span>Olá, Usuário</span>
        <span>⌄</span>
    </div>
</div>

<section class="hero">
    <div class="hero-copy">
        <h1>CENTRAL DE APLICATIVOS</h1>
        <h2>Acesso rápido aos sistemas operacionais</h2>
        <p>Soluções integradas que impulsionam a eficiência,<br>
        conectam pessoas e constroem grandes resultados.</p>
    </div>

    <div class="hero-image" style='{hero_style}'>
        <div class="hero-slogan">
            TECNOLOGIA<br>
            QUE CONSTRÓI<br>
            O AMANHÃ
        </div>
    </div>
</section>

<div class="apps-wrap">
    <div class="apps-grid">
        {cards_html}
    </div>
</div>

<div class="page-footer">
    <div class="footer-brand">
        <strong>Setta</strong>
        <span>|</span>
        <span>TECNOLOGIA A SERVIÇO DE GRANDES RESULTADOS</span>
    </div>
    <div>
        JUNTOS, CONSTRUÍMOS O AMANHÃ <span class="footer-line"></span>
    </div>
</div>
"""

st.html(html)
