import base64
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

import streamlit as st

try:
    import gspread
    from google.oauth2.service_account import Credentials
except Exception:
    gspread = None
    Credentials = None

st.set_page_config(
    page_title="IZ | Asistente de Carrera",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

VERSION = "V3.2 · Persistencia Drive"
DATA_KEYS = ("semillero", "tareas", "eventos", "contactos", "noticias", "ideas_app")

DEFAULTS = {
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


class SheetsStore:
    def __init__(self) -> None:
        self.enabled = False
        self.error = ""
        self.worksheet = None
        self._connect()

    def _connect(self) -> None:
        if gspread is None or Credentials is None:
            self.error = "Faltan dependencias de Google Sheets."
            return
        try:
            if "google_service_account" not in st.secrets or "spreadsheet_id" not in st.secrets:
                self.error = "Google Sheets aún no está configurado."
                return
            info = dict(st.secrets["google_service_account"])
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.file",
            ]
            creds = Credentials.from_service_account_info(info, scopes=scopes)
            client = gspread.authorize(creds)
            spreadsheet = client.open_by_key(st.secrets["spreadsheet_id"])
            try:
                self.worksheet = spreadsheet.worksheet("app_data")
            except gspread.WorksheetNotFound:
                self.worksheet = spreadsheet.add_worksheet(title="app_data", rows=50, cols=3)
                self.worksheet.update("A1:C1", [["key", "json", "updated_at"]])
            self.enabled = True
        except Exception as exc:
            self.error = f"No se pudo conectar con Google Sheets: {exc}"

    def load_all(self) -> dict[str, Any]:
        if not self.enabled or self.worksheet is None:
            return {}
        try:
            rows = self.worksheet.get_all_records()
            result: dict[str, Any] = {}
            for row in rows:
                key = str(row.get("key", "")).strip()
                raw = row.get("json", "")
                if key in DATA_KEYS and raw:
                    result[key] = json.loads(raw)
            return result
        except Exception as exc:
            self.error = f"No se pudieron leer los datos: {exc}"
            self.enabled = False
            return {}

    def save(self, key: str, value: Any) -> bool:
        if not self.enabled or self.worksheet is None:
            return False
        try:
            raw = json.dumps(value, ensure_ascii=False)
            cell = self.worksheet.find(key, in_column=1)
            now = datetime.now().isoformat(timespec="seconds")
            if cell:
                self.worksheet.update(f"B{cell.row}:C{cell.row}", [[raw, now]])
            else:
                self.worksheet.append_row([key, raw, now], value_input_option="RAW")
            return True
        except Exception as exc:
            self.error = f"No se pudo guardar {key}: {exc}"
            self.enabled = False
            return False


@st.cache_resource
def get_store() -> SheetsStore:
    return SheetsStore()


store = get_store()


def init_state() -> None:
    if "page" not in st.session_state:
        st.session_state.page = "Centro de Operaciones"
    if "data_loaded" not in st.session_state:
        cloud_data = store.load_all() if store.enabled else {}
        for key in DATA_KEYS:
            st.session_state[key] = cloud_data.get(key, DEFAULTS[key].copy())
        st.session_state.data_loaded = True


def persist(key: str) -> None:
    if store.enabled:
        ok = store.save(key, st.session_state[key])
        if not ok:
            st.toast("No se pudo guardar en Drive. Revisa Ajustes.", icon="⚠️")


init_state()

st.markdown(
    """
<style>
:root{--bg:#fbf5ec;--card:#fffdf8;--line:#e5d5c7;--text:#1f1e22;--muted:#776e67;--accent:#7d5fa0;}
html, body, [data-testid="stAppViewContainer"] {background:radial-gradient(circle at top,#fffaf1 0%,#fbf5ec 42%,#f3e7d8 100%);}
[data-testid="stHeader"]{height:1.9rem!important;background:rgba(255,255,255,.36)!important;}
.block-container{padding-top:.25rem!important;padding-bottom:2rem!important;max-width:740px!important;}
.iz-brand-row{display:flex;align-items:center;gap:8px}.iz-logo{width:38px;height:38px;border-radius:50%;object-fit:cover;box-shadow:0 5px 15px rgba(60,45,30,.10)}
.iz-wordmark{font-size:22px;font-weight:850;letter-spacing:-.04em}.version{color:var(--muted);font-size:11px;margin-top:1px}
.today-head{margin:.45rem 0 .55rem}.today-head h1{margin:0;font-size:32px;line-height:1.05;letter-spacing:-.045em}.today-head p{margin:6px 0 0;color:var(--muted);font-size:15px}
.section-label{font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:.8rem 0 .2rem}
.info-card{border:1px solid var(--line);border-radius:20px;padding:15px 16px;background:rgba(255,255,255,.88);box-shadow:0 8px 20px rgba(68,45,25,.05);margin:.35rem 0}
.info-card h3{margin:0 0 7px;font-size:18px;letter-spacing:-.025em}.info-card p{margin:4px 0;color:#3d3834;line-height:1.4}.info-card .muted{color:var(--muted);font-size:13px}
.compact-list{margin:0;padding-left:1.1rem}.compact-list li{margin:.28rem 0;color:#3d3834}.status-pill{display:inline-block;padding:5px 10px;border-radius:999px;background:#ead9c9;border:1px solid #dfcdbc;color:#3b332d;font-size:12px;margin-top:6px}
.stButton>button{width:100%;border-radius:15px!important;min-height:40px;border:1px solid var(--line);background:rgba(255,255,255,.84);color:var(--text)}
[data-testid="stPopover"]>button{border-radius:15px!important;min-height:40px}[data-testid="stVerticalBlockBorderWrapper"]{border-radius:20px!important;border-color:var(--line)!important;background:rgba(255,255,255,.72)}
.menu-title{font-size:12px;font-weight:850;letter-spacing:.09em;color:var(--muted);margin:8px 0 3px}.cloud-ok,.cloud-warn{font-size:12px;padding:7px 10px;border-radius:12px;margin:3px 0 8px}.cloud-ok{background:#e8f4e8;color:#2d6333}.cloud-warn{background:#fff1d8;color:#7b5720}
@media(max-width:520px){.block-container{padding-left:.8rem!important;padding-right:.8rem!important}.iz-logo{width:34px;height:34px}.iz-wordmark{font-size:21px}.today-head h1{font-size:29px}.info-card{padding:14px 15px;border-radius:18px}}
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


brand_col, voice_col, menu_col = st.columns([5.4, 1.05, 1.05], vertical_alignment="center")
with brand_col:
    st.markdown(f'<div class="iz-brand-row">{logo_html()}<div><div class="iz-wordmark">IZ</div><div class="version">{VERSION}</div></div></div>', unsafe_allow_html=True)
with voice_col:
    if st.button("🎙️", key="voice_top", help="Nueva nota rápida"):
        go("Semillero")
with menu_col:
    with st.popover("☰", help="Abrir menú"):
        st.markdown('<div class="menu-title">HOY</div>', unsafe_allow_html=True)
        if st.button("🏠 Centro de Operaciones", key="m_centro"): go("Centro de Operaciones")
        if st.button("✅ Tareas", key="m_tareas"): go("Tareas")
        if st.button("📅 Calendario", key="m_cal"): go("Calendario")
        st.markdown('<div class="menu-title">ESCRITURA</div>', unsafe_allow_html=True)
        if st.button("🌱 Semillero", key="m_sem"): go("Semillero")
        if st.button("🎬 Estudio", key="m_estudio"): go("Estudio")
        if st.button("📚 Libros y relatos", key="m_libros"): go("Libros y relatos")
        st.markdown('<div class="menu-title">CARRERA</div>', unsafe_allow_html=True)
        if st.button("🧭 Radar", key="m_radar"): go("Radar")
        if st.button("🤝 Contactos", key="m_rel"): go("Relaciones")
        st.markdown('<div class="menu-title">APP</div>', unsafe_allow_html=True)
        if st.button("💡 Ideas para la app", key="m_ideas"): go("Ideas para la app")
        if st.button("⚙️ Ajustes", key="m_ajustes"): go("Ajustes")

if store.enabled:
    st.markdown('<div class="cloud-ok">☁️ Guardado permanente activo en Google Drive</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="cloud-warn">⚠️ Modo temporal: configura Google Sheets en Ajustes para conservar los datos.</div>', unsafe_allow_html=True)


def centro() -> None:
    st.markdown('<div class="today-head"><h1>Hoy</h1><p>Lo que necesitas saber para organizar tu día como autora.</p></div>', unsafe_allow_html=True)
    pendientes = [t for t in st.session_state.tareas if not t["hecha"] and t.get("fecha") == str(date.today())]
    eventos_hoy = [e for e in st.session_state.eventos if e.get("fecha") == str(date.today())]
    st.markdown('<div class="section-label">✅ Tareas de hoy</div>', unsafe_allow_html=True)
    if pendientes:
        items = "".join(f"<li>{t['texto']}</li>" for t in pendientes[:4])
        st.markdown(f'<div class="info-card"><ul class="compact-list">{items}</ul></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-card"><p>No tienes tareas pendientes para hoy.</p></div>', unsafe_allow_html=True)
    if st.button("Ver y gestionar tareas", key="home_tareas"): go("Tareas")
    st.markdown('<div class="section-label">📍 Eventos de hoy</div>', unsafe_allow_html=True)
    if eventos_hoy:
        html = "".join(f"<p><strong>{e['hora']}</strong> · {e['titulo']}<br><span class='muted'>{e['lugar']}</span></p>" for e in eventos_hoy[:3])
        st.markdown(f'<div class="info-card">{html}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-card"><p>No hay eventos añadidos para hoy.</p></div>', unsafe_allow_html=True)
    if st.button("Abrir calendario", key="home_cal"): go("Calendario")
    st.markdown('<div class="section-label">🎙️ Notas rápidas</div>', unsafe_allow_html=True)
    notas_html = "".join(f"<p><strong>{item['tipo']}:</strong> {item['texto']}</p>" for item in st.session_state.semillero[:3])
    st.markdown(f'<div class="info-card">{notas_html or "<p>No hay notas todavía.</p>"}</div>', unsafe_allow_html=True)
    if st.button("Nueva nota o abrir Semillero", key="home_sem"): go("Semillero")
    st.markdown('<div class="section-label">📰 Noticias y oportunidades</div>', unsafe_allow_html=True)
    news_html = "".join(f"<p><strong>{n['titulo']}</strong><br><span class='muted'>{n['detalle']}</span></p>" for n in st.session_state.noticias[:3])
    st.markdown(f'<div class="info-card">{news_html}</div>', unsafe_allow_html=True)
    if st.button("Abrir Radar", key="home_radar"): go("Radar")
    st.markdown('<div class="section-label">👥 Contactos rápidos</div>', unsafe_allow_html=True)
    contacts_html = "".join(f"<p><strong>{c['nombre']}</strong> · {c['tipo']}<br><span class='muted'>{c['nota']}</span></p>" for c in st.session_state.contactos[:3])
    st.markdown(f'<div class="info-card">{contacts_html}</div>', unsafe_allow_html=True)
    if st.button("Abrir contactos", key="home_rel"): go("Relaciones")
    st.markdown('<div class="section-label">📚 Proyecto activo</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card"><h3>El libro mágico de Hugo e Inés</h3><p>Fase: preparación editorial y planificación de lanzamiento.</p><span class="status-pill">En marcha</span></div>', unsafe_allow_html=True)
    if st.button("Ver libros y relatos", key="home_libros"): go("Libros y relatos")


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
                st.session_state.semillero.insert(0, {"tipo":"Nota de voz","texto":resumen,"estado":"Por organizar","fecha":str(date.today())})
                persist("semillero")
                st.success("Nota de voz añadida al Semillero.")
                st.rerun()
    with st.form("nueva_semilla", clear_on_submit=True):
        tipo = st.selectbox("Tipo", ["Idea","Nota","Contacto","Evento","Noticia","Concurso","Relato"])
        texto = st.text_area("Contenido", placeholder="Guarda aquí algo que todavía no sabes dónde colocar...")
        submitted = st.form_submit_button("Guardar en Semillero")
        if submitted and texto.strip():
            st.session_state.semillero.insert(0, {"tipo":tipo,"texto":texto.strip(),"estado":"Por organizar","fecha":str(date.today())})
            persist("semillero")
            st.success("Guardado en Semillero.")
            st.rerun()
    for idx, item in enumerate(st.session_state.semillero):
        with st.container(border=True):
            st.subheader(item["tipo"]); st.write(item["texto"]); st.caption(f"{item.get('estado','Por organizar')} · {item.get('fecha','')}")
            if st.button("Eliminar", key=f"delete_seed_{idx}"):
                st.session_state.semillero.pop(idx); persist("semillero"); st.rerun()


def tareas() -> None:
    st.title("✅ Tareas")
    with st.form("nueva_tarea", clear_on_submit=True):
        texto = st.text_input("Nueva tarea"); fecha_tarea = st.date_input("Fecha", value=date.today())
        if st.form_submit_button("Añadir") and texto.strip():
            st.session_state.tareas.append({"texto":texto.strip(),"hecha":False,"fecha":str(fecha_tarea)})
            persist("tareas"); st.success("Tarea añadida."); st.rerun()
    for i, tarea in enumerate(list(st.session_state.tareas)):
        cols = st.columns([5.5,1.2])
        with cols[0]:
            nueva = st.checkbox(f"{tarea['texto']} · {tarea.get('fecha','')}", value=tarea["hecha"], key=f"task_{i}")
            if nueva != st.session_state.tareas[i]["hecha"]:
                st.session_state.tareas[i]["hecha"] = nueva; persist("tareas")
        with cols[1]:
            if st.button("🗑️", key=f"del_task_{i}", help="Eliminar tarea"):
                st.session_state.tareas.pop(i); persist("tareas"); st.rerun()


def radar() -> None:
    st.title("🧭 Radar")
    tabs = st.tabs(["⭐ Recomendado","🎤 Eventos","🏆 Concursos","📰 Noticias"])
    with tabs[0]:
        for noticia in st.session_state.noticias:
            with st.container(border=True): st.subheader(noticia["titulo"]); st.write(noticia["detalle"])
    with tabs[1]: st.write("Eventos literarios y culturales para revisar.")
    with tabs[2]: st.write("Concursos pendientes de clasificar.")
    with tabs[3]:
        with st.form("nueva_noticia", clear_on_submit=True):
            titulo = st.text_input("Titular"); detalle = st.text_input("Detalle o enlace")
            if st.form_submit_button("Añadir noticia") and titulo.strip():
                st.session_state.noticias.insert(0,{"titulo":titulo.strip(),"detalle":detalle.strip()}); persist("noticias"); st.rerun()


def estudio() -> None:
    st.title("🎬 Estudio")
    with st.container(border=True): st.subheader("Banco de contenido"); st.write("¿Sabías que...? sobre libros antiguos"); st.write("Vídeo: una foto, una historia")


def calendario() -> None:
    st.title("📅 Calendario")
    with st.form("nuevo_evento", clear_on_submit=True):
        titulo = st.text_input("Evento"); fecha_evento = st.date_input("Fecha", value=date.today()); hora = st.time_input("Hora"); lugar = st.text_input("Lugar")
        if st.form_submit_button("Añadir evento") and titulo.strip():
            st.session_state.eventos.append({"titulo":titulo.strip(),"fecha":str(fecha_evento),"hora":hora.strftime("%H:%M"),"lugar":lugar.strip()})
            persist("eventos"); st.success("Evento añadido."); st.rerun()
    for idx, evento in enumerate(sorted(st.session_state.eventos, key=lambda e:(e.get("fecha",""),e.get("hora","")))):
        with st.container(border=True):
            st.subheader(evento["titulo"]); st.write(f"{evento.get('fecha','')} · {evento.get('hora','')}"); st.caption(evento.get("lugar",""))
            if st.button("Eliminar evento", key=f"del_event_{idx}"):
                st.session_state.eventos.remove(evento); persist("eventos"); st.rerun()


def relaciones() -> None:
    st.title("🤝 Contactos")
    with st.form("nuevo_contacto", clear_on_submit=True):
        nombre = st.text_input("Nombre"); tipo = st.selectbox("Tipo", ["Editorial","Librería","Biblioteca","Autor/a","Prensa","Club de lectura","Otro"]); nota = st.text_input("Nota rápida")
        if st.form_submit_button("Guardar contacto") and nombre.strip():
            st.session_state.contactos.insert(0,{"nombre":nombre.strip(),"tipo":tipo,"nota":nota.strip()}); persist("contactos"); st.success("Contacto guardado."); st.rerun()
    for idx, contacto in enumerate(st.session_state.contactos):
        with st.container(border=True):
            st.subheader(contacto["nombre"]); st.write(contacto["tipo"]); st.caption(contacto["nota"])
            if st.button("Eliminar contacto", key=f"del_contact_{idx}"):
                st.session_state.contactos.pop(idx); persist("contactos"); st.rerun()


def libros() -> None:
    st.title("📚 Libros y relatos"); st.caption("Todo lo terminado o en campaña, esté publicado o no.")
    with st.container(border=True): st.subheader("El libro mágico de Hugo e Inés"); st.write("Estado: preparación de publicación.")
    with st.container(border=True): st.subheader("Preludio de un ocaso"); st.write("Relato terminado · posible concurso.")


def ideas_app() -> None:
    st.title("💡 Ideas para la app")
    with st.form("idea_app", clear_on_submit=True):
        idea = st.text_input("Nueva idea de mejora")
        if st.form_submit_button("Guardar idea") and idea.strip():
            st.session_state.ideas_app.insert(0,idea.strip()); persist("ideas_app"); st.success("Idea guardada."); st.rerun()
    for idx, idea in enumerate(st.session_state.ideas_app):
        with st.container(border=True):
            st.write(idea); st.caption("Nueva")
            if st.button("Eliminar", key=f"del_idea_{idx}"):
                st.session_state.ideas_app.pop(idx); persist("ideas_app"); st.rerun()


def ajustes() -> None:
    st.title("⚙️ Ajustes")
    if store.enabled:
        st.success("Google Sheets está conectado. Los datos se guardan de forma permanente y aparecen en móvil, tablet y PC.")
        if st.button("Forzar recarga desde Drive"):
            cloud = store.load_all()
            for key in DATA_KEYS:
                if key in cloud: st.session_state[key] = cloud[key]
            st.success("Datos recargados."); st.rerun()
    else:
        st.warning("La app está en modo temporal.")
        st.write("Para activar el guardado permanente:")
        st.markdown("1. Crea una hoja de Google Sheets.\n2. Crea una cuenta de servicio en Google Cloud.\n3. Comparte la hoja con el correo de esa cuenta como Editor.\n4. Añade las credenciales y el ID de la hoja en **Streamlit → Manage app → Settings → Secrets**.")
        st.info("Consulta el archivo README_PERSISTENCIA.md incluido en el ZIP para completar la conexión segura.")
        if store.error: st.caption(store.error)


ROUTES = {"Centro de Operaciones":centro,"Semillero":semillero,"Tareas":tareas,"Radar":radar,"Estudio":estudio,"Calendario":calendario,"Relaciones":relaciones,"Libros y relatos":libros,"Ideas para la app":ideas_app,"Ajustes":ajustes}
ROUTES.get(st.session_state.page, centro)()
