import streamlit as st
from datetime import date

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")

st.markdown("""
<style>
:root{
  --bg:#f7efe6; --card:#fffaf4; --ink:#2b2520; --muted:#7a6d63;
  --accent:#4f3d63; --accent2:#8c6ca8; --line:#eaded1; --ok:#56745b;
}
html, body, [class*="css"]{font-family: Inter, system-ui, -apple-system, Segoe UI, sans-serif;}
.stApp{background:linear-gradient(180deg,#f8efe7 0%,#fdf8f3 100%); color:var(--ink);}
.block-container{padding-top:1.2rem; padding-bottom:7rem; max-width:760px;}
.iz-header{background:var(--card);border:1px solid var(--line);border-radius:28px;padding:22px;box-shadow:0 8px 28px rgba(60,40,25,.08);margin-bottom:14px;}
.iz-title{font-size:1.75rem;font-weight:800;margin:0;color:var(--ink);}
.iz-sub{color:var(--muted);margin-top:4px;font-size:.95rem;}
.card{background:var(--card);border:1px solid var(--line);border-radius:24px;padding:18px;margin:12px 0;box-shadow:0 6px 18px rgba(60,40,25,.055);}
.card h3{margin:0 0 10px 0;font-size:1.05rem;}
.pill{display:inline-block;background:#efe3f2;color:#4f3d63;border-radius:999px;padding:6px 10px;margin:4px 4px 4px 0;font-size:.82rem;font-weight:700;}
.small{color:var(--muted);font-size:.88rem;}
.metric-row{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;}
.metric{background:#f4eadf;border-radius:18px;padding:12px;text-align:center;}
.metric b{display:block;font-size:1.25rem;color:var(--accent)}
.nav-note{position:fixed;left:50%;transform:translateX(-50%);bottom:10px;z-index:999;background:#2b2520;color:white;border-radius:999px;padding:9px 14px;font-size:.82rem;box-shadow:0 8px 30px rgba(0,0,0,.2);}
button[kind="primary"]{background:#4f3d63!important;border-radius:16px!important;}
.stButton>button{border-radius:16px!important;border:1px solid var(--line)!important;}
textarea{border-radius:18px!important;}
</style>
""", unsafe_allow_html=True)

if "voice_notes" not in st.session_state:
    st.session_state.voice_notes = [
        {"tipo":"🎙️ Nota de voz", "titulo":"Idea para vídeo sobre bibliotecas históricas", "estado":"Sin organizar"},
        {"tipo":"💡 Idea", "titulo":"Serie: ¿sabías que...?", "estado":"Pendiente"},
    ]
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"txt":"Definir calendario editorial de septiembre", "done":False, "zona":"Hoy"},
        {"txt":"Crear lista inicial de librerías de Madrid", "done":False, "zona":"Semana"},
        {"txt":"Preparar dossier básico de autora", "done":False, "zona":"Próximamente"},
    ]
if "suggestions" not in st.session_state:
    st.session_state.suggestions = [
        {"txt":"Añadir calendario mensual real", "estado":"Nueva"},
        {"txt":"Conectar datos con Google Drive", "estado":"En estudio"},
    ]

PAGES = ["🏠 Centro de Operaciones", "🌱 Semillero", "✅ Tareas", "🧭 Radar", "📅 Calendario", "🎬 Estudio", "📚 Libros", "🤝 Relaciones", "💡 Ideas para la app"]

st.sidebar.title("🧭 IZ")
page = st.sidebar.radio("Navegación", PAGES, label_visibility="collapsed")
st.sidebar.caption("V1 Beta · Centro de Operaciones")


def header(title, sub=""):
    st.markdown(f"""<div class='iz-header'><p class='iz-title'>{title}</p><div class='iz-sub'>{sub}</div></div>""", unsafe_allow_html=True)

def card(title, body=""):
    st.markdown(f"<div class='card'><h3>{title}</h3>{body}</div>", unsafe_allow_html=True)

if page == "🏠 Centro de Operaciones":
    header("Centro de Operaciones", "Buenos días, Irene · Aquí está lo que necesita tu atención.")
    st.markdown("<div class='metric-row'><div class='metric'><b>3</b>Tareas</div><div class='metric'><b>2</b>Semillas</div><div class='metric'><b>4</b>Oportunidades</div></div>", unsafe_allow_html=True)
    card("🎯 Prioridades", "• Preparar base de contactos<br>• Crear banco de contenidos<br>• Revisar agenda cultural")
    card("🧭 Brújula", "Esta semana no intentaría hacerlo todo. Prioridad: dejar listo el sistema y empezar a mover la marca.")
    card("🌱 Semillero", f"{len(st.session_state.voice_notes)} elementos por organizar")
    card("🔥 Radar rápido", "• Presentaciones en Madrid<br>• Librerías para mapear<br>• Noticias editoriales para contenido")
    card("📚 Libro activo", "El libro mágico de Hugo e Inés · Campaña inicial en preparación")

