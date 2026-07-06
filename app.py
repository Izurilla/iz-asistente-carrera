import streamlit as st
from pathlib import Path

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")

LOGO_PATH = Path(__file__).with_name("logo_irene.png")

MODULES = [
    "Centro de Operaciones",
    "Semillero",
    "Tareas",
    "Radar",
    "Estudio",
    "Calendario",
    "Relaciones",
    "Libros y relatos",
    "Ideas para la app",
]

DEFAULT_SEMILLAS = [
    {"tipo": "Nota de voz", "texto": "Idea para vídeo: ¿sabías que...? sobre libros antiguos", "estado": "Por organizar"},
    {"tipo": "Idea", "texto": "Vídeo: una foto, una historia", "estado": "Por organizar"},
]
DEFAULT_TAREAS = [
    "Revisar calendario + noticias",
    "Preparar base de contactos",
    "Crear banco de contenidos",
]
DEFAULT_OPS = [
    "Presentación en FNAC Callao · Madrid",
    "Concurso de relato histórico · cierra en 16 días",
    "Buscar eventos de librerías en Getafe/Leganés",
    "Revisar agenda cultural del fin de semana",
]


def init_state():
    if "page" not in st.session_state:
        st.session_state.page = "Centro de Operaciones"
    if "semillas" not in st.session_state:
        st.session_state.semillas = list(DEFAULT_SEMILLAS)
    if "tareas" not in st.session_state:
        st.session_state.tareas = list(DEFAULT_TAREAS)
    if "oportunidades" not in st.session_state:
        st.session_state.oportunidades = list(DEFAULT_OPS)
    if "ideas_app" not in st.session_state:
        st.session_state.ideas_app = [
            "Menú compacto arriba",
            "Notas de voz siempre visibles",
            "Conectar datos con Drive",
        ]


def go_to(page: str):
    st.session_state.page = page
    st.rerun()


