import streamlit as st
from pathlib import Path

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")

LOGO = Path(__file__).parent / "logo_irene.png"

if "page" not in st.session_state:
    st.session_state.page = "Centro de Operaciones"
if "items" not in st.session_state:
    st.session_state.items = [
        {"tipo": "Nota de voz", "texto": "Idea para vídeo: ¿sabías que...? sobre libros antiguos", "estado": "Por organizar"},
        {"tipo": "Idea", "texto": "Post: por qué Irene Zurilla escribe", "estado": "Por organizar"},
    ]
if "tasks" not in st.session_state:
    st.session_state.tasks = ["Revisar calendario + noticias", "Preparar base de contactos", "Crear banco de contenidos"]
if "app_ideas" not in st.session_state:
    st.session_state.app_ideas = ["Menú compacto en móvil", "Cards realmente clicables", "Integrar Drive"]

PAGES = [
    "Centro de Operaciones", "Semillero", "Tareas", "Radar", "Estudio", "Calendario",
    "Relaciones", "Libros y relatos", "Ideas para la app", "Ajustes"
]

CSS = """
<style>
:root{--bg:#fbf4ea;--card:#fffdf8;--ink:#232129;--muted:#766f68;--line:#eadccf;--accent:#73549b;--soft:#efe3d7;}
.stApp{background:linear-gradient(180deg,#fffaf3 0%,#f7eadc 100%);}
.block-container{padding-top:1.1rem!important;padding-bottom:2rem!important;max-width:760px!important;}
[data-testid="stHeader"]{background:rgba(255,250,243,.86)!important;backdrop-filter: blur(8px);}
button{border-radius:18px!important;}
.header{display:flex;align-items:center;justify-content:space-between;gap:12px;border-bottom:1px solid var(--line);padding:0 0 12px 0;margin-bottom:12px;}
.brand{display:flex;align-items:center;gap:10px;min-width:0;}
.brand img{width:52px;height:52px;border-radius:50%;object-fit:cover;box-shadow:0 8px 22px rgba(80,50,20,.16);}
.brand .iz{font-size:30px;font-weight:900;color:var(--ink);letter-spacing:-1px;}
.badge{padding:8px 14px;border-radius:999px;background:#fff8f0;border:1px solid var(--line);color:var(--muted);font-size:15px;white-space:nowrap;}
.hero{background:linear-gradient(135deg,#fffaf4,#ead8c5);border:1px solid var(--line);border-radius:30px;padding:28px 26px;margin:14px 0 16px;box-shadow:0 16px 40px rgba(85,55,30,.10);}
.hero h1{font-size:42px;line-height:1.04;margin:0 0 14px;color:var(--ink);letter-spacing:-1px;}
.hero p{font-size:22px;color:var(--muted);line-height:1.45;margin:0;}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:12px 0 16px;}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:12px 8px;text-align:center;box-shadow:0 10px 22px rgba(85,55,30,.06);}
.kpi .icon{font-size:22px;line-height:1;}
.kpi .num{font-size:28px;font-weight:900;color:var(--accent);line-height:1.1;margin-top:3px;}
.kpi .label{font-size:13px;color:var(--ink);margin-top:2px;}
.summary{background:var(--card);border:1px solid var(--line);border-radius:24px;padding:20px;margin:18px 0;box-shadow:0 12px 26px rgba(85,55,30,.07);}
.summary h2{font-size:26px;margin:0 0 12px;color:var(--ink);}
.summary-row{border-top:1px solid #f1e6da;padding:11px 0;font-size:17px;color:var(--ink);line-height:1.35;}
.summary-row:first-of-type{border-top:0;}
.summary-row b{color:var(--ink);}
.card{background:var(--card);border:1px solid var(--line);border-radius:26px;padding:22px;margin:16px 0;box-shadow:0 12px 28px rgba(85,55,30,.07);}
.card h2{font-size:34px;margin:0 0 12px;color:var(--ink);}
.card h3{font-size:24px;margin:0 0 10px;color:var(--ink);}
.muted{color:var(--muted);font-size:18px;line-height:1.45;}
.pill{display:inline-block;background:var(--soft);border:1px solid var(--line);border-radius:999px;padding:8px 14px;margin:4px 6px 4px 0;color:var(--ink);font-size:15px;}
.stSelectbox label,.stTextArea label,.stTextInput label{font-weight:700;color:var(--ink)!important;}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div{border-radius:18px;background:#fffdf8;border-color:var(--line);min-height:50px;}
.stButton>button{width:100%;border:1px solid var(--line);background:#fffdf8;color:#232129;padding:.72rem 1rem;font-weight:700;}
.navrow div[data-testid="column"]{padding:0 4px;}
@media(max-width:640px){
 .block-container{padding-left:18px!important;padding-right:18px!important;padding-top:.8rem!important;}
 .brand img{width:46px;height:46px}.brand .iz{font-size:28px}.badge{font-size:14px;padding:7px 12px;}
 .hero{padding:22px 20px;border-radius:28px;margin-top:12px;}
 .hero h1{font-size:38px;}
 .hero p{font-size:21px;}
 .kpi-grid{grid-template-columns:repeat(4,1fr);gap:8px;}
 .kpi{border-radius:17px;padding:10px 4px;}
 .kpi .icon{font-size:19px}.kpi .num{font-size:25px}.kpi .label{font-size:12px;}
 .summary{padding:17px;border-radius:22px;}
 .summary h2{font-size:24px;}
 .summary-row{font-size:16px;}
 .card h2{font-size:31px;}
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Header
if LOGO.exists():
    import base64
    logo_b64 = base64.b64encode(LOGO.read_bytes()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="Irene Zurilla" />'
else:
    logo_html = '<div style="font-size:34px">IZ</div>'
st.markdown(f"""
<div class="header">
  <div class="brand">{logo_html}<div class="iz">IZ</div></div>
  <div class="badge">V2.8 estable</div>
