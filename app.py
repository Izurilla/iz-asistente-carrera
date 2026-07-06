
import streamlit as st
from pathlib import Path
import base64

st.set_page_config(
    page_title="IZ | Asistente de Carrera",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

VERSION = "V2.7 estable"

# ---------- ESTADO ----------
if "page" not in st.session_state:
    st.session_state.page = "Centro de Operaciones"
if "semillero" not in st.session_state:
    st.session_state.semillero = [
        {"tipo": "Nota de voz", "texto": "Idea para vídeo: ¿sabías que...? sobre libros antiguos.", "estado": "Por organizar"},
        {"tipo": "Idea", "texto": "Crear banco de contenidos para septiembre.", "estado": "Por organizar"},
    ]
if "tareas" not in st.session_state:
    st.session_state.tareas = [
        {"texto": "Revisar calendario + noticias", "hecha": False},
        {"texto": "Preparar base de contactos", "hecha": False},
        {"texto": "Crear banco de contenidos", "hecha": False},
    ]
if "ideas_app" not in st.session_state:
    st.session_state.ideas_app = [
        "El menú en móvil debe ser compacto.",
        "Las cards del dashboard deben sentirse clicables.",
        "El micro debe ir arriba, no flotando abajo.",
    ]

PAGES = [
    "Centro de Operaciones",
    "Semillero",
    "Tareas",
    "Radar",
    "Estudio",
    "Calendario",
    "Relaciones",
    "Libros y relatos",
    "Ideas para la app",
    "Ajustes",
]

# ---------- ESTILO ----------
st.markdown("""
<style>
:root{
  --bg:#fbf5ec;
  --card:#fffdf8;
  --soft:#efe0d1;
  --line:#e5d5c7;
  --text:#1f1e22;
  --muted:#776e67;
  --accent:#7d5fa0;
}
html, body, [data-testid="stAppViewContainer"] {
  background: radial-gradient(circle at top, #fffaf1 0%, #fbf5ec 42%, #f3e7d8 100%);
}
[data-testid="stHeader"], [data-testid="stToolbar"]{
  background: rgba(255,255,255,0.65) !important;
}
.block-container{
  padding-top: 1.2rem !important;
  padding-bottom: 2rem !important;
  max-width: 740px !important;
}
.iz-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  margin: 0.2rem 0 0.8rem 0;
}
.iz-brand{
  display:flex;
  align-items:center;
  gap:12px;
}
.iz-logo{
  width:58px;
  height:58px;
  border-radius:50%;
  object-fit:cover;
  box-shadow:0 8px 24px rgba(60,45,30,.14);
}
.iz-title{
  font-size:28px;
  font-weight:850;
  letter-spacing:-0.04em;
  color:var(--text);
}
.version-pill{
  border:1px solid var(--line);
  border-radius:999px;
  padding:10px 16px;
  color:#6d625a;
  background:rgba(255,255,255,.45);
  white-space:nowrap;
}
.nav-row{
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap:10px;
  margin: 0.5rem 0 0.8rem 0;
}
.stButton > button{
  width:100%;
  border-radius:18px !important;
  min-height:48px;
  border:1px solid var(--line);
  background:rgba(255,255,255,.78);
  color:var(--text);
  font-size:18px;
}
div[data-baseweb="select"] > div{
  border-radius:18px !important;
  border-color:var(--line) !important;
  background:rgba(255,255,255,.82) !important;
  min-height:54px;
}
.hero{
  border:1px solid var(--line);
  border-radius:34px;
  padding:34px 34px;
  background:linear-gradient(135deg,#fffaf2,#ead7c5);
  box-shadow:0 18px 40px rgba(68,45,25,.08);
  margin:1rem 0 1.2rem 0;
}
.hero h1{
  margin:0 0 18px 0;
  font-size:48px;
  line-height:1.05;
  letter-spacing:-0.055em;
}
.hero p{
  margin:0;
  font-size:22px;
  color:var(--muted);
  line-height:1.55;
}
.kpi-grid{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:10px;
  margin: 0.7rem 0 1.1rem 0;
}
.kpi{
  border:1px solid var(--line);
  background:rgba(255,255,255,.86);
  border-radius:22px;
  padding:14px 8px;
  text-align:center;
  box-shadow:0 10px 22px rgba(68,45,25,.05);
}
.kpi strong{
  display:block;
  font-size:28px;
  color:var(--accent);
  line-height:1;
}
.kpi span{
  display:block;
  font-size:13px;
  margin-top:8px;
  color:#3f3935;
}
.card{
  border:1px solid var(--line);
  border-radius:28px;
  padding:24px 26px;
  background:rgba(255,255,255,.88);
  box-shadow:0 14px 34px rgba(68,45,25,.07);
  margin: 0.9rem 0;
}
.card h2{
  margin:0 0 14px 0;
  font-size:27px;
  letter-spacing:-0.035em;
}
.card p, .card li{
  font-size:18px;
  color:#3b3733;
  line-height:1.55;
}
.chips{
  display:flex;
  flex-wrap:wrap;
  gap:10px;
  margin-top:12px;
}
.chip{
  padding:9px 14px;
  border-radius:999px;
  background:#ead9c9;
  border:1px solid #dfcdbc;
  color:#3b332d;
}
.mini-actions{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:10px;
}
.small-note{
  color:var(--muted);
  font-size:14px;
  text-align:center;
  margin:0.2rem 0 0.8rem 0;
}
@media(max-width:520px){
  .block-container{
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }
  .iz-logo{width:50px;height:50px;}
  .iz-title{font-size:26px;}
  .version-pill{font-size:15px;padding:8px 12px;}
  .nav-row{grid-template-columns:1fr 1fr;}
  .hero{padding:28px 26px;border-radius:30px;}
  .hero h1{font-size:42px;}
  .hero p{font-size:21px;}
  .kpi-grid{grid-template-columns:repeat(4,1fr);gap:8px;}
  .kpi{border-radius:18px;padding:12px 4px;}
  .kpi strong{font-size:25px;}
  .kpi span{font-size:12px;}
  .card{padding:22px 24px;border-radius:26px;}
  .card h2{font-size:25px;}
}
</style>
""", unsafe_allow_html=True)

def logo_html():
    logo_path = Path("logo_irene.png")
    if logo_path.exists():
        data = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
        return f'<img class="iz-logo" src="data:image/png;base64,{data}">'
    return '<div class="iz-logo" style="display:flex;align-items:center;justify-content:center;background:#fff;">IZ</div>'

def go(page):
    st.session_state.page = page

# ---------- CABECERA ----------
st.markdown(f"""
<div class="iz-header">
  <div class="iz-brand">
    {logo_html()}
    <div class="iz-title">IZ</div>
  </div>
  <div class="version-pill">{VERSION}</div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    if st.button("🎙️ Notas", key="top_notas"):
        go("Semillero")
with c2:
    menu_value = st.selectbox("☰ Menú", PAGES, index=PAGES.index(st.session_state.page), key="nav_select", label_visibility="collapsed")
    if menu_value != st.session_state.page:
        go(menu_value)

# ---------- PÁGINAS ----------
def centro():
    st.markdown("""
    <div class="hero">
      <h1>Centro de<br>Operaciones</h1>
      <p>Buenos días, Irene · Aquí está lo que necesita tu atención.</p>
    </div>
    """, unsafe_allow_html=True)

    tareas_pendientes = sum(1 for t in st.session_state.tareas if not t["hecha"])
    semillas = len(st.session_state.semillero)
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi"><strong>{tareas_pendientes}</strong><span>Tareas</span></div>
      <div class="kpi"><strong>{semillas}</strong><span>Semillas</span></div>
      <div class="kpi"><strong>4</strong><span>Oportunidades</span></div>
      <div class="kpi"><strong>2</strong><span>Eventos</span></div>
    </div>
    """, unsafe_allow_html=True)

    a,b,c,d = st.columns(4)
    with a:
        if st.button("Tareas", key="kpi_tareas"): go("Tareas")
    with b:
        if st.button("Semillero", key="kpi_semillero"): go("Semillero")
    with c:
        if st.button("Radar", key="kpi_radar"): go("Radar")
    with d:
        if st.button("Calendario", key="kpi_cal"): go("Calendario")

    st.markdown("""
    <div class="card">
      <h2>🎯 Prioridad del día</h2>
      <ul>
        <li>Preparar base de contactos.</li>
        <li>Crear banco de contenidos.</li>
        <li>Revisar agenda cultural.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <h2>🔥 Radar rápido</h2>
      <p>4 oportunidades detectadas para revisar esta semana.</p>
      <div class="chips">
        <span class="chip">Madrid</span>
        <span class="chip">Librerías</span>
        <span class="chip">Concursos</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <h2>📚 Libro activo</h2>
      <p><strong>El libro mágico de Hugo e Inés</strong><br>Fase: preparación de publicación.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <h2>🎙️ Última nota de voz</h2>
      <p>Idea para vídeo: ¿sabías que...? sobre libros antiguos.</p>
      <p style="color:#776e67;">Estado: por organizar</p>
    </div>
    """, unsafe_allow_html=True)

def semillero():
    st.title("🌱 Semillero")
    st.write("Todo lo que aún no tiene sitio definitivo entra aquí.")
    with st.form("nueva_semilla", clear_on_submit=True):
        tipo = st.selectbox("Tipo", ["Nota de voz", "Idea", "Contacto", "Evento", "Noticia", "Concurso", "Relato"])
        texto = st.text_area("Contenido", placeholder="Guarda aquí algo que todavía no sabes dónde colocar...")
        submitted = st.form_submit_button("Guardar en Semillero")
        if submitted and texto.strip():
            st.session_state.semillero.insert(0, {"tipo": tipo, "texto": texto.strip(), "estado": "Por organizar"})
            st.success("Guardado en Semillero.")
    for i, item in enumerate(st.session_state.semillero):
        st.markdown(f"""
        <div class="card">
          <h2>🎙️ {item['tipo']}</h2>
          <p>{item['texto']}</p>
          <span class="chip">{item['estado']}</span>
        </div>
        """, unsafe_allow_html=True)

def tareas():
    st.title("✅ Tareas")
    with st.form("nueva_tarea", clear_on_submit=True):
        texto = st.text_input("Nueva tarea")
        add = st.form_submit_button("Añadir")
        if add and texto.strip():
            st.session_state.tareas.append({"texto": texto.strip(), "hecha": False})
            st.success("Tarea añadida.")
    st.subheader("🔥 Hoy")
    for i, tarea in enumerate(st.session_state.tareas):
        st.session_state.tareas[i]["hecha"] = st.checkbox(tarea["texto"], value=tarea["hecha"], key=f"task_{i}")

def radar():
    st.title("🧭 Radar")
    tabs = st.tabs(["⭐ Recomendado", "🎤 Eventos", "🏆 Concursos", "📰 Noticias"])
    with tabs[0]:
        st.markdown('<div class="card"><h2>Oportunidad</h2><p>Presentación en FNAC Callao · Madrid</p><span class="chip">Revisar</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h2>Oportunidad</h2><p>Concurso de relato histórico · cierra en 16 días</p><span class="chip">Revisar</span></div>', unsafe_allow_html=True)
    with tabs[1]:
        st.write("Eventos literarios y culturales para revisar.")
    with tabs[2]:
        st.write("Concursos pendientes de clasificar.")
    with tabs[3]:
        st.write("Noticias del sector editorial.")

def estudio():
    st.title("🎬 Estudio")
    st.markdown('<div class="card"><h2>Ideas</h2><p>¿Sabías que...? sobre libros antiguos</p><p>Vídeo: una foto, una historia</p></div>', unsafe_allow_html=True)

def calendario():
    st.title("📅 Calendario")
    st.markdown('<div class="card"><h2>Esta semana</h2><p>Viernes: revisar radar del fin de semana.</p><p>Domingo: reunión de dirección.</p></div>', unsafe_allow_html=True)

def relaciones():
    st.title("🤝 Relaciones")
    st.markdown('<div class="card"><h2>Contactos prioritarios</h2><p>Librerías, bibliotecas, autores, prensa y clubes de lectura.</p></div>', unsafe_allow_html=True)

def libros():
    st.title("📚 Libros y relatos")
    st.write("Aquí irá todo lo terminado o en campaña, publicado o no.")
    st.markdown('<div class="card"><h2>El libro mágico de Hugo e Inés</h2><p>Estado: preparación de publicación.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h2>Preludio de un ocaso</h2><p>Relato terminado · posible concurso.</p></div>', unsafe_allow_html=True)

def ideas_app():
    st.title("💡 Ideas para la app")
    with st.form("idea_app", clear_on_submit=True):
        idea = st.text_input("Nueva idea de mejora")
        ok = st.form_submit_button("Guardar idea")
        if ok and idea.strip():
            st.session_state.ideas_app.insert(0, idea.strip())
            st.success("Idea guardada.")
    for idea in st.session_state.ideas_app:
        st.markdown(f'<div class="card"><p>{idea}</p><span class="chip">Nueva</span></div>', unsafe_allow_html=True)

def ajustes():
    st.title("⚙️ Ajustes")
    st.write("Próximamente: Drive, copias, exportaciones y preferencias.")

page = st.session_state.page
if page == "Centro de Operaciones": centro()
elif page == "Semillero": semillero()
elif page == "Tareas": tareas()
elif page == "Radar": radar()
elif page == "Estudio": estudio()
elif page == "Calendario": calendario()
elif page == "Relaciones": relaciones()
elif page == "Libros y relatos": libros()
elif page == "Ideas para la app": ideas_app()
elif page == "Ajustes": ajustes()
