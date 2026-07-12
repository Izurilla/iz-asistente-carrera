import base64
from datetime import date, datetime
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="IZ | Asistente de Carrera",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

VERSION = "V3.1 · Hoy funcional"

# ---------- ESTADO ----------
def init_state() -> None:
    defaults = {
        "page": "Centro de Operaciones",
        "semillero": [
            {
                "tipo": "Nota de voz",
                "texto": "Idea para vídeo: ¿sabías que...? sobre libros antiguos.",
                "estado": "Por organizar",
                "fecha": str(date.today()),
            },
            {
                "tipo": "Idea",
                "texto": "Crear banco de contenidos para septiembre.",
                "estado": "Por organizar",
                "fecha": str(date.today()),
            },
        ],
        "tareas": [
            {"texto": "Revisar calendario y noticias", "hecha": False, "fecha": str(date.today())},
            {"texto": "Preparar base de contactos", "hecha": False, "fecha": str(date.today())},
            {"texto": "Crear banco de contenidos", "hecha": False, "fecha": str(date.today())},
        ],
        "eventos": [
            {
                "titulo": "Presentación literaria por revisar",
                "hora": "18:30",
                "lugar": "Madrid",
                "fecha": str(date.today()),
            }
        ],
        "contactos": [
            {"nombre": "Editorial Apuleyo", "tipo": "Editorial", "nota": "Seguimiento editorial"},
            {"nombre": "Librerías de Madrid", "tipo": "Librería", "nota": "Base de contactos pendiente"},
        ],
        "noticias": [
            {"titulo": "Concurso de relato histórico", "detalle": "Cierra en 16 días"},
            {"titulo": "Agenda cultural de Madrid", "detalle": "Revisar próximos eventos literarios"},
        ],
        "ideas_app": [
            "El menú en móvil debe ser compacto.",
            "Acceso rápido a notas de voz.",
            "La pantalla principal debe centrarse en lo que ocurre hoy.",
        ],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()

# ---------- ESTILO ----------
st.markdown(
    """
<style>
:root{
  --bg:#fbf5ec;
  --card:#fffdf8;
  --line:#e5d5c7;
  --text:#1f1e22;
  --muted:#776e67;
  --accent:#7d5fa0;
}
html, body, [data-testid="stAppViewContainer"] {
  background: radial-gradient(circle at top, #fffaf1 0%, #fbf5ec 42%, #f3e7d8 100%);
}
[data-testid="stHeader"]{
  height: 1.9rem !important;
  background: rgba(255,255,255,0.36) !important;
}
.block-container{
  padding-top: .25rem !important;
  padding-bottom: 2rem !important;
  max-width: 740px !important;
}
.iz-brand-row{display:flex;align-items:center;gap:8px;}
.iz-logo{
  width:38px;height:38px;border-radius:50%;object-fit:cover;
  box-shadow:0 5px 15px rgba(60,45,30,.10);
}
.iz-wordmark{font-size:22px;font-weight:850;letter-spacing:-.04em;}
.version{color:var(--muted);font-size:11px;margin-top:1px;}
.today-head{margin:.45rem 0 .55rem 0;}
.today-head h1{margin:0;font-size:32px;line-height:1.05;letter-spacing:-.045em;}
.today-head p{margin:6px 0 0 0;color:var(--muted);font-size:15px;}
.section-label{
  font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.08em;
  color:var(--muted);margin:.8rem 0 .2rem 0;
}
.info-card{
  border:1px solid var(--line);border-radius:20px;padding:15px 16px;
  background:rgba(255,255,255,.88);box-shadow:0 8px 20px rgba(68,45,25,.05);margin:.35rem 0;
}
.info-card h3{margin:0 0 7px 0;font-size:18px;letter-spacing:-.025em;}
.info-card p{margin:4px 0;color:#3d3834;line-height:1.4;}
.info-card .muted{color:var(--muted);font-size:13px;}
.compact-list{margin:0;padding-left:1.1rem;}
.compact-list li{margin:.28rem 0;color:#3d3834;}
.status-pill{
  display:inline-block;padding:5px 10px;border-radius:999px;background:#ead9c9;
  border:1px solid #dfcdbc;color:#3b332d;font-size:12px;margin-top:6px;
}
.stButton > button{
  width:100%;border-radius:15px !important;min-height:40px;border:1px solid var(--line);
  background:rgba(255,255,255,.84);color:var(--text);
}
[data-testid="stPopover"] > button{border-radius:15px !important;min-height:40px;}
[data-testid="stVerticalBlockBorderWrapper"]{
  border-radius:20px !important;border-color:var(--line) !important;background:rgba(255,255,255,.72);
}
.menu-title{font-size:12px;font-weight:850;letter-spacing:.09em;color:var(--muted);margin:8px 0 3px 0;}
.quick-row{display:grid;grid-template-columns:repeat(2,1fr);gap:9px;margin:.45rem 0 .3rem;}
.quick-chip{border:1px solid var(--line);background:rgba(255,255,255,.82);border-radius:16px;padding:11px 12px;}
.quick-chip strong{display:block;font-size:13px;}
.quick-chip span{display:block;color:var(--muted);font-size:12px;margin-top:2px;}
@media(max-width:520px){
  .block-container{padding-left:.8rem !important;padding-right:.8rem !important;}
  .iz-logo{width:34px;height:34px;}
  .iz-wordmark{font-size:21px;}
  .today-head h1{font-size:29px;}
  .info-card{padding:14px 15px;border-radius:18px;}
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


# ---------- CABECERA ----------
brand_col, voice_col, menu_col = st.columns([5.4, 1.05, 1.05], vertical_alignment="center")
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
    if st.button("🎙️", key="voice_top", help="Nueva nota rápida"):
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

    pendientes = [t for t in st.session_state.tareas if not t["hecha"] and t.get("fecha") == str(date.today())]
    eventos_hoy = [e for e in st.session_state.eventos if e.get("fecha") == str(date.today())]

    st.markdown('<div class="section-label">✅ Tareas de hoy</div>', unsafe_allow_html=True)
    if pendientes:
        items = "".join(f"<li>{t['texto']}</li>" for t in pendientes[:4])
        st.markdown(f'<div class="info-card"><ul class="compact-list">{items}</ul></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-card"><p>No tienes tareas pendientes para hoy.</p></div>', unsafe_allow_html=True)
    if st.button("Ver y gestionar tareas", key="home_tareas"):
        go("Tareas")

    st.markdown('<div class="section-label">📍 Eventos de hoy</div>', unsafe_allow_html=True)
    if eventos_hoy:
        eventos_html = "".join(
            f"<p><strong>{e['hora']}</strong> · {e['titulo']}<br><span class='muted'>{e['lugar']}</span></p>"
            for e in eventos_hoy[:3]
        )
        st.markdown(f'<div class="info-card">{eventos_html}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-card"><p>No hay eventos añadidos para hoy.</p></div>', unsafe_allow_html=True)
    if st.button("Abrir calendario", key="home_cal"):
        go("Calendario")

    st.markdown('<div class="section-label">🎙️ Notas rápidas</div>', unsafe_allow_html=True)
    ultimas = st.session_state.semillero[:3]
    notas_html = "".join(f"<p><strong>{item['tipo']}:</strong> {item['texto']}</p>" for item in ultimas)
    st.markdown(f'<div class="info-card">{notas_html or "<p>No hay notas todavía.</p>"}</div>', unsafe_allow_html=True)
    if st.button("Nueva nota o abrir Semillero", key="home_sem"):
        go("Semillero")

    st.markdown('<div class="section-label">📰 Noticias y oportunidades</div>', unsafe_allow_html=True)
    noticias_html = "".join(
        f"<p><strong>{n['titulo']}</strong><br><span class='muted'>{n['detalle']}</span></p>"
        for n in st.session_state.noticias[:3]
    )
    st.markdown(f'<div class="info-card">{noticias_html}</div>', unsafe_allow_html=True)
    if st.button("Abrir Radar", key="home_radar"):
        go("Radar")

    st.markdown('<div class="section-label">👥 Contactos rápidos</div>', unsafe_allow_html=True)
    contactos_html = "".join(
        f"<p><strong>{c['nombre']}</strong> · {c['tipo']}<br><span class='muted'>{c['nota']}</span></p>"
        for c in st.session_state.contactos[:3]
    )
    st.markdown(f'<div class="info-card">{contactos_html}</div>', unsafe_allow_html=True)
    if st.button("Abrir contactos", key="home_rel"):
        go("Relaciones")

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

    if hasattr(st, "audio_input"):
        audio = st.audio_input("Grabar nota de voz")
        if audio is not None:
            st.audio(audio)
            texto_audio = st.text_input("Título o resumen de la nota", key="audio_summary")
            if st.button("Guardar nota de voz", key="save_audio"):
                resumen = texto_audio.strip() or f"Nota de voz {datetime.now().strftime('%H:%M')}"
                st.session_state.semillero.insert(
                    0,
                    {"tipo": "Nota de voz", "texto": resumen, "estado": "Por organizar", "fecha": str(date.today())},
                )
                st.success("Nota de voz añadida al Semillero.")
                st.rerun()

    with st.form("nueva_semilla", clear_on_submit=True):
        tipo = st.selectbox("Tipo", ["Idea", "Nota", "Contacto", "Evento", "Noticia", "Concurso", "Relato"])
        texto = st.text_area("Contenido", placeholder="Guarda aquí algo que todavía no sabes dónde colocar...")
        submitted = st.form_submit_button("Guardar en Semillero")
        if submitted and texto.strip():
            st.session_state.semillero.insert(
                0,
                {"tipo": tipo, "texto": texto.strip(), "estado": "Por organizar", "fecha": str(date.today())},
            )
            st.success("Guardado en Semillero.")
            st.rerun()

    for idx, item in enumerate(st.session_state.semillero):
        with st.container(border=True):
            st.subheader(item["tipo"])
            st.write(item["texto"])
            st.caption(f"{item.get('estado', 'Por organizar')} · {item.get('fecha', '')}")
            if st.button("Eliminar", key=f"delete_seed_{idx}"):
                st.session_state.semillero.pop(idx)
                st.rerun()


def tareas() -> None:
    st.title("✅ Tareas")
    with st.form("nueva_tarea", clear_on_submit=True):
        texto = st.text_input("Nueva tarea")
        fecha_tarea = st.date_input("Fecha", value=date.today())
        add = st.form_submit_button("Añadir")
        if add and texto.strip():
            st.session_state.tareas.append({"texto": texto.strip(), "hecha": False, "fecha": str(fecha_tarea)})
            st.success("Tarea añadida.")
            st.rerun()

    for i, tarea in enumerate(list(st.session_state.tareas)):
        cols = st.columns([5.5, 1.2])
        with cols[0]:
            nueva = st.checkbox(
                f"{tarea['texto']} · {tarea.get('fecha', '')}", value=tarea["hecha"], key=f"task_{i}"
            )
            st.session_state.tareas[i]["hecha"] = nueva
        with cols[1]:
            if st.button("🗑️", key=f"del_task_{i}", help="Eliminar tarea"):
                st.session_state.tareas.pop(i)
                st.rerun()


def radar() -> None:
    st.title("🧭 Radar")
    tabs = st.tabs(["⭐ Recomendado", "🎤 Eventos", "🏆 Concursos", "📰 Noticias"])
    with tabs[0]:
        for noticia in st.session_state.noticias:
            with st.container(border=True):
                st.subheader(noticia["titulo"])
                st.write(noticia["detalle"])
    with tabs[1]:
        st.write("Eventos literarios y culturales para revisar.")
    with tabs[2]:
        st.write("Concursos pendientes de clasificar.")
    with tabs[3]:
        with st.form("nueva_noticia", clear_on_submit=True):
            titulo = st.text_input("Titular")
            detalle = st.text_input("Detalle o enlace")
            if st.form_submit_button("Añadir noticia") and titulo.strip():
                st.session_state.noticias.insert(0, {"titulo": titulo.strip(), "detalle": detalle.strip()})
                st.rerun()


def estudio() -> None:
    st.title("🎬 Estudio")
    with st.container(border=True):
        st.subheader("Banco de contenido")
        st.write("¿Sabías que...? sobre libros antiguos")
        st.write("Vídeo: una foto, una historia")


def calendario() -> None:
    st.title("📅 Calendario")
    with st.form("nuevo_evento", clear_on_submit=True):
        titulo = st.text_input("Evento")
        fecha_evento = st.date_input("Fecha", value=date.today())
        hora = st.time_input("Hora")
        lugar = st.text_input("Lugar")
        if st.form_submit_button("Añadir evento") and titulo.strip():
            st.session_state.eventos.append(
                {"titulo": titulo.strip(), "fecha": str(fecha_evento), "hora": hora.strftime("%H:%M"), "lugar": lugar.strip()}
            )
            st.success("Evento añadido.")
            st.rerun()

    for idx, evento in enumerate(sorted(st.session_state.eventos, key=lambda e: (e.get("fecha", ""), e.get("hora", "")))):
        with st.container(border=True):
            st.subheader(evento["titulo"])
            st.write(f"{evento.get('fecha', '')} · {evento.get('hora', '')}")
            st.caption(evento.get("lugar", ""))
            if st.button("Eliminar evento", key=f"del_event_{idx}"):
                st.session_state.eventos.remove(evento)
                st.rerun()


def relaciones() -> None:
    st.title("🤝 Contactos")
    with st.form("nuevo_contacto", clear_on_submit=True):
        nombre = st.text_input("Nombre")
        tipo = st.selectbox("Tipo", ["Editorial", "Librería", "Biblioteca", "Autor/a", "Prensa", "Club de lectura", "Otro"])
        nota = st.text_input("Nota rápida")
        if st.form_submit_button("Guardar contacto") and nombre.strip():
            st.session_state.contactos.insert(0, {"nombre": nombre.strip(), "tipo": tipo, "nota": nota.strip()})
            st.success("Contacto guardado.")
            st.rerun()

    for idx, contacto in enumerate(st.session_state.contactos):
        with st.container(border=True):
            st.subheader(contacto["nombre"])
            st.write(contacto["tipo"])
            st.caption(contacto["nota"])
            if st.button("Eliminar contacto", key=f"del_contact_{idx}"):
                st.session_state.contactos.pop(idx)
                st.rerun()


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
            st.rerun()
    for idx, idea in enumerate(st.session_state.ideas_app):
        with st.container(border=True):
            st.write(idea)
            st.caption("Nueva")
            if st.button("Eliminar", key=f"del_idea_{idx}"):
                st.session_state.ideas_app.pop(idx)
                st.rerun()


def ajustes() -> None:
    st.title("⚙️ Ajustes")
    st.info("En esta fase los datos se conservan mientras la sesión de Streamlit permanece activa. La conexión permanente con Google Drive será el siguiente paso técnico.")


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

ROUTES.get(st.session_state.page, centro)()