</div>
""", unsafe_allow_html=True)

# Top actions: Notes + compact menu
c1, c2 = st.columns([1, 1])
with c1:
    if st.button("🎙️ Notas", key="top_notes"):
        st.session_state.page = "Semillero"
        st.rerun()
with c2:
    page = st.selectbox("☰ Menú", PAGES, index=PAGES.index(st.session_state.page), label_visibility="collapsed")
    if page != st.session_state.page:
        st.session_state.page = page
        st.rerun()

def goto(label):
    st.session_state.page = label
    st.rerun()

def kpis():
    task_count = len(st.session_state.tasks)
    seed_count = len(st.session_state.items)
    opp_count = 4
    event_count = 2
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi"><div class="icon">✅</div><div class="num">{task_count}</div><div class="label">Tareas</div></div>
      <div class="kpi"><div class="icon">🌱</div><div class="num">{seed_count}</div><div class="label">Semillas</div></div>
      <div class="kpi"><div class="icon">⭐</div><div class="num">{opp_count}</div><div class="label">Oportunidades</div></div>
      <div class="kpi"><div class="icon">🗓️</div><div class="num">{event_count}</div><div class="label">Eventos</div></div>
    </div>
    """, unsafe_allow_html=True)
    a,b,c,d = st.columns(4)
    with a:
        if st.button("Abrir", key="kpi_tasks"): goto("Tareas")
    with b:
        if st.button("Abrir", key="kpi_seeds"): goto("Semillero")
    with c:
        if st.button("Abrir", key="kpi_radar"): goto("Radar")
    with d:
        if st.button("Abrir", key="kpi_cal"): goto("Calendario")

def centro():
    st.markdown("""
    <div class="hero">
      <h1>Centro de<br>Operaciones</h1>
      <p>Buenos días, Irene · Aquí está lo que necesita tu atención.</p>
    </div>
    """, unsafe_allow_html=True)
    kpis()
    st.markdown("""
    <div class="summary">
      <h2>Resumen de hoy</h2>
      <div class="summary-row">🎯 <b>Prioridad:</b> preparar base de contactos y revisar agenda cultural.</div>
      <div class="summary-row">🔥 <b>Radar:</b> 4 oportunidades para revisar esta semana.</div>
      <div class="summary-row">📚 <b>Libro activo:</b> El libro mágico de Hugo e Inés · preparación de publicación.</div>
      <div class="summary-row">🎙️ <b>Última nota:</b> idea para vídeo sobre libros antiguos.</div>
    </div>
    """, unsafe_allow_html=True)

