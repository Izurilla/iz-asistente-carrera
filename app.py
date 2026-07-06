import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="IZ | Asistente de Carrera",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

VERSION = "V2.0 visual"

MODULES = [
    "🏠 Centro de Operaciones",
    "🌱 Semillero",
    "✅ Tareas",
    "🧭 Radar",
    "🎬 Estudio",
    "📅 Calendario",
    "🤝 Relaciones",
    "📚 Libros",
    "📰 Noticias",
    "📈 Dirección",
    "💡 Ideas para la app",
]


def init_state():
    defaults = {
        "page": MODULES[0],
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
            "Menú desplegable en lugar de botones inferiores",
            "Botón de notas de voz siempre visible",
            "Dashboard compacto para móvil",
        ],
        "contactos": [
            "Librerías Madrid / Getafe / Leganés",
            "Bibliotecas Comunidad de Madrid",
            "Autores y presentaciones literarias",
        ],
        "notas_voz": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

st.markdown(
    """
    <style>
    :root{
      --bg:#f6eadf; --panel:#fffaf3; --panel2:#f0ddc8; --ink:#201d1b; --muted:#7a6a5c;
      --line:#e6d4c2; --accent:#2b243b; --accent2:#6f567f; --green:#6f8a75;
      --shadow:0 16px 40px rgba(76,52,31,.10);
    }
    html, body, [data-testid="stAppViewContainer"]{
      background: radial-gradient(circle at top left,#fff9f2 0%,#f7ecdf 42%,#f2e4d7 100%);
    }
    [data-testid="stHeader"]{background:rgba(255,255,255,0)}
    .block-container{padding-top:.7rem;padding-bottom:7.2rem;max-width:680px;}
    h1,h2,h3,p,div,span,label{font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}
    div[data-testid="stSelectbox"] label{display:none;}
    .topbar{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;gap:10px;}
    .brand{font-weight:800;letter-spacing:-.04em;font-size:24px;color:var(--ink);}
    .version{font-size:12px;color:var(--muted);background:rgba(255,250,243,.65);border:1px solid var(--line);padding:6px 10px;border-radius:999px;}
    .hero{background:linear-gradient(135deg,#ead5bd 0%,#fff8ef 100%);border:1px solid var(--line);border-radius:30px;padding:22px 22px 20px;box-shadow:var(--shadow);margin:8px 0 14px;}
    .hero h1{font-size:30px;margin:0;color:var(--ink);letter-spacing:-.055em;line-height:1.04;}
    .hero p{font-size:15px;color:var(--muted);margin:9px 0 0;}
    .kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:14px 0 4px;}
    .kpi{background:rgba(255,250,243,.9);border:1px solid var(--line);border-radius:20px;padding:12px 7px;text-align:center;box-shadow:0 8px 24px rgba(76,52,31,.06);}
    .kpi b{display:block;font-size:24px;line-height:1;color:var(--accent2)}
    .kpi span{display:block;margin-top:5px;font-size:11.5px;color:var(--muted)}
    .card{background:rgba(255,250,243,.94);border:1px solid var(--line);border-radius:24px;padding:16px;margin:10px 0;box-shadow:0 10px 28px rgba(76,52,31,.07);}
    .card h2{font-size:19px;letter-spacing:-.025em;margin:0 0 8px;color:var(--ink)}
    .card p{font-size:14.5px;line-height:1.45;color:var(--muted);margin:0 0 8px;}
    .mini-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px;}
    .mini{background:#f3e4d5;border:1px solid #e4d0bc;border-radius:20px;padding:13px;min-height:76px;}
    .mini strong{display:block;color:var(--ink);font-size:14px;margin-bottom:4px}
    .mini span{font-size:12.5px;color:var(--muted)}
    .pill{display:inline-block;background:#efe1d2;border:1px solid #e2ccb6;color:#3b332d;padding:7px 10px;border-radius:999px;font-size:12px;margin:3px 3px 0 0;}
    .floating-mic{position:fixed;right:18px;bottom:22px;width:76px;height:76px;border-radius:28px;background:linear-gradient(135deg,#201d1b,#37304c);color:#fff;display:flex;align-items:center;justify-content:center;font-size:34px;z-index:9999;box-shadow:0 18px 50px rgba(0,0,0,.28);border:7px solid rgba(255,250,243,.95);}
    .hint{font-size:12px;color:var(--muted);text-align:center;margin-top:-4px;margin-bottom:8px;}
    .section-title{font-size:22px;font-weight:800;letter-spacing:-.04em;margin:6px 0 8px;color:var(--ink);}
    .divider{height:1px;background:var(--line);margin:10px 0;}
    .stButton>button{border-radius:16px;border:1px solid #dfcbb7;background:#fffaf3;color:#211f1c;font-weight:650;}
    .stButton>button:hover{border-color:#bda58e;background:#f4e6d8;}
    @media(max-width:520px){
      .block-container{padding-left:1rem;padding-right:1rem;}
      .hero h1{font-size:27px;}
      .kpi-grid{gap:7px;}
      .kpi{padding:11px 4px;border-radius:18px;}
      .kpi b{font-size:22px;}
      .kpi span{font-size:10.5px;}
      .mini-grid{grid-template-columns:1fr 1fr;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def top_menu():
    st.markdown('<div class="topbar"><div class="brand">🧭 IZ</div><div class="version">' + VERSION + '</div></div>', unsafe_allow_html=True)
    selected = st.selectbox("Menú", MODULES, index=MODULES.index(st.session_state.page) if st.session_state.page in MODULES else 0, key="menu_select")
    if selected != st.session_state.page:
        st.session_state.page = selected
        st.rerun()
    st.markdown('<div class="hint">Usa el desplegable para moverte por la app · El micrófono queda siempre visible</div>', unsafe_allow_html=True)


def card(title, body, pills=None):
    pill_html = ""
    if pills:
        pill_html = "".join([f'<span class="pill">{p}</span>' for p in pills])
    st.markdown(f'<div class="card"><h2>{title}</h2><p>{body}</p>{pill_html}</div>', unsafe_allow_html=True)


def page_centro():
    st.markdown(
        f"""
        <div class="hero">
          <h1>Centro de Operaciones</h1>
          <p>Buenos días, Irene. Esto es lo que necesita tu atención ahora.</p>
          <div class="kpi-grid">
            <div class="kpi"><b>{len(st.session_state.tareas_hoy)}</b><span>Tareas</span></div>
            <div class="kpi"><b>{len(st.session_state.semillero)}</b><span>Semillero</span></div>
            <div class="kpi"><b>{len(st.session_state.oportunidades)}</b><span>Radar</span></div>
            <div class="kpi"><b>1</b><span>Agenda</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    card("🎯 Prioridad del día", "Dejar estable la app y recuperar el dashboard móvil. No añadir más módulos hasta que la pantalla principal sea cómoda.", ["Hoy", "Alta prioridad"])
    st.markdown('<div class="mini-grid">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        card("📚 Libro activo", "El libro mágico de Hugo e Inés · campaña inicial en preparación.", ["Infantil", "Lanzamiento"])
    with col2:
        card("🧭 Radar rápido", "4 oportunidades pendientes de revisar esta semana.", ["Madrid", "Eventos"])
    col3, col4 = st.columns(2)
    with col3:
        card("🌱 Semillero", f"{len(st.session_state.semillero)} elementos sin organizar.", ["Notas", "Ideas"])
    with col4:
        card("🎙️ Última nota", "Pendiente de grabar o escribir desde Notas de voz.", ["Audio"])
    card("☕ Consejo de Dirección", "Esta versión debe sentirse útil en móvil antes de crecer. Menos scroll, más decisión.", ["Dirección"])


def page_semillero():
    st.markdown('<div class="section-title">🌱 Semillero</div>', unsafe_allow_html=True)
    with st.form("nueva_semilla", clear_on_submit=True):
        tipo = st.selectbox("Tipo", ["🎙️ Nota de voz", "💡 Idea", "👤 Contacto", "📅 Evento", "📰 Noticia", "🏆 Concurso", "📌 Tarea"])
        texto = st.text_area("Contenido", placeholder="Guarda aquí algo que todavía no sabes dónde colocar...")
        if st.form_submit_button("Guardar en Semillero") and texto.strip():
            st.session_state.semillero.insert(0, {"tipo": tipo, "texto": texto.strip(), "estado": "Por organizar"})
            st.success("Guardado")
    for item in st.session_state.semillero:
        card(item["tipo"], item["texto"], [item["estado"]])


def page_tareas():
    st.markdown('<div class="section-title">✅ Tareas</div>', unsafe_allow_html=True)
    with st.form("nueva_tarea", clear_on_submit=True):
        nueva = st.text_input("Nueva tarea")
        if st.form_submit_button("Añadir") and nueva.strip():
            st.session_state.tareas_hoy.append(nueva.strip())
            st.success("Tarea añadida")
    st.markdown('<div class="card"><h2>🔥 Hoy</h2>', unsafe_allow_html=True)
    for tarea in st.session_state.tareas_hoy:
        st.checkbox(tarea, key=f"tarea_{tarea}")
    st.markdown('</div>', unsafe_allow_html=True)
    card("📅 Esta semana", "Preparar base de contactos · Revisar agenda cultural · Crear banco de contenidos.")
    card("⏳ Próximamente", "Dossier de autora · Registro de marca · Calendario editorial de septiembre.")


def page_radar():
    st.markdown('<div class="section-title">🧭 Radar</div>', unsafe_allow_html=True)
    tabs = st.tabs(["⭐ Recomendado", "🎤 Eventos", "🏆 Concursos", "📰 Noticias"])
    with tabs[0]:
        for op in st.session_state.oportunidades:
            card("Oportunidad", op, ["Revisar"])
    with tabs[1]:
        card("Madrid literario", "Presentaciones, librerías, bibliotecas y vida cultural de Madrid.", ["Pendiente"])
    with tabs[2]:
        card("Concursos", "Convocatorias para relatos, infantil y autora novel.", ["Pendiente"])
    with tabs[3]:
        card("Noticias", "Noticias del mundo editorial, libros e historia.", ["Pendiente"])


def page_estudio():
    st.markdown('<div class="section-title">🎬 Estudio</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    stages = [("💡 Ideas", "24"), ("📝 Guiones", "6"), ("🎙️ Grabar", "8"), ("✂️ Editar", "3"), ("📅 Programar", "5"), ("✅ Publicado", "12")]
    for idx, (name, count) in enumerate(stages):
        with cols[idx % 3]:
            card(name, f"{count} elementos", [])


def page_calendario():
    st.markdown('<div class="section-title">📅 Calendario</div>', unsafe_allow_html=True)
    card("Hoy", "Revisar app · probar dashboard · anotar sugerencias.", ["Trabajo app"])
    card("Viernes", "Radar del fin de semana.", ["Rutina"])
    card("Domingo", "Reunión de Dirección.", ["Rutina"])


def page_relaciones():
    st.markdown('<div class="section-title">🤝 Relaciones</div>', unsafe_allow_html=True)
    for c in st.session_state.contactos:
        card("Contacto / categoría", c, ["Seguimiento"])


def page_libros():
    st.markdown('<div class="section-title">📚 Libros</div>', unsafe_allow_html=True)
    card("El libro mágico de Hugo e Inés", "Libro infantil activo. Preparar campaña, presentaciones y materiales.", ["Activo", "Infantil"])
    card("Preludio de un ocaso", "Relato en expediente de autora. Revisar oportunidades de concurso.", ["Relato"])


def page_noticias():
    st.markdown('<div class="section-title">📰 Noticias</div>', unsafe_allow_html=True)
    card("Noticias reales", "Próximo paso: conectar este módulo a búsquedas web y guardar noticias útiles.", ["V futura"])


def page_direccion():
    st.markdown('<div class="section-title">📈 Dirección</div>', unsafe_allow_html=True)
    card("Rutina", "Domingo: reunión de dirección. Viernes: radar del fin de semana. Mensual: revisión estratégica.", ["Aprobado"])
    card("Criterio", "La app está al servicio de tu carrera. No construiremos funciones que no ayuden a tomar decisiones.", ["Regla"])


def page_ideas_app():
    st.markdown('<div class="section-title">💡 Ideas para la app</div>', unsafe_allow_html=True)
    with st.form("idea_app", clear_on_submit=True):
        idea = st.text_input("Nueva idea")
        if st.form_submit_button("Guardar idea") and idea.strip():
            st.session_state.ideas_app.insert(0, idea.strip())
            st.success("Idea guardada")
    for idea in st.session_state.ideas_app:
        card("💡 Idea", idea, ["Nueva"])


def page_notas_voz():
    st.markdown('<div class="section-title">🎙️ Notas de voz</div>', unsafe_allow_html=True)
    st.info("De momento funciona como captura escrita. La grabación real llegará en una versión posterior.")
    with st.form("nota_voz", clear_on_submit=True):
        nota = st.text_area("Nota rápida", placeholder="Escribe o transcribe lo que quieras guardar...")
        if st.form_submit_button("Guardar nota") and nota.strip():
            st.session_state.notas_voz.insert(0, nota.strip())
            st.session_state.semillero.insert(0, {"tipo": "🎙️ Nota de voz", "texto": nota.strip(), "estado": "Por organizar"})
            st.success("Nota guardada en Semillero")
    for n in st.session_state.notas_voz:
        card("🎙️ Nota", n, ["Reciente"])


def floating_mic():
    st.markdown('<div class="floating-mic">🎙️</div>', unsafe_allow_html=True)
    if st.button("🎙️ Notas de voz", use_container_width=True):
        st.session_state.page = "🎙️ Notas de voz"
        st.rerun()


top_menu()

# Añadimos la página de notas aunque no esté en el desplegable para mantenerla como acción fija.
if st.session_state.page == "🏠 Centro de Operaciones":
    page_centro()
elif st.session_state.page == "🌱 Semillero":
    page_semillero()
elif st.session_state.page == "✅ Tareas":
    page_tareas()
elif st.session_state.page == "🧭 Radar":
    page_radar()
elif st.session_state.page == "🎬 Estudio":
    page_estudio()
elif st.session_state.page == "📅 Calendario":
    page_calendario()
elif st.session_state.page == "🤝 Relaciones":
    page_relaciones()
elif st.session_state.page == "📚 Libros":
    page_libros()
elif st.session_state.page == "📰 Noticias":
    page_noticias()
elif st.session_state.page == "📈 Dirección":
    page_direccion()
elif st.session_state.page == "💡 Ideas para la app":
    page_ideas_app()
elif st.session_state.page == "🎙️ Notas de voz":
    page_notas_voz()

floating_mic()
