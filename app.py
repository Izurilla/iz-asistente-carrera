import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="IZ | Asistente de Carrera",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

VERSION = "V1.4 stable"

# -----------------------------
# Estado inicial seguro
# -----------------------------
def init_state():
    defaults = {
        "semillero": [
            {"tipo": "🎙️ Nota de voz", "texto": "Idea para vídeo: ¿sabías que...? sobre libros antiguos", "estado": "Por organizar"},
            {"tipo": "💡 Idea", "texto": "Crear banco de contenidos de septiembre", "estado": "Por organizar"},
        ],
        "tareas_hoy": [
            "Revisar calendario + noticias",
            "Preparar base de contactos",
            "Crear banco de contenidos",
        ],
        "oportunidades": [
            "Presentación en FNAC Callao · Madrid",
            "Concurso de relato histórico · cierra en 16 días",
            "Buscar eventos de librerías en Getafe/Leganés",
            "Agenda cultural de Madrid para el fin de semana",
        ],
        "ideas_app": [
            "Añadir módulo de noticias reales",
            "Crear calendario mensual",
            "Mejorar botón de notas de voz",
        ],
        "contactos": [
            "Librerías Madrid / Getafe / Leganés",
            "Bibliotecas Comunidad de Madrid",
            "Autores y presentaciones literarias",
        ],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# -----------------------------
# Estilos
# -----------------------------
st.markdown(
    """
    <style>
    :root { --bg:#fbf4ea; --card:#fffaf3; --ink:#211f1c; --muted:#6f655b; --line:#e7d8c8; --accent:#2a2340; --soft:#efe3d4; }
    html, body, [data-testid="stAppViewContainer"] { background: radial-gradient(circle at top, #fff9f0 0%, #f8efe4 45%, #f4eadf 100%); }
    [data-testid="stHeader"] { background: rgba(255,255,255,0); }
    .block-container { padding-top: 1.1rem; padding-bottom: 6.5rem; max-width: 760px; }
    h1, h2, h3, p, div, span, label { font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
    .hero { background: linear-gradient(135deg, #f4e4d2, #fffaf3); border:1px solid var(--line); border-radius:28px; padding:26px 28px; box-shadow:0 18px 45px rgba(78,54,30,.08); margin-bottom:18px; }
    .hero h1 { margin:0; font-size:34px; letter-spacing:-.04em; color:var(--ink); }
    .hero p { color:var(--muted); font-size:17px; margin:.55rem 0 0; }
    .grid { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin:14px 0 18px; }
    .kpi { background:rgba(255,250,243,.9); border:1px solid var(--line); border-radius:22px; padding:18px 10px; text-align:center; box-shadow:0 12px 28px rgba(78,54,30,.05); }
    .kpi strong { display:block; font-size:30px; color:#5a4673; line-height:1; }
    .kpi span { display:block; color:var(--ink); margin-top:7px; font-size:15px; }
    .card { background:rgba(255,250,243,.95); border:1px solid var(--line); border-radius:24px; padding:20px; margin:14px 0; box-shadow:0 14px 34px rgba(78,54,30,.07); }
    .card h2 { margin:0 0 12px 0; font-size:24px; color:var(--ink); }
    .pill { display:inline-block; background:#efe3d4; border:1px solid #e5d3bf; padding:8px 12px; border-radius:999px; font-size:13px; margin:4px 4px 4px 0; }
    .nav { position:fixed; bottom:0; left:0; right:0; background:rgba(255,250,243,.96); border-top:1px solid #eadccb; padding:10px 10px 16px; z-index:999; box-shadow:0 -10px 32px rgba(78,54,30,.08); }
    .mic { position:fixed; bottom:58px; left:50%; transform:translateX(-50%); width:76px; height:76px; border-radius:28px; background:#211f1c; color:white; display:flex; align-items:center; justify-content:center; font-size:34px; z-index:1000; box-shadow:0 16px 44px rgba(0,0,0,.25); border:8px solid rgba(255,250,243,.9); }
    .small { color:var(--muted); font-size:14px; }
    @media (max-width: 520px) { .hero h1 {font-size:28px;} .grid {gap:8px;} .kpi strong {font-size:26px;} .block-container {padding-left:1rem; padding-right:1rem;} }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Navegación
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Centro"


def nav_button(label, page):
    if st.button(label, use_container_width=True, key=f"nav_{page}"):
        st.session_state.page = page
        st.rerun()


def bottom_nav():
    st.markdown('<div class="mic">🎙️</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav">', unsafe_allow_html=True)
    cols = st.columns(5)
    with cols[0]: nav_button("🏠 Centro", "Centro")
    with cols[1]: nav_button("🌱 Semillero", "Semillero")
    with cols[2]: nav_button("✅ Tareas", "Tareas")
    with cols[3]: nav_button("🧭 Radar", "Radar")
    with cols[4]: nav_button("☰ Más", "Mas")
    st.markdown('</div>', unsafe_allow_html=True)


def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def render_card(title, body_html):
    st.markdown(f'<div class="card"><h2>{title}</h2>{body_html}</div>', unsafe_allow_html=True)

# -----------------------------
# Páginas
# -----------------------------
def page_centro():
    hero("Centro de Operaciones", f"Buenos días, Irene · {VERSION}")
    st.markdown(
        f"""
        <div class="grid">
            <div class="kpi"><strong>{len(st.session_state.tareas_hoy)}</strong><span>Tareas</span></div>
            <div class="kpi"><strong>{len(st.session_state.semillero)}</strong><span>Semillas</span></div>
            <div class="kpi"><strong>{len(st.session_state.oportunidades)}</strong><span>Oportunidades</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_card("🧭 Brújula", "<p>Esta semana no intentaría hacerlo todo. Prioridad: dejar estable el sistema y empezar a mover la marca.</p>")
    st.markdown('<div class="card"><h2>🎯 Prioridades</h2>', unsafe_allow_html=True)
    for tarea in st.session_state.tareas_hoy[:3]:
        st.checkbox(tarea, key=f"centro_{tarea}")
    st.markdown('</div>', unsafe_allow_html=True)
    render_card("🌱 Semillero", f"<p>{len(st.session_state.semillero)} elementos por organizar.</p><span class='pill'>Notas de voz</span><span class='pill'>Ideas</span><span class='pill'>Contactos</span>")
    render_card("🔥 Radar rápido", "<p>4 oportunidades detectadas para revisar esta semana.</p><span class='pill'>Madrid</span><span class='pill'>Librerías</span><span class='pill'>Concursos</span>")


def page_semillero():
    hero("Semillero", "Notas, ideas y oportunidades pendientes de organizar.")
    with st.form("nueva_semilla", clear_on_submit=True):
        tipo = st.selectbox("Tipo", ["🎙️ Nota de voz", "💡 Idea", "👤 Contacto", "📅 Evento", "📰 Noticia", "🏆 Concurso", "📌 Tarea"])
        texto = st.text_area("Contenido", placeholder="Escribe aquí lo que quieres guardar...")
        submitted = st.form_submit_button("Guardar en Semillero")
        if submitted and texto.strip():
            st.session_state.semillero.insert(0, {"tipo": tipo, "texto": texto.strip(), "estado": "Por organizar"})
            st.success("Guardado en Semillero")
    for i, item in enumerate(st.session_state.semillero):
        render_card(f"{item['tipo']}", f"<p>{item['texto']}</p><span class='pill'>{item['estado']}</span>")


def page_tareas():
    hero("Tareas", "Lo que toca hacer, sin ruido.")
    with st.form("nueva_tarea", clear_on_submit=True):
        nueva = st.text_input("Nueva tarea")
        if st.form_submit_button("Añadir tarea") and nueva.strip():
            st.session_state.tareas_hoy.append(nueva.strip())
            st.success("Tarea añadida")
    st.markdown('<div class="card"><h2>🔥 Hoy</h2>', unsafe_allow_html=True)
    for tarea in st.session_state.tareas_hoy:
        st.checkbox(tarea, key=f"tarea_{tarea}")
    st.markdown('</div>', unsafe_allow_html=True)
    render_card("📅 Esta semana", "<p>Preparar base de contactos · Crear banco de contenidos · Revisar agenda cultural.</p>")
    render_card("⏳ Próximamente", "<p>Dossier de autora · Registro de marca · Calendario editorial de septiembre.</p>")


def page_radar():
    hero("Radar", "Oportunidades que pueden mover tu carrera.")
    tabs = st.tabs(["⭐ Recomendado", "🎤 Eventos", "🏆 Concursos", "📰 Noticias"])
    with tabs[0]:
        for op in st.session_state.oportunidades:
            render_card("Oportunidad", f"<p>{op}</p><span class='pill'>Revisar</span>")
    with tabs[1]:
        st.write("Presentaciones, librerías, bibliotecas y vida cultural de Madrid.")
    with tabs[2]:
        st.write("Concursos literarios y convocatorias para autora.")
    with tabs[3]:
        st.write("Noticias del sector editorial y cultural.")


def page_mas():
    hero("Más", "Módulos en construcción.")
    option = st.radio("Abrir", ["🎬 Estudio", "📚 Libros", "🤝 Relaciones", "📅 Calendario", "📈 Dirección", "💡 Ideas para la app"], label_visibility="collapsed")
    if option == "💡 Ideas para la app":
        with st.form("idea_app", clear_on_submit=True):
            idea = st.text_input("Nueva idea para mejorar la app")
            if st.form_submit_button("Guardar idea") and idea.strip():
                st.session_state.ideas_app.append(idea.strip())
                st.success("Idea guardada")
        for idea in st.session_state.ideas_app:
            render_card("💡 Idea para la app", f"<p>{idea}</p><span class='pill'>Nueva</span>")
    elif option == "🤝 Relaciones":
        for contacto in st.session_state.contactos:
            render_card("Contacto / categoría", f"<p>{contacto}</p>")
    elif option == "📚 Libros":
        render_card("📖 Libro activo", "<p>El libro mágico de Hugo e Inés</p><span class='pill'>Campaña inicial</span><span class='pill'>Presentaciones</span>")
    elif option == "🎬 Estudio":
        render_card("🎬 Estudio Editorial", "<p>Ideas · Guiones · Grabar · Editar · Programar · Publicado</p>")
    elif option == "📅 Calendario":
        render_card("📅 Calendario", "<p>Próxima fase: vista semanal y mensual.</p>")
    elif option == "📈 Dirección":
        render_card("📈 Dirección", "<p>Domingo: reunión de dirección. Viernes: radar del fin de semana. Mensual: revisión estratégica.</p>")

# -----------------------------
# Render
# -----------------------------
page = st.session_state.page
if page == "Centro":
    page_centro()
elif page == "Semillero":
    page_semillero()
elif page == "Tareas":
    page_tareas()
elif page == "Radar":
    page_radar()
elif page == "Mas":
    page_mas()

bottom_nav()
