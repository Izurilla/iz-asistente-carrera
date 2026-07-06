import streamlit as st
from datetime import datetime

st.set_page_config(page_title='IZ | Asistente de Carrera', page_icon='🧭', layout='centered')

# ---------- Estado ----------
def init_state():
    defaults = {
        'page': 'Centro de Operaciones',
        'seed_items': [
            {'tipo': 'Nota de voz', 'texto': 'Idea para vídeo: ¿sabías que...? sobre libros antiguos', 'estado': 'Por organizar'},
            {'tipo': 'Idea', 'texto': 'Serie: una foto, una historia', 'estado': 'Por organizar'},
        ],
        'tasks': ['Revisar calendario + noticias', 'Preparar base de contactos', 'Crear banco de contenidos'],
        'ideas_app': ['Menú desplegable más compacto', 'Cards clicables', 'Botón de notas de voz que no tape contenido'],
        'voice_text': '',
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

PAGES = [
    'Centro de Operaciones',
    'Semillero',
    'Tareas',
    'Radar',
    'Estudio',
    'Calendario',
    'Relaciones',
    'Libros y relatos',
    'Ideas para la app',
    'Dirección',
]

# ---------- Estilos ----------
st.markdown('''
<style>
:root{
  --bg:#fbf4ea; --card:#fffdf8; --ink:#1f1f24; --muted:#736b66;
  --line:#eadccc; --accent:#6f5797; --soft:#f1e4d6; --dark:#211d1a;
}
html, body, [data-testid="stAppViewContainer"] { background: var(--bg); }
[data-testid="stHeader"] { background: rgba(251,244,234,.92); }
[data-testid="stToolbar"] { right: .5rem; }
.block-container { padding: 1.1rem 1rem 6.2rem; max-width: 780px; }
h1,h2,h3,p,li,label,span { color: var(--ink); }
.iz-top { display:flex; align-items:center; justify-content:space-between; margin:.35rem 0 1rem; }
.iz-logo { font-size:1.55rem; font-weight:800; letter-spacing:-.03em; }
.version { font-size:.85rem; color:var(--muted); border:1px solid var(--line); padding:.35rem .7rem; border-radius:999px; background:#fff8f0; }
.hero { background:linear-gradient(135deg,#fffdf8,#eddbc7); border:1px solid var(--line); border-radius:24px; padding:1.35rem; box-shadow:0 12px 26px rgba(58,39,25,.08); margin:.8rem 0 1rem; }
.hero h1 { margin:0 0 .35rem; font-size:2.1rem; line-height:1.05; letter-spacing:-.04em; }
.hero p { margin:0; color:var(--muted); font-size:1.04rem; }
.kpi-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:.55rem; margin:.8rem 0 1rem; }
.kpi-card { background:var(--card); border:1px solid var(--line); border-radius:18px; padding:.75rem .45rem; text-align:center; box-shadow:0 8px 20px rgba(58,39,25,.06); cursor:pointer; }
.kpi-card strong { display:block; font-size:1.55rem; color:var(--accent); line-height:1; }
.kpi-card span { display:block; color:var(--muted); font-size:.78rem; margin-top:.25rem; }
.card { background:var(--card); border:1px solid var(--line); border-radius:22px; padding:1rem; box-shadow:0 12px 28px rgba(58,39,25,.07); margin:.8rem 0; }
.card.clickable { cursor:pointer; transition: transform .12s ease, box-shadow .12s ease; }
.card.clickable:active { transform:scale(.99); }
.card-title { font-size:1.22rem; font-weight:800; margin-bottom:.4rem; display:flex; align-items:center; gap:.3rem; }
.card p, .card li { color:var(--muted); font-size:.98rem; }
.pills { display:flex; gap:.45rem; flex-wrap:wrap; margin-top:.6rem; }
.pill { background:var(--soft); border:1px solid #e3d0bf; padding:.35rem .7rem; border-radius:999px; font-size:.86rem; color:#3b332d; }
.mic-fab { position:fixed; right:18px; bottom:78px; z-index:999; width:74px; height:74px; border-radius:24px; background:var(--dark); color:white; display:flex; align-items:center; justify-content:center; font-size:2rem; box-shadow:0 12px 34px rgba(0,0,0,.26); border:8px solid rgba(255,255,255,.55); }
.mic-label { position:fixed; right:12px; bottom:52px; z-index:999; background:rgba(33,29,26,.92); color:white; border-radius:999px; padding:.25rem .55rem; font-size:.72rem; }
.menu-hint { font-size:.82rem; color:var(--muted); text-align:center; margin:.3rem 0 .55rem; }
.small-note { background:#f4efe8; border:1px solid var(--line); padding:.75rem; border-radius:16px; color:var(--muted); }
.stSelectbox > div > div { border-radius:16px !important; }
.stButton > button { border-radius:16px; border:1px solid var(--line); background:var(--card); color:var(--ink); min-height:3rem; }
.stButton > button:hover { border-color:#cdb9a5; background:#fff7ed; color:var(--ink); }
.nav-grid { display:grid; grid-template-columns:1fr 1fr; gap:.55rem; margin:.6rem 0 1rem; }
@media(max-width:520px){
  .block-container { padding-left:.85rem; padding-right:.85rem; }
  .hero { padding:1.15rem; border-radius:24px; }
  .hero h1 { font-size:1.75rem; }
  .kpi-grid { grid-template-columns:repeat(4,1fr); gap:.38rem; }
  .kpi-card { border-radius:16px; padding:.65rem .25rem; }
  .kpi-card strong { font-size:1.25rem; }
  .kpi-card span { font-size:.68rem; }
  .card { padding:.95rem; border-radius:20px; }
}
</style>
''', unsafe_allow_html=True)

# ---------- Navegación ----------
def set_page(name):
    st.session_state.page = name
    st.rerun()

def header():
    st.markdown("<div class='iz-top'><div class='iz-logo'>🧭 IZ</div><div class='version'>V2.5 estable</div></div>", unsafe_allow_html=True)
    selected = st.selectbox('Menú', PAGES, index=PAGES.index(st.session_state.page), label_visibility='collapsed', key='menu_select')
    if selected != st.session_state.page:
        st.session_state.page = selected
        st.rerun()
    st.markdown("<div class='menu-hint'>Menú compacto · las cards principales son accesos rápidos</div>", unsafe_allow_html=True)

# ---------- Componentes ----------
def hero(title, subtitle):
    st.markdown(f"""
    <div class='hero'>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def kpi(label, value, target):
    if st.button(f"{value}\n{label}", key=f'kpi_{label}', use_container_width=True):
        set_page(target)

def card(title, body, target=None, pills=None, key=None):
    klass = 'card clickable' if target else 'card'
    st.markdown(f"<div class='{klass}'><div class='card-title'>{title}</div><div>{body}</div>", unsafe_allow_html=True)
    if pills:
        pill_html = ''.join([f"<span class='pill'>{p}</span>" for p in pills])
        st.markdown(f"<div class='pills'>{pill_html}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if target:
        if st.button('Abrir', key=key or f'open_{target}_{title}', use_container_width=True):
            set_page(target)

# ---------- Páginas ----------
def centro():
    hero('Centro de Operaciones', 'Buenos días, Irene · Aquí está lo que necesita tu atención.')
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi('Tareas', len(st.session_state.tasks), 'Tareas')
    with c2: kpi('Semillas', len(st.session_state.seed_items), 'Semillero')
    with c3: kpi('Oportunidades', 4, 'Radar')
    with c4: kpi('Eventos', 2, 'Calendario')

    card('🎯 Prioridad del día', '<ul><li>Preparar base de contactos</li><li>Crear banco de contenidos</li><li>Revisar agenda cultural</li></ul>', 'Tareas', key='prioridad')
    card('🔥 Radar rápido', '<p>4 oportunidades detectadas para revisar esta semana.</p>', 'Radar', ['Madrid','Librerías','Concursos'], key='radar_rapido')
    card('📚 Libro activo', '<p><b>El libro mágico de Hugo e Inés</b><br>Fase: preparación de publicación.</p>', 'Libros y relatos', key='libro_activo')
    card('🎙️ Última nota de voz', '<p>Idea para vídeo: ¿sabías que...? sobre libros antiguos.<br><br><span style="color:#736b66">Estado: por organizar</span></p>', 'Semillero', key='ultima_nota')

def semillero():
    hero('Semillero', 'Todo lo que todavía no tiene sitio definitivo.')
    tipo = st.selectbox('Tipo', ['Nota de voz','Idea','Contacto','Evento','Noticia','Concurso','Relato'], key='tipo_semilla')
    texto = st.text_area('Contenido', placeholder='Guarda aquí algo que todavía no sabes dónde colocar...', key='texto_semilla')
    if st.button('Guardar en Semillero', use_container_width=True):
        if texto.strip():
            st.session_state.seed_items.append({'tipo': tipo, 'texto': texto.strip(), 'estado': 'Por organizar'})
            st.success('Guardado en Semillero')
    for i, item in enumerate(st.session_state.seed_items):
        card(f"{item['tipo']}", f"<p>{item['texto']}</p><span class='pill'>{item['estado']}</span>", key=f'seed_{i}')

def tareas():
    hero('Tareas', 'Lo pendiente sin perder de vista la semana.')
    nueva = st.text_input('Nueva tarea', key='nueva_tarea')
    if st.button('Añadir tarea', use_container_width=True):
        if nueva.strip():
            st.session_state.tasks.append(nueva.strip())
            st.success('Tarea añadida')
    st.markdown("<div class='card'><div class='card-title'>🔥 Hoy</div>", unsafe_allow_html=True)
    for i, task in enumerate(st.session_state.tasks):
        st.checkbox(task, key=f'task_{i}')
    st.markdown('</div>', unsafe_allow_html=True)
    card('🗓️ Esta semana', '<p>Preparar base de contactos · Crear banco de contenidos · Revisar agenda cultural.</p>')

def radar():
    hero('Radar', 'Oportunidades, eventos, concursos y vida cultural.')
    tab1, tab2, tab3, tab4 = st.tabs(['⭐ Recomendado','🎤 Eventos','🏆 Concursos','📰 Noticias'])
    with tab1:
        card('Oportunidad', '<p>Presentación en FNAC Callao · Madrid</p>', 'Calendario', ['Revisar'])
        card('Oportunidad', '<p>Buscar eventos de librerías en Getafe/Leganés</p>', 'Relaciones', ['Madrid sur'])
    with tab2:
        card('Evento', '<p>Actividad literaria de fin de semana pendiente de revisar.</p>', 'Calendario')
    with tab3:
        card('Concurso', '<p>Concurso de relato histórico · cierra en 16 días.</p>', 'Libros y relatos')
    with tab4:
        card('Noticia', '<p>Noticias del sector editorial pendientes de conectar en una versión futura.</p>')

def estudio():
    hero('Estudio', 'Contenido para redes, vídeos, publicaciones y campañas.')
    card('💡 Ideas', '<p>Curiosidades de libros · Historia · Una foto, una historia.</p>')
    card('🎙️ Por grabar', '<p>Vídeo sobre primer bestseller · Presentación de autora.</p>')
    card('📅 Programado', '<p>Post domingo · Cuentos Tita Nene.</p>')

def calendario():
    hero('Calendario', 'Fechas clave, publicaciones y eventos.')
    card('Hoy', '<p>Revisar radar · Preparar ideas · Ordenar tareas.</p>')
    card('Esta semana', '<p>Radar viernes · Reunión de dirección domingo.</p>')
    card('Fechas clave', '<p>Día del Libro · Sant Jordi · Navidad · Campaña de lanzamiento.</p>')

def relaciones():
    hero('Relaciones', 'Contactos que construir y cuidar.')
    card('Librerías', '<p>FNAC Callao · Casa del Libro · Librerías Madrid sur.</p>')
    card('Bibliotecas', '<p>Getafe · Leganés · Majadahonda · Madrid.</p>')
    card('Seguimientos', '<p>Personas a revisar cada cierto tiempo.</p>')

def libros():
    hero('Libros y relatos', 'Todo lo terminado o en fase de publicación, se publique o no.')
    card('El libro mágico de Hugo e Inés', '<p>Estado: preparación de publicación · Infantil · Cuentos Tita Nene.</p>')
    card('Preludio de un ocaso', '<p>Relato terminado · Posible envío a concurso.</p>')
    card('Añadir obra', '<p>Aquí irán cuentos, relatos, libros terminados y proyectos listos para mover.</p>')

def ideas_app():
    hero('Ideas para la app', 'Mejoras que se te ocurren mientras usas el sistema.')
    idea = st.text_area('Nueva idea para la app', placeholder='Ej: Que el menú sea más compacto...', key='idea_app_text')
    if st.button('Guardar idea para la app', use_container_width=True):
        if idea.strip():
            st.session_state.ideas_app.append(idea.strip())
            st.success('Idea guardada')
    for i, idea_txt in enumerate(st.session_state.ideas_app):
        card('💡 Idea', f'<p>{idea_txt}</p><span class="pill">Nueva</span>', key=f'idea_app_{i}')

def direccion():
    hero('Dirección', 'Decisiones, enfoque semanal y rumbo de carrera.')
    card('☕ Consejo de Dirección', '<p>No intentes hacerlo todo. Prioridad: sistema estable + base de contactos + contenido adelantado.</p>')
    card('📌 Regla de estabilidad', '<p>No modificar lo que funciona. Cambios pequeños y seguros.</p>')

# ---------- Main ----------
header()
page = st.session_state.page
if page == 'Centro de Operaciones': centro()
elif page == 'Semillero': semillero()
elif page == 'Tareas': tareas()
elif page == 'Radar': radar()
elif page == 'Estudio': estudio()
elif page == 'Calendario': calendario()
elif page == 'Relaciones': relaciones()
elif page == 'Libros y relatos': libros()
elif page == 'Ideas para la app': ideas_app()
elif page == 'Dirección': direccion()

# Botón flotante visual de notas de voz
st.markdown("<div class='mic-fab'>🎙️</div><div class='mic-label'>Notas de voz</div>", unsafe_allow_html=True)