def semillero():
    st.markdown('<div class="card"><h2>🌱 Semillero</h2><p class="muted">Notas, ideas y elementos pendientes de organizar.</p></div>', unsafe_allow_html=True)
    tipo = st.selectbox("Tipo", ["Nota de voz", "Idea", "Contacto", "Evento", "Noticia", "Sugerencia app"])
    txt = st.text_area("Contenido", placeholder="Guarda aquí algo que todavía no sabes dónde colocar...")
    if st.button("Guardar en Semillero"):
        if txt.strip():
            st.session_state.items.append({"tipo": tipo, "texto": txt.strip(), "estado": "Por organizar"})
            st.success("Guardado en Semillero")
    for i, item in enumerate(st.session_state.items):
        st.markdown(f'<div class="card"><h3>{item["tipo"]}</h3><p class="muted">{item["texto"]}</p><span class="pill">{item["estado"]}</span></div>', unsafe_allow_html=True)

def tareas():
    st.markdown('<div class="card"><h2>✅ Tareas</h2><p class="muted">Pendientes de carrera y lanzamiento.</p></div>', unsafe_allow_html=True)
    new = st.text_input("Nueva tarea")
    if st.button("Añadir tarea"):
        if new.strip():
            st.session_state.tasks.append(new.strip())
            st.success("Tarea añadida")
    st.markdown('<div class="card"><h3>🔥 Hoy</h3>', unsafe_allow_html=True)
    for t in st.session_state.tasks:
        st.checkbox(t, key=f"task_{t}")
    st.markdown('</div>', unsafe_allow_html=True)

def radar():
    st.markdown('<div class="card"><h2>🧭 Radar</h2><p class="muted">Oportunidades culturales, editoriales y literarias.</p></div>', unsafe_allow_html=True)
    for text in ["Presentación en FNAC Callao · Madrid", "Concurso de relato histórico · cierra en 16 días", "Buscar eventos de librerías en Getafe/Leganés", "Club de lectura en Madrid"]:
        st.markdown(f'<div class="card"><h3>Oportunidad</h3><p class="muted">{text}</p><span class="pill">Revisar</span></div>', unsafe_allow_html=True)

def estudio():
    st.markdown('<div class="card"><h2>🎬 Estudio</h2><p class="muted">Banco de contenidos y producción.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>Ideas</h3><p>¿Sabías que...? sobre libros antiguos</p><p>Vídeo: una foto, una historia</p></div>', unsafe_allow_html=True)

def calendario():
    st.markdown('<div class="card"><h2>🗓️ Calendario</h2><p class="muted">Agenda de publicaciones, eventos y fechas clave.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>Esta semana</h3><p>Viernes · Revisar radar cultural</p><p>Domingo · Reunión de dirección</p></div>', unsafe_allow_html=True)

def relaciones():
    st.markdown('<div class="card"><h2>🤝 Relaciones</h2><p class="muted">Contactos, librerías, editoriales y bibliotecas.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>Seguimiento</h3><p>Librerías de Madrid · pendiente de base inicial</p><p>Bibliotecas · preparar listado</p></div>', unsafe_allow_html=True)

def libros():
    st.markdown('<div class="card"><h2>📚 Libros y relatos</h2><p class="muted">Obras terminadas, publicadas o pendientes de mover.</p></div>', unsafe_allow_html=True)
    for obra, estado in [("El libro mágico de Hugo e Inés", "Preparación de publicación"), ("Preludio de un ocaso", "Relato terminado"), ("La casa del ciervo", "Cuento listo para ilustrar")]:
        st.markdown(f'<div class="card"><h3>{obra}</h3><p class="muted">{estado}</p></div>', unsafe_allow_html=True)

def ideas_app():
    st.markdown('<div class="card"><h2>💡 Ideas para la app</h2><p class="muted">Mejoras que se te ocurran mientras la usas.</p></div>', unsafe_allow_html=True)
    idea = st.text_input("Nueva idea para la app")
    if st.button("Guardar idea"):
        if idea.strip():
            st.session_state.app_ideas.append(idea.strip())
            st.success("Idea guardada")
    for idea in st.session_state.app_ideas:
        st.markdown(f'<div class="card"><p>{idea}</p><span class="pill">En revisión</span></div>', unsafe_allow_html=True)

def ajustes():
    st.markdown('<div class="card"><h2>⚙️ Ajustes</h2><p class="muted">Drive, copias y configuración futura.</p></div>', unsafe_allow_html=True)
    st.info("Google Drive se integrará en una fase posterior.")

ROUTES = {
    "Centro de Operaciones": centro,
    "Semillero": semillero,
    "Tareas": tareas,
    "Radar": radar,
    "Estudio": estudio,
    "Calendario": calendario,
    "Relaciones": relaciones,
    "Libros y relatos": libros,
    "Ideas para la app": ideas_app,
    "Ajustes": ajustes,
}

ROUTES[st.session_state.page]()