def css():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #fbf7ef 0%, #f2e8da 100%);
        }
        [data-testid="stHeader"] { background: rgba(255,255,255,0); }
        .block-container {
            max-width: 760px;
            padding-top: 1.1rem;
            padding-bottom: 2rem;
        }
        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 4px 2px 14px 2px;
            border-bottom: 1px solid rgba(60,45,35,.08);
            margin-bottom: 14px;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .brand-title {
            font-size: 28px;
            font-weight: 900;
            color: #25232b;
            line-height: 1;
        }
        .version-pill {
            border: 1px solid rgba(80,55,45,.14);
            background: rgba(255,255,255,.45);
            border-radius: 999px;
            padding: 8px 14px;
            color: #7a6b60;
            font-size: 14px;
            white-space: nowrap;
        }
        .hero {
            background: linear-gradient(135deg, rgba(255,255,255,.88), rgba(237,220,202,.94));
            border: 1px solid rgba(90,70,55,.12);
            border-radius: 30px;
            padding: 24px 26px;
            box-shadow: 0 18px 40px rgba(75,55,35,.08);
            margin: 12px 0 18px 0;
        }
        .hero h1 {
            font-size: 42px;
            line-height: 1.05;
            margin: 0 0 16px 0;
            color: #22212a;
            letter-spacing: -1px;
        }
        .hero p {
            font-size: 20px;
            color: #766b62;
            margin: 0;
            line-height: 1.45;
        }
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin: 16px 0 18px 0;
        }
        .kpi {
            background: rgba(255,255,255,.82);
            border: 1px solid rgba(80,60,45,.10);
            border-radius: 22px;
            padding: 14px 8px;
            text-align: center;
            box-shadow: 0 12px 30px rgba(75,55,35,.07);
            min-height: 98px;
        }
        .kpi .icon { font-size: 22px; margin-bottom: 4px; }
        .kpi .num { font-size: 30px; font-weight: 900; color: #765299; line-height: 1.05; }
        .kpi .label { font-size: 14px; color: #27242a; margin-top: 4px; }
        .summary {
            background: rgba(255,255,255,.88);
            border: 1px solid rgba(80,60,45,.10);
            border-radius: 26px;
            padding: 22px 24px;
            box-shadow: 0 12px 30px rgba(75,55,35,.07);
            margin: 18px 0;
        }
        .summary h2 {
            margin: 0 0 14px 0;
            font-size: 26px;
            color: #25232b;
        }
        .summary-row {
            padding: 10px 0;
            border-top: 1px solid rgba(80,60,45,.08);
            font-size: 17px;
            line-height: 1.35;
            color: #4a4540;
        }
        .summary-row:first-of-type { border-top: 0; }
        .card {
            background: rgba(255,255,255,.86);
            border: 1px solid rgba(80,60,45,.10);
            border-radius: 28px;
            padding: 24px;
            box-shadow: 0 12px 30px rgba(75,55,35,.07);
            margin: 16px 0;
        }
        .card h2, .card h3 { margin-top: 0; color: #25232b; }
        .small-note { color: #7a6b60; font-size: 15px; }
        div.stButton > button {
            border-radius: 18px !important;
            border: 1px solid rgba(70,45,35,.16) !important;
            background: rgba(255,255,255,.92) !important;
            color: #29262e !important;
            min-height: 46px;
            box-shadow: 0 8px 20px rgba(70,45,35,.04);
        }
        div[data-baseweb="select"] > div {
            border-radius: 18px !important;
            background: rgba(255,255,255,.82) !important;
            border-color: rgba(70,45,35,.14) !important;
        }
        textarea, input { border-radius: 16px !important; }
        @media (max-width: 640px) {
            .block-container { padding-left: 18px; padding-right: 18px; padding-top: .6rem; }
            .brand-title { font-size: 26px; }
            .version-pill { font-size: 13px; padding: 7px 12px; }
            .hero { padding: 20px 22px; border-radius: 26px; }
            .hero h1 { font-size: 38px; }
            .hero p { font-size: 20px; }
            .kpi-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
            .kpi { min-height: 88px; padding: 12px 8px; }
            .kpi .num { font-size: 28px; }
            .summary { padding: 20px 22px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def header():
    left, right = st.columns([1, 1])
    with left:
        if LOGO_PATH.exists():
            lcol, tcol = st.columns([0.38, 0.62])
            with lcol:
                st.image(str(LOGO_PATH), width=58)
            with tcol:
                st.markdown("<div class='brand-title'>IZ</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='brand-title'>IZ</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div style='text-align:right'><span class='version-pill'>V2.8 estable</span></div>", unsafe_allow_html=True)

    ncol, mcol = st.columns([0.32, 0.68])
    with ncol:
        if st.button("🎙️ Notas", use_container_width=True, key="top_notes"):
            st.session_state.show_notes = True
    with mcol:
        selected = st.selectbox(
            "Menú",
            MODULES,
            index=MODULES.index(st.session_state.page),
            label_visibility="collapsed",
            key="main_menu_select",
        )
        if selected != st.session_state.page:
            st.session_state.page = selected
            st.rerun()

    if st.session_state.get("show_notes", False):
        with st.expander("🎙️ Nueva nota", expanded=True):
            note_type = st.selectbox("Tipo", ["Nota de voz", "Idea", "Contacto", "Evento", "Tarea", "Idea para la app"], key="note_type")
            text = st.text_area("Contenido", placeholder="Escribe o pega aquí lo que quieras guardar...", key="note_text")
            if st.button("Guardar nota", use_container_width=True, key="save_note"):
                if text.strip():
                    if note_type == "Tarea":
                        st.session_state.tareas.append(text.strip())
                    elif note_type == "Idea para la app":
                        st.session_state.ideas_app.append(text.strip())
                    else:
                        st.session_state.semillas.append({"tipo": note_type, "texto": text.strip(), "estado": "Por organizar"})
                    st.session_state.note_text = ""
                    st.session_state.show_notes = False
                    st.success("Guardado.")
                    st.rerun()
                else:
                    st.warning("Escribe algo antes de guardar.")


def kpi_box(icon: str, num: int, label: str):
    st.markdown(
        f"""
        <div class='kpi'>
            <div class='icon'>{icon}</div>
            <div class='num'>{num}</div>
            <div class='label'>{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def centro():
    st.markdown(
        """
        <div class='hero'>
            <h1>Centro de<br>Operaciones</h1>
            <p>Buenos días, Irene · Aquí está lo que necesita tu atención.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tareas_count = len(st.session_state.tareas)
    semillas_count = len(st.session_state.semillas)
    oportunidades_count = len(st.session_state.oportunidades)
    eventos_count = 2

    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        kpi_box("☑️", tareas_count, "Tareas")
        if st.button("Abrir tareas", key="kpi_tareas", use_container_width=True):
            go_to("Tareas")
    with cols[1]:
        kpi_box("🌱", semillas_count, "Semillas")
        if st.button("Abrir semillero", key="kpi_semillero", use_container_width=True):
            go_to("Semillero")
    with cols[2]:
        kpi_box("⭐", oportunidades_count, "Oportunidades")
        if st.button("Abrir radar", key="kpi_radar", use_container_width=True):
            go_to("Radar")
    with cols[3]:
        kpi_box("📅", eventos_count, "Eventos")
        if st.button("Abrir calendario", key="kpi_calendario", use_container_width=True):
            go_to("Calendario")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='summary'>
            <h2>Resumen de hoy</h2>
            <div class='summary-row'>🎯 <strong>Prioridad:</strong> Preparar base de contactos y crear banco de contenidos.</div>
            <div class='summary-row'>🔥 <strong>Radar:</strong> 4 oportunidades detectadas para revisar esta semana.</div>
            <div class='summary-row'>📚 <strong>Libro activo:</strong> El libro mágico de Hugo e Inés · preparación de publicación.</div>
            <div class='summary-row'>🎙️ <strong>Última nota:</strong> Idea para vídeo sobre libros antiguos.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def semillero():
    st.title("🌱 Semillero")
    st.caption("Todo lo que todavía no tiene destino definitivo.")
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        tipo = st.selectbox("Tipo", ["Nota de voz", "Idea", "Contacto", "Evento", "Noticia", "Concurso", "Libro/relato"], key="seed_type")
        texto = st.text_area("Contenido", placeholder="Guarda aquí algo que todavía no sabes dónde colocar...", key="seed_text")
        if st.button("Guardar en Semillero", key="add_seed"):
            if texto.strip():
                st.session_state.semillas.append({"tipo": tipo, "texto": texto.strip(), "estado": "Por organizar"})
                st.session_state.seed_text = ""
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    for i, item in enumerate(st.session_state.semillas):
        st.markdown(
            f"""
            <div class='card'>
                <h3>{item['tipo']}</h3>
                <p>{item['texto']}</p>
                <p class='small-note'>Estado: {item['estado']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def tareas():
    st.title("✅ Tareas")
    nueva = st.text_input("Nueva tarea", key="new_task")
    if st.button("Añadir tarea", key="add_task") and nueva.strip():
        st.session_state.tareas.append(nueva.strip())
        st.session_state.new_task = ""
        st.rerun()
    st.markdown("<div class='card'><h2>Hoy</h2>", unsafe_allow_html=True)
    for i, tarea in enumerate(st.session_state.tareas):
        st.checkbox(tarea, key=f"task_{i}")
    st.markdown("</div>", unsafe_allow_html=True)


def radar():
    st.title("🧭 Radar")
    tabs = st.tabs(["⭐ Recomendado", "🎤 Eventos", "🏆 Concursos", "📰 Noticias"])
    with tabs[0]:
        for op in st.session_state.oportunidades:
            st.markdown(f"<div class='card'><h3>Oportunidad</h3><p>{op}</p></div>", unsafe_allow_html=True)
    with tabs[1]:
        st.write("Próximamente: agenda cultural de Madrid y alrededores.")
    with tabs[2]:
        st.write("Próximamente: concursos filtrados por tipo de obra.")
    with tabs[3]:
        st.write("Próximamente: noticias editoriales y culturales.")


def estudio():
    st.title("🎬 Estudio")
    st.markdown("<div class='card'><h2>Ideas</h2><p>¿Sabías que...? sobre libros antiguos</p><p>Vídeo: una foto, una historia</p></div>", unsafe_allow_html=True)


def calendario():
    st.title("📅 Calendario")
    st.markdown("<div class='card'><h2>Esta semana</h2><p>Viernes: revisar radar cultural.</p><p>Domingo: reunión de dirección.</p></div>", unsafe_allow_html=True)


def relaciones():
    st.title("🤝 Relaciones")
    st.markdown("<div class='card'><h2>Contactos prioritarios</h2><p>Librerías · Bibliotecas · Editorial · Autores · Prensa</p></div>", unsafe_allow_html=True)


def libros():
    st.title("📚 Libros y relatos")
    st.caption("Aquí van libros, cuentos y relatos terminados, publicados o no.")
    st.markdown("<div class='card'><h2>El libro mágico de Hugo e Inés</h2><p>Estado: preparación de publicación.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h2>Preludio de un ocaso</h2><p>Relato terminado · pendiente de concursos.</p></div>", unsafe_allow_html=True)


def ideas_app():
    st.title("💡 Ideas para la app")
    idea = st.text_input("Nueva idea de mejora", key="new_idea_app")
    if st.button("Guardar idea", key="save_idea_app") and idea.strip():
        st.session_state.ideas_app.append(idea.strip())
        st.session_state.new_idea_app = ""
        st.rerun()
    for idea in st.session_state.ideas_app:
        st.markdown(f"<div class='card'><p>{idea}</p><p class='small-note'>Estado: nueva</p></div>", unsafe_allow_html=True)


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
}

init_state()
css()
header()
ROUTES[st.session_state.page]()
