import streamlit as st
from datetime import datetime

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")

# ---------- ESTADO ----------
if "page" not in st.session_state:
    st.session_state.page = "Centro de Operaciones"
if "tareas" not in st.session_state:
    st.session_state.tareas = [
        {"texto": "Preparar base de contactos", "done": False},
        {"texto": "Crear banco de contenidos", "done": False},
        {"texto": "Revisar agenda cultural", "done": False},
    ]
if "semillero" not in st.session_state:
    st.session_state.semillero = [
        {"tipo": "Nota de voz", "texto": "Idea para vídeo: ¿sabías que...? sobre libros antiguos", "estado": "Por organizar"},
        {"tipo": "Idea", "texto": "Serie de curiosidades históricas para septiembre", "estado": "Por organizar"},
    ]
if "ideas_app" not in st.session_state:
    st.session_state.ideas_app = [
        {"texto": "Menú desplegable funcional", "estado": "Hecho"},
        {"texto": "Notas de voz con grabación real", "estado": "Pendiente"},
    ]
if "notas" not in st.session_state:
    st.session_state.notas = []

# ---------- ESTILOS ----------
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg,#fbf7ef 0%,#f2e7d9 100%); }
    header, footer { visibility: hidden; }
    .block-container { padding-top: 1rem; padding-bottom: 7rem; max-width: 760px; }
    .topbar { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:14px; }
    .brand { font-size: 1.35rem; font-weight: 800; color:#1d1b1a; }
    .version { font-size:.85rem; padding:6px 12px; border:1px solid #e0d3c4; border-radius:999px; background:#fffaf3; color:#6d6258; }
    .hero { background: linear-gradient(135deg,#fffaf4 0%,#ead9c5 100%); border:1px solid #e1d2c1; border-radius:28px; padding:28px 24px; box-shadow: 0 18px 45px rgba(74,52,34,.08); margin-bottom:18px; }
    .hero h1 { margin:0 0 12px 0; font-size:2.1rem; line-height:1.1; color:#171717; }
    .hero p { margin:0; color:#6d6258; font-size:1.05rem; }
    .grid { display:grid; grid-template-columns: repeat(2, 1fr); gap:12px; margin:16px 0; }
    .kpi { background:#fffdf8; border:1px solid #e5d9cb; border-radius:22px; padding:18px 10px; text-align:center; box-shadow:0 8px 25px rgba(74,52,34,.06); }
    .kpi strong { display:block; font-size:2rem; color:#6f5591; }
    .kpi span { color:#4d4640; font-size:.95rem; }
    .card { background:#fffdf8; border:1px solid #e3d6c8; border-radius:24px; padding:22px; box-shadow:0 14px 40px rgba(74,52,34,.07); margin:16px 0; }
    .card h2, .card h3 { margin-top:0; color:#171717; }
    .chip { display:inline-block; padding:8px 14px; margin:4px 5px 4px 0; border-radius:999px; background:#eadbcb; border:1px solid #dbc8b5; color:#3b342e; }
    .voice-button { position: fixed; right: 22px; bottom: 24px; z-index: 999; width:76px; height:76px; border-radius:26px; background:#1f1c19; color:white; display:flex; align-items:center; justify-content:center; font-size:2.2rem; box-shadow:0 12px 35px rgba(0,0,0,.28); border:8px solid rgba(255,255,255,.55); }
    .note { color:#6d6258; font-size:.95rem; }
    div[data-testid="stSelectbox"] { background:#fffdf8; border:1px solid #e5d9cb; border-radius:16px; padding:4px 10px 8px 10px; }
    @media (max-width: 600px) {
      .hero h1 { font-size:1.8rem; }
      .block-container { padding-left: 1rem; padding-right: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

PAGES = [
    "Centro de Operaciones", "Semillero", "Tareas", "Radar", "Estudio",
    "Calendario", "Relaciones", "Libros y relatos", "Ideas para la app", "Ajustes"
]

# ---------- NAVEGACIÓN ----------
st.markdown('<div class="topbar"><div class="brand">🧭 IZ</div><div class="version">V2.4 estable</div></div>', unsafe_allow_html=True)
selected = st.selectbox("☰ Menú", PAGES, index=PAGES.index(st.session_state.page), label_visibility="collapsed")
st.session_state.page = selected
st.markdown('<div class="voice-button">🎙️</div>', unsafe_allow_html=True)

# ---------- HELPERS ----------
def kpis():
    tareas_pend = sum(1 for t in st.session_state.tareas if not t["done"])
    semillas = len(st.session_state.semillero)
    oportunidades = 4
    eventos = 2
    st.markdown(f"""
    <div class="grid">
      <div class="kpi"><strong>{tareas_pend}</strong><span>Tareas</span></div>
      <div class="kpi"><strong>{semillas}</strong><span>Semillas</span></div>
      <div class="kpi"><strong>{oportunidades}</strong><span>Oportunidades</span></div>
      <div class="kpi"><strong>{eventos}</strong><span>Eventos</span></div>
    </div>
    """, unsafe_allow_html=True)

def card(title, body):
    st.markdown(f'<div class="card"><h3>{title}</h3>{body}</div>', unsafe_allow_html=True)

# ---------- PÁGINAS ----------
def page_centro():
    st.markdown('<div class="hero"><h1>Centro de Operaciones</h1><p>Buenos días, Irene · Aquí está lo que necesita tu atención.</p></div>', unsafe_allow_html=True)
    kpis()
    card("🎯 Prioridad del día", "<p>• Preparar base de contactos<br>• Crear banco de contenidos<br>• Revisar agenda cultural</p>")
    card("🔥 Radar rápido", "<p>4 oportunidades detectadas para revisar esta semana.</p><span class='chip'>Madrid</span><span class='chip'>Librerías</span><span class='chip'>Concursos</span>")
    card("📚 Libro activo", "<p><strong>El libro mágico de Hugo e Inés</strong><br>Fase: preparación de publicación.</p>")
    if st.session_state.semillero:
        ultima = st.session_state.semillero[0]
        card("🎙️ Última nota / semilla", f"<p>{ultima['texto']}</p><p class='note'>Estado: {ultima['estado']}</p>")

def page_semillero():
    st.markdown('<div class="hero"><h1>🌱 Semillero</h1><p>Todo lo que aún no tiene destino definitivo entra aquí.</p></div>', unsafe_allow_html=True)
    tipo = st.selectbox("Tipo", ["Nota de voz", "Idea", "Contacto", "Evento", "Noticia", "Concurso", "Tarea"])
    texto = st.text_area("Contenido", placeholder="Guarda aquí algo que todavía no sabes dónde colocar...")
    if st.button("Guardar en Semillero") and texto.strip():
        st.session_state.semillero.insert(0, {"tipo": tipo, "texto": texto.strip(), "estado": "Por organizar"})
        st.success("Guardado en Semillero")
    for item in st.session_state.semillero:
        card(f"{item['tipo']}", f"<p>{item['texto']}</p><span class='chip'>{item['estado']}</span>")

def page_tareas():
    st.markdown('<div class="hero"><h1>✅ Tareas</h1><p>Acciones concretas para avanzar sin dispersarte.</p></div>', unsafe_allow_html=True)
    nueva = st.text_input("Nueva tarea")
    if st.button("Añadir tarea") and nueva.strip():
        st.session_state.tareas.append({"texto": nueva.strip(), "done": False})
        st.success("Tarea añadida")
    st.markdown('<div class="card"><h3>🔥 Hoy</h3>', unsafe_allow_html=True)
    for i, tarea in enumerate(st.session_state.tareas):
        st.session_state.tareas[i]["done"] = st.checkbox(tarea["texto"], value=tarea["done"], key=f"tarea_{i}")
    st.markdown('</div>', unsafe_allow_html=True)

def page_radar():
    st.markdown('<div class="hero"><h1>🧭 Radar</h1><p>Oportunidades literarias, culturales y de visibilidad.</p></div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["⭐ Recomendado", "🎤 Eventos", "🏆 Concursos", "📰 Noticias"])
    with tab1:
        card("Oportunidad", "<p>Presentación en FNAC Callao · Madrid</p><span class='chip'>Revisar</span>")
        card("Oportunidad", "<p>Buscar eventos de librerías en Getafe/Leganés</p><span class='chip'>Madrid sur</span>")
    with tab2:
        card("Evento", "<p>Presentación literaria · viernes 19:00</p>")
    with tab3:
        card("Concurso", "<p>Concurso de relato histórico · cierra en 16 días</p>")
    with tab4:
        card("Noticia", "<p>Pendiente conectar fuentes de noticias reales.</p>")

def page_estudio():
    st.markdown('<div class="hero"><h1>🎬 Estudio</h1><p>Banco de contenidos y producción editorial.</p></div>', unsafe_allow_html=True)
    card("💡 Ideas", "<p>• Vídeo: una foto, una historia<br>• ¿Sabías que...? libros antiguos<br>• Por qué Irene Zurilla escribe</p>")
    card("🎙️ Grabar", "<p>Curiosidad: primer bestseller<br>Vídeo: por qué me gusta la historia</p>")
    card("📅 Programado", "<p>Post domingo · Cuentos Tita Nene</p>")

def page_calendario():
    st.markdown('<div class="hero"><h1>📅 Calendario</h1><p>Fechas, publicaciones, eventos y campañas.</p></div>', unsafe_allow_html=True)
    card("Esta semana", "<p>Viernes: Radar del fin de semana<br>Domingo: Reunión de Dirección</p>")
    card("Fechas clave", "<p>23 abril · Día del Libro<br>Navidad · campaña de cierre de año</p>")

def page_relaciones():
    st.markdown('<div class="hero"><h1>🤝 Relaciones</h1><p>Contactos, librerías, bibliotecas, prensa y autores.</p></div>', unsafe_allow_html=True)
    card("Librerías", "<p>Librería Cervantes · seguimiento pendiente</p>")
    card("Bibliotecas", "<p>Biblioteca Getafe · contacto por iniciar</p>")

def page_libros():
    st.markdown('<div class="hero"><h1>📚 Libros y relatos</h1><p>Todo lo terminado, publicado o no.</p></div>', unsafe_allow_html=True)
    card("El libro mágico de Hugo e Inés", "<p>Tipo: cuento infantil<br>Estado: preparación de publicación</p>")
    card("Preludio de un ocaso", "<p>Tipo: relato<br>Estado: terminado / concursos</p>")
    card("Añadir obra", "<p>Próxima mejora: formulario para libros, cuentos y relatos.</p>")

def page_ideas_app():
    st.markdown('<div class="hero"><h1>💡 Ideas para la app</h1><p>Mejoras que se te ocurren mientras la usas.</p></div>', unsafe_allow_html=True)
    idea = st.text_input("Nueva idea para la app")
    if st.button("Guardar idea") and idea.strip():
        st.session_state.ideas_app.insert(0, {"texto": idea.strip(), "estado": "Nueva"})
        st.success("Idea guardada")
    for item in st.session_state.ideas_app:
        card(item["texto"], f"<span class='chip'>{item['estado']}</span>")

def page_ajustes():
    st.markdown('<div class="hero"><h1>⚙️ Ajustes</h1><p>Configuración y conexión futura con Drive.</p></div>', unsafe_allow_html=True)
    card("Google Drive", "<p>Próxima fase: conectar datos vivos a Drive/Sheets.</p>")
    card("Versión", "<p>V2.4 estable · Base segura para seguir desarrollando.</p>")

pages = {
    "Centro de Operaciones": page_centro,
    "Semillero": page_semillero,
    "Tareas": page_tareas,
    "Radar": page_radar,
    "Estudio": page_estudio,
    "Calendario": page_calendario,
    "Relaciones": page_relaciones,
    "Libros y relatos": page_libros,
    "Ideas para la app": page_ideas_app,
    "Ajustes": page_ajustes,
}
pages[st.session_state.page]()
