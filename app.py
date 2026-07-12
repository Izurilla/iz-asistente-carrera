import base64
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="IZ | Asistente de Carrera",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

VERSION = "V3.0 · Rediseño Hoy"

# ---------- ESTADO ----------
if "page" not in st.session_state:
    st.session_state.page = "Centro de Operaciones"
if "semillero" not in st.session_state:
    st.session_state.semillero = [
        {
            "tipo": "Nota de voz",
            "texto": "Idea para vídeo: ¿sabías que...? sobre libros antiguos.",
            "estado": "Por organizar",
        },
        {
            "tipo": "Idea",
            "texto": "Crear banco de contenidos para septiembre.",
            "estado": "Por organizar",
        },
    ]
if "tareas" not in st.session_state:
    st.session_state.tareas = [
        {"texto": "Revisar calendario y noticias", "hecha": False},
        {"texto": "Preparar base de contactos", "hecha": False},
        {"texto": "Crear banco de contenidos", "hecha": False},
    ]
if "ideas_app" not in st.session_state:
    st.session_state.ideas_app = [
        "El menú en móvil debe ser compacto.",
        "Acceso rápido a notas de voz.",
        "La pantalla principal debe centrarse en lo que ocurre hoy.",
    ]

# ---------- ESTILO ----------
st.markdown(
    """
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
  background: rgba(255,255,255,0.55) !important;
}
.block-container{
  padding-top: .8rem !important;
  padding-bottom: 2rem !important;
  max-width: 740px !important;
}
.iz-brand-row{
  display:flex;
  align-items:center;
  gap:10px;
}
.iz-logo{
  width:52px;
  height:52px;
  border-radius:50%;
  object-fit:cover;
  box-shadow:0 7px 20px rgba(60,45,30,.12);
}
.iz-wordmark{
  font-size:25px;
  font-weight:850;
  letter-spacing:-.04em;
}
.version{
  color:var(--muted);
  font-size:12px;
  margin-top:2px;
}
.today-head{
  margin:.7rem 0 .8rem 0;
}
.today-head h1{
  margin:0;
  font-size:34px;
  line-height:1.05;
  letter-spacing:-.045em;
}
.today-head p{
  margin:7px 0 0 0;
  color:var(--muted);
  font-size:16px;
}
.section-label{
  font-size:13px;
  font-weight:800;
  text-transform:uppercase;
  letter-spacing:.08em;
  color:var(--muted);
  margin:.9rem 0 .25rem 0;
}
.info-card{
  border:1px solid var(--line);
  border-radius:22px;
  padding:17px 18px;
  background:rgba(255,255,255,.88);
  box-shadow:0 9px 23px rgba(68,45,25,.055);
  margin:.45rem 0;
}
.info-card h3{
  margin:0 0 8px 0;
  font-size:19px;
  letter-spacing:-.025em;
}
.info-card p{
  margin:4px 0;
  color:#3d3834;
  line-height:1.45;
}
.info-card .muted{
  color:var(--muted);
  font-size:14px;
}
.compact-list{
  margin:0;
  padding-left:1.15rem;
}
.compact-list li{
  margin:.35rem 0;
  color:#3d3834;
}
.status-pill{
  display:inline-block;
  padding:5px 10px;
  border-radius:999px;
  background:#ead9c9;
  border:1px solid #dfcdbc;
  color:#3b332d;
  font-size:12px;
  margin-top:6px;
}
.stButton > button{
  width:100%;
  border-radius:16px !important;
  min-height:42px;
  border:1px solid var(--line);
  background:rgba(255,255,255,.82);
  color:var(--text);
}
[data-testid="stPopover"] > button{
  border-radius:16px !important;
  min-height:42px;
}
[data-testid="stVerticalBlockBorderWrapper"]{
  border-radius:22px !important;
  border-color:var(--line) !important;
  background:rgba(255,255,255,.72);
}
.menu-title{
  font-size:12px;
  font-weight:850;
  letter-spacing:.09em;
  color:var(--muted);
  margin:8px 0 3px 0;
}
@media(max-width:520px){
  .block-container{
    padding-left:.85rem !important;
    padding-right:.85rem !important;
  }
  .iz-logo{width:46px;height:46px;}
  .iz-wordmark{font-size:23px;}
  .today-head h1{font-size:31px;}
  .info-card{padding:15px 16px;border-radius:19px;}
}
</style>
""",
    unsafe_allow_html=True,
)