elif page == "🌱 Semillero":
    header("Semillero", "Todo lo que capturas antes de decidir a dónde va.")
    with st.form("new_seed"):
        tipo = st.selectbox("Tipo", ["🎙️ Nota de voz", "💡 Idea", "👤 Contacto", "📅 Evento", "🏆 Concurso", "📰 Noticia"])
        titulo = st.text_input("Título o resumen")
        if st.form_submit_button("Guardar en Semillero", type="primary") and titulo:
            st.session_state.voice_notes.insert(0, {"tipo":tipo, "titulo":titulo, "estado":"Sin organizar"})
            st.success("Guardado en Semillero")
    for item in st.session_state.voice_notes:
        st.markdown(f"<div class='card'><h3>{item['tipo']}</h3><b>{item['titulo']}</b><br><span class='small'>{item['estado']}</span><br><span class='pill'>Organizar después</span></div>", unsafe_allow_html=True)

elif page == "✅ Tareas":
    header("Tareas", "Hoy, semana y próximos pasos.")
    new_task = st.text_input("Nueva tarea")
    zona = st.selectbox("Cuándo", ["Hoy", "Semana", "Próximamente", "Algún día"])
    if st.button("Añadir tarea", type="primary") and new_task:
        st.session_state.tasks.append({"txt":new_task, "done":False, "zona":zona})
    for z in ["Hoy", "Semana", "Próximamente", "Algún día"]:
        st.subheader(z)
        for i,t in enumerate(st.session_state.tasks):
            if t["zona"] == z:
                st.session_state.tasks[i]["done"] = st.checkbox(t["txt"], value=t["done"], key=f"task{i}")

elif page == "🧭 Radar":
    header("Radar", "Oportunidades, eventos y señales del mundo literario.")
    tabs = st.tabs(["Madrid", "Concursos", "Noticias", "Favoritos"])
    with tabs[0]:
        card("🎤 Presentación literaria", "Madrid · Revisar horarios compatibles con llegada 18:00-18:30")
        card("📚 Librerías prioritarias", "FNAC, Casa del Libro, librerías independientes y bibliotecas de zona sur.")
    with tabs[1]:
        card("🏆 Concurso por revisar", "Añadir convocatorias reales cuando activemos búsqueda web.")
    with tabs[2]:
        card("📰 Noticias", "Pendiente activar módulo de noticias reales del sector editorial.")
    with tabs[3]:
        card("⭐ Favoritos", "Aquí irán librerías, autores, espacios y eventos que quieras vigilar.")

elif page == "📅 Calendario":
    header("Calendario", "Fechas importantes, publicaciones y eventos.")
    st.date_input("Seleccionar fecha", value=date.today())
    card("Hoy", "• Revisar Radar<br>• Añadir 3 contactos<br>• Guardar ideas de contenido")
    card("Fechas clave", "23 abril · Día del Libro<br>Sant Jordi · Campañas<br>Navidad · Lanzamiento y reactivación")

elif page == "🎬 Estudio":
    header("Estudio Editorial", "Contenido por temporadas, no por urgencias.")
    cols = st.columns(3)
    for col, name, count in zip(cols, ["Ideas", "Guion", "Grabar"], [12,4,6]):
        col.markdown(f"<div class='card'><h3>{name}</h3><b>{count}</b><br><span class='small'>pendientes</span></div>", unsafe_allow_html=True)
    card("Series aprobadas", "¿Sabías que...? · Madrid Literario · Cuaderno de autora · Una foto, una historia")

elif page == "📚 Libros":
    header("Libros", "Proyectos, campaña y próximos pasos.")
    card("📖 El libro mágico de Hugo e Inés", "Estado: terminado / campaña en preparación<br>Prioridad: contactos, presentaciones y material infantil")
    card("✍️ Obra adulta", "Estado: construcción de marca Irene Zurilla antes de lanzamiento")

elif page == "🤝 Relaciones":
    header("Relaciones", "Contactos que hay que cuidar.")
    card("📚 Librerías", "Crear mapa inicial: Madrid, Getafe, Leganés, Majadahonda, zona Toledo")
    card("🏛 Bibliotecas", "Pendiente lista inicial y calendario de actividades")
    card("📰 Prensa / creadores", "Pendiente base de datos")

elif page == "💡 Ideas para la app":
    header("Ideas para la app", "Aquí dejamos mejoras para futuras versiones.")
    with st.form("idea_app"):
        idea = st.text_input("Nueva idea de mejora")
        estado = st.selectbox("Estado", ["Nueva", "En estudio", "Aprobada", "En desarrollo", "Terminada", "Descartada"])
        if st.form_submit_button("Guardar idea", type="primary") and idea:
            st.session_state.suggestions.insert(0, {"txt":idea, "estado":estado})
            st.success("Idea guardada")
    for s in st.session_state.suggestions:
        st.markdown(f"<div class='card'><h3>💡 {s['txt']}</h3><span class='pill'>{s['estado']}</span></div>", unsafe_allow_html=True)

st.markdown("<div class='nav-note'>🎙️ Notas de voz · siempre visible en móvil</div>", unsafe_allow_html=True)
