import streamlit as st
from datetime import date

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")

if "items" not in st.session_state:
    st.session_state.items = [
        {"tipo": "🎙️ Nota", "texto": "Preparar ideas de septiembre", "estado": "Sin organizar"},
        {"tipo": "💡 Idea", "texto": "Vídeo: una foto, una historia", "estado": "Sin organizar"},
    ]
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"texto": "Preparar base de contactos", "done": False},
        {"texto": "Crear banco de contenidos", "done": False},
        {"texto": "Revisar agenda cultural", "done": False},
    ]
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

CSS = """
<style>
[data-testid="stAppViewContainer"] { background: #f7efe4; }
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 760px; padding-top: 1rem; padding-bottom: 7rem; }
.hero { background: linear-gradient(135deg,#fffaf2,#eadbc8); border: 1px solid #ead9c6; border-radius: 28px; padding: 24px; box-shadow: 0 18px 40px rgba(66,43,20,.08); margin-bottom: 18px; }
.hero h1 { margin: 0; font-size: 34px; line-height: 1.05; }
.hero p { color:#776b60; font-size: 18px; margin-bottom: 0; }
.kpi-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 14px 0 18px; }
.kpi { background:#efe4d7; border-radius:22px; padding:16px 10px; text-align:center; box-shadow: inset 0 0 0 1px rgba(70,40,20,.04); }
.kpi strong { display:block; font-size:30px; color:#5d4a7d; }
.kpi span { font-size:15px; color:#2f2924; }
.card { background: rgba(255,252,246,.95); border: 1px solid #e8d8c5; border-radius: 24px; padding: 20px; margin: 14px 0; box-shadow: 0 15px 35px rgba(66,43,20,.06); }
.card h2, .card h3 { margin-top:0; }
.nav { position: fixed; left: 0; right: 0; bottom: 0; z-index: 999; background: rgba(255,250,242,.96); border-top: 1px solid #e6d6c4; padding: 10px 8px 12px; display:flex; justify-content:center; gap:8px; }
.nav a { text-decoration:none; color:#2b2723; background:#fff; border:1px solid #e0d0bd; border-radius:16px; padding:10px 12px; font-weight:650; font-size:14px; min-width:82px; text-align:center; }
.mic { position: fixed; left: 50%; bottom: 48px; transform: translateX(-50%); z-index:1000; width:76px; height:76px; border-radius:28px; background:#211d18; color:#fff; display:flex; align-items:center; justify-content:center; font-size:34px; box-shadow: 0 14px 30px rgba(0,0,0,.28); border:8px solid rgba(255,255,255,.75); }
.small { color:#7b6f64; font-size:14px; }
.badge { display:inline-block; padding: 6px 10px; border-radius: 999px; background:#efe4d7; margin-right:6px; margin-bottom:6px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

PAGES = ["Centro", "Semillero", "Tareas", "Radar", "Estudio", "Más"]
page = st.query_params.get("page", "Centro")
if page not in PAGES:
    page = "Centro"


def nav():
    st.markdown(
        """
        <a class="mic" href="?page=Semillero">🎙️</a>
        <div class="nav">
            <a href="?page=Centro">🏠 Centro</a>
            <a href="?page=Tareas">✅ Tareas</a>
            <a href="?page=Radar">🧭 Radar</a>
            <a href="?page=Estudio">🎬 Estudio</a>
            <a href="?page=Más">☰ Más</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def centro():
    st.markdown(
        """
        <div class="hero">
          <h1>Centro de Operaciones</h1>
          <p>Buenos días, Irene · Aquí está lo que necesita tu atención.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    tareas_pendientes = sum(1 for t in st.session_state.tasks if not t.get("done"))
    semillas = len(st.session_state.items)
    oportunidades = 4
    st.markdown(
        f"""
        <div class="kpi-grid">
          <div class="kpi"><strong>{tareas_pendientes}</strong><span>Tareas</span></div>
          <div class="kpi"><strong>{semillas}</strong><span>Semillas</span></div>
          <div class="kpi"><strong>{oportunidades}</strong><span>Oportunidades</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="card"><h2>🎯 Prioridades</h2><p>• Preparar base de contactos<br>• Crear banco de contenidos<br>• Revisar agenda cultural</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h2>🧭 Brújula</h2><p>Esta semana no intentaría hacerlo todo. Prioridad: dejar listo el sistema y empezar a mover la marca.</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card"><h2>🌱 Semillero</h2><p>{semillas} elementos por organizar.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h2>🔥 Radar rápido</h2><p>• Presentación en FNAC Callao · Madrid<br>• Concurso de relato histórico · cierra en 16 días<br>• Buscar eventos en Getafe/Leganés</p></div>', unsafe_allow_html=True)


def semillero():
    st.markdown('<div class="hero"><h1>🌱 Semillero</h1><p>Notas, ideas y oportunidades antes de organizarlas.</p></div>', unsafe_allow_html=True)
    with st.form("new_item", clear_on_submit=True):
        tipo = st.selectbox("Tipo", ["🎙️ Nota de voz", "💡 Idea", "📅 Evento", "👤 Contacto", "📰 Noticia", "🏆 Concurso", "📌 Tarea"])
        texto = st.text_area("Nota", placeholder="Escribe o transcribe aquí lo que quieras guardar...")
        submitted = st.form_submit_button("Guardar en Semillero")
        if submitted and texto.strip():
            st.session_state.items.insert(0, {"tipo": tipo, "texto": texto.strip(), "estado": "Sin organizar"})
            st.success("Guardado en Semillero")
    st.subheader("Por organizar")
    for i, item in enumerate(st.session_state.items):
        st.markdown(f"""
        <div class="card"><h3>{item['tipo']}</h3><p>{item['texto']}</p><span class="badge">{item['estado']}</span></div>
        """, unsafe_allow_html=True)


def tareas():
    st.markdown('<div class="hero"><h1>✅ Tareas</h1><p>Hoy, esta semana y próximos pasos.</p></div>', unsafe_allow_html=True)
    new_task = st.text_input("Nueva tarea")
    if st.button("Añadir tarea") and new_task.strip():
        st.session_state.tasks.append({"texto": new_task.strip(), "done": False})
        st.rerun()
    st.subheader("Pendientes")
    for i, t in enumerate(st.session_state.tasks):
        done = st.checkbox(t["texto"], value=t["done"], key=f"task_{i}")
        st.session_state.tasks[i]["done"] = done


def radar():
    st.markdown('<div class="hero"><h1>🧭 Radar</h1><p>Oportunidades para Irene Zurilla.</p></div>', unsafe_allow_html=True)
    for title, meta in [
        ("Presentación en FNAC Callao", "Madrid · viernes · 19:00"),
        ("Concurso de relato histórico", "Online · cierra en 16 días"),
        ("Agenda cultural Getafe/Leganés", "Revisar este viernes"),
        ("Librerías independientes Madrid", "Crear lista de favoritos"),
    ]:
        st.markdown(f'<div class="card"><h3>{title}</h3><p>{meta}</p></div>', unsafe_allow_html=True)


def estudio():
    st.markdown('<div class="hero"><h1>🎬 Estudio</h1><p>Banco de contenidos y producción.</p></div>', unsafe_allow_html=True)
    cols = st.columns(2)
    cols[0].metric("Ideas", "27")
    cols[1].metric("Pendientes de grabar", "8")
    st.markdown('<div class="card"><h3>Ideas de esta semana</h3><p>• ¿Sabías que...? libros antiguos<br>• Una foto, una historia<br>• Por qué Irene Zurilla escribe</p></div>', unsafe_allow_html=True)


def mas():
    st.markdown('<div class="hero"><h1>☰ Más</h1><p>Módulos de gestión.</p></div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Libros", "🤝 Relaciones", "💡 Ideas app", "📈 Dirección"])
    with tab1:
        st.markdown('<div class="card"><h3>Libro activo</h3><p>El libro mágico de Hugo e Inés · Campaña en preparación</p></div>', unsafe_allow_html=True)
    with tab2:
        st.markdown('<div class="card"><h3>Contactos prioritarios</h3><p>Librerías · Bibliotecas · Editorial · Prensa</p></div>', unsafe_allow_html=True)
    with tab3:
        idea = st.text_input("Nueva idea para mejorar la app")
        if st.button("Guardar idea") and idea.strip():
            st.session_state.suggestions.insert(0, idea.strip())
            st.success("Idea guardada")
        for s in st.session_state.suggestions:
            st.write("💡", s)
    with tab4:
        st.markdown('<div class="card"><h3>Consejo de Dirección</h3><p>No añadimos funciones por añadir. Primero: que el Centro de Operaciones sea útil en móvil.</p></div>', unsafe_allow_html=True)


if page == "Centro":
    centro()
elif page == "Semillero":
    semillero()
elif page == "Tareas":
    tareas()
elif page == "Radar":
    radar()
elif page == "Estudio":
    estudio()
else:
    mas()

nav()