def logo_html() -> str:
    logo_path = Path("logo_irene.png")
    if logo_path.exists():
        data = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
        return f'<img class="iz-logo" src="data:image/png;base64,{data}">'
    return '<div class="iz-logo" style="display:flex;align-items:center;justify-content:center;background:#fff;">IZ</div>'


def go(page: str) -> None:
    st.session_state.page = page
    st.rerun()


# ---------- CABECERA FIJA Y MENÚ COMPACTO ----------
brand_col, voice_col, menu_col = st.columns([5.2, 1.15, 1.15], vertical_alignment="center")
with brand_col:
    st.markdown(
        f"""
        <div class="iz-brand-row">
          {logo_html()}
          <div>
            <div class="iz-wordmark">IZ</div>
            <div class="version">{VERSION}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with voice_col:
    if st.button("🎙️", key="voice_top", help="Notas rápidas"):
        go("Semillero")
with menu_col:
    with st.popover("☰", help="Abrir menú"):
        st.markdown('<div class="menu-title">HOY</div>', unsafe_allow_html=True)
        if st.button("🏠 Centro de Operaciones", key="m_centro"):
            go("Centro de Operaciones")
        if st.button("✅ Tareas", key="m_tareas"):
            go("Tareas")
        if st.button("📅 Calendario", key="m_cal"):
            go("Calendario")

        st.markdown('<div class="menu-title">ESCRITURA</div>', unsafe_allow_html=True)
        if st.button("🌱 Semillero", key="m_sem"):
            go("Semillero")
        if st.button("🎬 Estudio", key="m_estudio"):
            go("Estudio")
        if st.button("📚 Libros y relatos", key="m_libros"):
            go("Libros y relatos")

        st.markdown('<div class="menu-title">CARRERA</div>', unsafe_allow_html=True)
        if st.button("🧭 Radar", key="m_radar"):
            go("Radar")
        if st.button("🤝 Contactos", key="m_rel"):
            go("Relaciones")

        st.markdown('<div class="menu-title">APP</div>', unsafe_allow_html=True)
        if st.button("💡 Ideas para la app", key="m_ideas"):
            go("Ideas para la app")
        if st.button("⚙️ Ajustes", key="m_ajustes"):
            go("Ajustes")


# ---------- PÁGINAS ----------
def centro() -> None:
    st.markdown(
        """
        <div class="today-head">
          <h1>Hoy</h1>
          <p>Lo que necesitas saber para organizar tu día como autora.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # TAREAS
    st.markdown('<div class="section-label">✅ Tareas de hoy</div>', unsafe_allow_html=True)
    pendientes = [t for t in st.session_state.tareas if not t["hecha"]][:3]
    if pendientes:
        items = "".join(f"<li>{t['texto']}</li>" for t in pendientes)
        st.markdown(
            f'<div class="info-card"><ul class="compact-list">{items}</ul></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="info-card"><p>No tienes tareas pendientes para hoy.</p></div>', unsafe_allow_html=True)
    if st.button("Ver todas las tareas", key="home_tareas"):
        go("Tareas")

    # EVENTOS
    st.markdown('<div class="section-label">📍 Eventos de hoy</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-card">
          <h3>Agenda cultural</h3>
          <p>18:30 · Presentación literaria por revisar</p>
          <p class="muted">Madrid · Pendiente de confirmar</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Abrir calendario", key="home_cal"):
        go("Calendario")

    # NOTAS
    st.markdown('<div class="section-label">🎙️ Notas rápidas</div>', unsafe_allow_html=True)
    ultimas = st.session_state.semillero[:2]
    notas_html = "".join(
        f"<p><strong>{item['tipo']}:</strong> {item['texto']}</p>" for item in ultimas
    )
    st.markdown(f'<div class="info-card">{notas_html}</div>', unsafe_allow_html=True)
    if st.button("Nueva nota o ver Semillero", key="home_sem"):
        go("Semillero")

    # NOTICIAS / RADAR
    st.markdown('<div class="section-label">📰 Noticias y oportunidades</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-card">
          <h3>Radar literario</h3>
          <p>• Presentación en Madrid para revisar.</p>
          <p>• Concurso de relato histórico: cierra en 16 días.</p>
          <p>• Próxima fecha clave: campaña de otoño.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Abrir Radar", key="home_radar"):
        go("Radar")

    # CONTACTOS
    st.markdown('<div class="section-label">👥 Contactos rápidos</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-card">
          <p><strong>Editorial Apuleyo</strong> · seguimiento editorial</p>
          <p><strong>Librerías de Madrid</strong> · base de contactos pendiente</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Abrir contactos", key="home_rel"):
        go("Relaciones")

    # PROYECTO ACTIVO
    st.markdown('<div class="section-label">📚 Proyecto activo</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-card">
          <h3>El libro mágico de Hugo e Inés</h3>
          <p>Fase: preparación editorial y planificación de lanzamiento.</p>
          <span class="status-pill">En marcha</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Ver libros y relatos", key="home_libros"):
        go("Libros y relatos")


def semillero() -> None:
    st.title("🌱 Semillero")
    st.caption("Notas, ideas y capturas que todavía no tienen un destino definitivo.")
    with st.form("nueva_semilla", clear_on_submit=True):
        tipo = st.selectbox(
            "Tipo",
            ["Nota de voz", "Idea", "Contacto", "Evento", "Noticia", "Concurso", "Relato"],
        )
        texto = st.text_area(
            "Contenido",
            placeholder="Guarda aquí algo que todavía no sabes dónde colocar...",
        )
        submitted = st.form_submit_button("Guardar en Semillero")
        if submitted and texto.strip():
            st.session_state.semillero.insert(
                0,
                {"tipo": tipo, "texto": texto.strip(), "estado": "Por organizar"},
            )
            st.success("Guardado en Semillero.")
    for item in st.session_state.semillero:
        with st.container(border=True):
            st.subheader(item["tipo"])
            st.write(item["texto"])
            st.caption(item["estado"])


def tareas() -> None:
    st.title("✅ Tareas")
    with st.form("nueva_tarea", clear_on_submit=True):
        texto = st.text_input("Nueva tarea")
        add = st.form_submit_button("Añadir")
        if add and texto.strip():
            st.session_state.tareas.append({"texto": texto.strip(), "hecha": False})
            st.success("Tarea añadida.")
    st.subheader("Hoy")
    for i, tarea in enumerate(st.session_state.tareas):
        st.session_state.tareas[i]["hecha"] = st.checkbox(
            tarea["texto"], value=tarea["hecha"], key=f"task_{i}"
        )


def radar() -> None:
    st.title("🧭 Radar")
    tabs = st.tabs(["⭐ Recomendado", "🎤 Eventos", "🏆 Concursos", "📰 Noticias"])
    with tabs[0]:
        with st.container(border=True):
            st.subheader("Presentación en Madrid")
            st.write("FNAC Callao · Pendiente de revisar")
        with st.container(border=True):
            st.subheader("Concurso de relato histórico")
            st.write("Cierra en 16 días")
    with tabs[1]:
        st.write("Eventos literarios y culturales para revisar.")
    with tabs[2]:
        st.write("Concursos pendientes de clasificar.")
    with tabs[3]:
        st.write("Noticias sobre lectura, escritura, lanzamientos y sector editorial.")


def estudio() -> None:
    st.title("🎬 Estudio")
    with st.container(border=True):
        st.subheader("Banco de contenido")
        st.write("¿Sabías que...? sobre libros antiguos")
        st.write("Vídeo: una foto, una historia")


def calendario() -> None:
    st.title("📅 Calendario")
    with st.container(border=True):
        st.subheader("Esta semana")
        st.write("Viernes: revisar radar del fin de semana.")
        st.write("Domingo por la tarde: reunión de dirección.")


def relaciones() -> None:
    st.title("🤝 Contactos")
    with st.container(border=True):
        st.subheader("Acceso rápido")
        st.write("Editoriales, librerías, bibliotecas, autores, prensa y clubes de lectura.")
        st.caption("La base de contactos editable llegará en la siguiente fase.")


def libros() -> None:
    st.title("📚 Libros y relatos")
    st.caption("Todo lo terminado o en campaña, esté publicado o no.")
    with st.container(border=True):
        st.subheader("El libro mágico de Hugo e Inés")
        st.write("Estado: preparación de publicación.")
    with st.container(border=True):
        st.subheader("Preludio de un ocaso")
        st.write("Relato terminado · posible concurso.")


def ideas_app() -> None:
    st.title("💡 Ideas para la app")
    with st.form("idea_app", clear_on_submit=True):
        idea = st.text_input("Nueva idea de mejora")
        ok = st.form_submit_button("Guardar idea")
        if ok and idea.strip():
            st.session_state.ideas_app.insert(0, idea.strip())
            st.success("Idea guardada.")
    for idea in st.session_state.ideas_app:
        with st.container(border=True):
            st.write(idea)
            st.caption("Nueva")


def ajustes() -> None:
    st.title("⚙️ Ajustes")
    st.write("Próximamente: Drive, copias, exportaciones y preferencias.")


page = st.session_state.page
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
elif page == "Ajustes":
    ajustes()
