import streamlit as st
from datetime import datetime

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")

st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #fbf6ee 0%, #f3eadf 100%); }
    .block-container { padding-top: 1.2rem; padding-bottom: 7rem; max-width: 760px; }
    h1, h2, h3 { color: #201c19; }
    .hero { background:#eadccb; padding:28px 28px; border-radius:30px; border:1px solid #ddccba; margin-bottom:22px; }
    .hero h1 { margin:0; font-size:38px; line-height:1.1; }
    .hero p { margin:14px 0 0 0; color:#6d625a; font-size:18px; }
    .card { background:#fffaf2; border:1px solid #e1d2c2; border-radius:26px; padding:22px; margin:16px 0; box-shadow:0 12px 30px rgba(80,55,25,.06); }
    .mini-grid { display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; margin:18px 0; }
    .kpi { background:#efe3d6; border:1px solid #dfcfbd; border-radius:18px; padding:14px 8px; text-align:center; }
    .kpi strong { display:block; font-size:26px; color:#5b4770; }
    .kpi span { display:block; font-size:13px; color:#403a35; margin-top:4px; }
    .chip { display:inline-block; background:#eadccb; border:1px solid #d8c6b5; border-radius:999px; padding:8px 14px; margin:4px 4px 4px 0; }
    .voice { position:fixed; right:24px; bottom:24px; width:86px; height:86px; border-radius:28px; background:#171310; color:white; display:flex; align-items:center; justify-content:center; font-size:40px; box-shadow:0 12px 30px rgba(0,0,0,.25); z-index:9999; }
    @media (max-width: 640px) {
      .block-container { padding-left: 1rem; padding-right: 1rem; }
      .hero h1 { font-size:32px; }
      .mini-grid { grid-template-columns: repeat(2, 1fr); }
      .voice { width:78px; height:78px; font-size:36px; right:18px; bottom:20px; }
    }
</style>
""", unsafe_allow_html=True)

if "items" not in st.session_state:
    st.session_state.items = [
        {"tipo": "Nota de voz", "texto": "Idea para vídeo: ¿sabías que...? sobre libros antiguos", "estado": "Por organizar"},
        {"tipo": "Idea", "texto": "Crear serie de vídeos sobre historia y libros", "estado": "Por organizar"},
    ]
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"texto": "Revisar calendario + noticias", "done": False},
        {"texto": "Preparar base de contactos", "done": False},
        {"texto": "Crear banco de contenidos", "done": False},
    ]
if "suggestions" not in st.session_state:
    st.session_state.suggestions = ["Menú de tres puntos más compacto", "Mejorar grabación de notas de voz"]

MODULES = [
    "Centro de Operaciones", "Semillero", "Tareas", "Radar", "Estudio", "Calendario", "Relaciones", "Libros y relatos", "Ideas para la app", "Ajustes"
]

st.markdown("<div style='display:flex;align-items:center;gap:10px;margin-bottom:10px;'><div style='font-size:34px'>🧭</div><h2 style='margin:0'>IZ</h2><span style='margin-left:auto;background:#f0e5db;border:1px solid #ddccba;border-radius:20px;padding:8px 14px'>V2.2 stable</span></div>", unsafe_allow_html=True)
page = st.selectbox("☰ Menú", MODULES, label_visibility="collapsed")


def hero(title, subtitle):
    st.markdown(f"<div class='hero'><h1>{title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)


def kpis():
    pendientes = sum(1 for t in st.session_state.tasks if not t["done"])
    semillas = len(st.session_state.items)
    st.markdown(
        f"""
        <div class='mini-grid'>
          <div class='kpi'><strong>{pendientes}</strong><span>Tareas</span></div>
          <div class='kpi'><strong>{semillas}</strong><span>Semillero</span></div>
          <div class='kpi'><strong>4</strong><span>Radar</span></div>
          <div class='kpi'><strong>2</strong><span>Eventos</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def centro():
    hero("Centro de Operaciones", "Buenos días, Irene · Aquí está lo que necesita tu atención.")
    kpis()
    st.markdown("<div class='card'><h3>🎯 Prioridad del día</h3><p>Preparar base de contactos · Crear banco de contenidos · Revisar agenda cultural.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>🔥 Radar rápido</h3><p>4 oportunidades detectadas para revisar esta semana.</p><span class='chip'>Madrid</span><span class='chip'>Librerías</span><span class='chip'>Concursos</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>📚 Libro activo</h3><p><b>El libro mágico de Hugo e Inés</b><br>Fase: publicación / preparación de campaña.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>🎙️ Última nota de voz</h3><p>Idea para vídeo: ¿sabías que...? sobre libros antiguos</p></div>", unsafe_allow_html=True)


def semillero():
    hero("🌱 Semillero", "Notas, ideas y oportunidades pendientes de organizar.")
    tipo = st.selectbox("Tipo", ["Nota de voz", "Idea", "Contacto", "Evento", "Noticia", "Concurso", "Recordatorio"])
    texto = st.text_area("Contenido", placeholder="Guarda aquí algo que todavía no sabes dónde colocar...")
    if st.button("Guardar en Semillero") and texto.strip():
        st.session_state.items.insert(0, {"tipo": tipo, "texto": texto.strip(), "estado": "Por organizar"})
        st.success("Guardado en Semillero")
    for item in st.session_state.items:
        st.markdown(f"<div class='card'><h3>{item['tipo']}</h3><p>{item['texto']}</p><span class='chip'>{item['estado']}</span></div>", unsafe_allow_html=True)


def tareas():
    hero("✅ Tareas", "Organiza lo importante sin convertirlo en ruido.")
    nueva = st.text_input("Nueva tarea")
    if st.button("Añadir tarea") and nueva.strip():
        st.session_state.tasks.append({"texto": nueva.strip(), "done": False})
        st.success("Tarea añadida")
    st.markdown("<div class='card'><h3>🔥 Hoy</h3></div>", unsafe_allow_html=True)
    for i, task in enumerate(st.session_state.tasks):
        st.session_state.tasks[i]["done"] = st.checkbox(task["texto"], value=task["done"], key=f"task_{i}")


def radar():
    hero("🧭 Radar", "Oportunidades, eventos y señales del mundo literario.")
    tabs = st.tabs(["⭐ Recomendado", "🎤 Eventos", "🏆 Concursos", "📰 Noticias"])
    with tabs[0]:
        for texto in ["Presentación en FNAC Callao · Madrid", "Concurso de relato histórico · cierra en 16 días", "Buscar eventos de librerías en Getafe/Leganés"]:
            st.markdown(f"<div class='card'><h3>Oportunidad</h3><p>{texto}</p><span class='chip'>Revisar</span></div>", unsafe_allow_html=True)
    with tabs[1]:
        st.info("Aquí irán las presentaciones y eventos culturales.")
    with tabs[2]:
        st.info("Aquí irán concursos y convocatorias.")
    with tabs[3]:
        st.info("Aquí irán noticias del mundo editorial y literario.")


def estudio():
    hero("🎬 Estudio", "Banco de contenidos y producción editorial.")
    for titulo, num in [("Ideas", 12), ("Guiones", 4), ("Pendientes de grabar", 6), ("Programados", 3)]:
        st.markdown(f"<div class='card'><h3>{titulo}</h3><p>{num} elementos</p></div>", unsafe_allow_html=True)


def calendario():
    hero("📅 Calendario", "Fechas clave, publicaciones, eventos y campaña.")
    st.markdown("<div class='card'><h3>Esta semana</h3><p>Viernes: Radar del fin de semana<br>Domingo: Reunión de Dirección</p></div>", unsafe_allow_html=True)


def relaciones():
    hero("🤝 Relaciones", "Contactos profesionales, librerías, bibliotecas y autores.")
    for c in ["Librería pendiente de visitar", "Biblioteca Getafe", "Editorial / contacto general"]:
        st.markdown(f"<div class='card'><h3>{c}</h3><p>Seguimiento pendiente</p></div>", unsafe_allow_html=True)


def libros():
    hero("📚 Libros y relatos", "Obras terminadas, publicadas o pendientes de publicar.")
    obras = ["El libro mágico de Hugo e Inés", "Preludio de un ocaso", "Relatos terminados pendientes de clasificar"]
    for obra in obras:
        st.markdown(f"<div class='card'><h3>{obra}</h3><p>Estado: en seguimiento</p></div>", unsafe_allow_html=True)


def ideas_app():
    hero("💡 Ideas para la app", "Mejoras que se te ocurran mientras la usas.")
    idea = st.text_input("Nueva idea para la app")
    if st.button("Guardar idea") and idea.strip():
        st.session_state.suggestions.insert(0, idea.strip())
        st.success("Idea guardada")
    for idea in st.session_state.suggestions:
        st.markdown(f"<div class='card'><p>{idea}</p><span class='chip'>Nueva</span></div>", unsafe_allow_html=True)


def ajustes():
    hero("⚙️ Ajustes", "Configuración, Drive y futuras integraciones.")
    st.info("Pendiente: conexión con Google Drive y copias de seguridad.")


if page == "Centro de Operaciones":
    centro()
elif page == "Semillero":
    semillero()
elif page == "Tareas":
    tareas()
elif page == "Radar":
    radar()
elif page == "Estudio":
    estudio()
elif page == "Calendario":
    calendario()
elif page == "Relaciones":
    relaciones()
elif page == "Libros y relatos":
    libros()
elif page == "Ideas para la app":
    ideas_app()
else:
    ajustes()

st.markdown("<div class='voice'>🎙️</div>", unsafe_allow_html=True)
