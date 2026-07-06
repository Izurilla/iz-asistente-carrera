import streamlit as st
from datetime import datetime

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")

# ---------- CSS ----------
st.markdown("""
<style>
:root{--bg:#f7efe6;--card:#fffaf4;--ink:#26211d;--muted:#766f68;--line:#eadccf;--accent:#211d19;--soft:#efe1d3;--purple:#6b5b95;}
.stApp{background:linear-gradient(180deg,#fbf5ee 0%,#f4eadf 100%); color:var(--ink);} 
.block-container{max-width:760px; padding-top:1.2rem; padding-bottom:8rem;}
h1,h2,h3{letter-spacing:-.02em;}
.hero{background:linear-gradient(135deg,#fffaf4,#ead9c8);border:1px solid var(--line);border-radius:28px;padding:26px 28px;margin:8px 0 18px;box-shadow:0 14px 35px rgba(60,40,20,.08)}
.hero h1{font-size:34px;margin:0 0 8px;font-weight:800}.hero p{font-size:17px;color:var(--muted);margin:0;line-height:1.55}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:12px 0 18px}.kpi{background:rgba(255,250,244,.82);border:1px solid var(--line);border-radius:20px;padding:14px 10px;text-align:center;box-shadow:0 8px 20px rgba(60,40,20,.05)}.kpi strong{display:block;font-size:28px;color:var(--purple);line-height:1}.kpi span{font-size:13px;color:var(--muted)}
.card{background:rgba(255,250,244,.9);border:1px solid var(--line);border-radius:24px;padding:20px;margin:14px 0;box-shadow:0 12px 30px rgba(60,40,20,.06)}
.card h2{font-size:23px;margin:0 0 12px}.card p,.card li{font-size:16px;line-height:1.6}.muted{color:var(--muted)}
.pill{display:inline-flex;align-items:center;gap:6px;background:#efe2d7;border-radius:999px;padding:7px 11px;margin:4px;font-size:13px;color:#3d352f}.tag{background:#ece8ff;color:#4b3d78}
.nav{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);width:min(720px,92vw);background:rgba(255,250,244,.94);backdrop-filter:blur(10px);border:1px solid var(--line);border-radius:24px;padding:10px;display:flex;justify-content:space-between;gap:8px;box-shadow:0 16px 40px rgba(40,30,20,.18);z-index:1000}.nav button{border:0;background:#fff;border:1px solid var(--line);border-radius:16px;padding:10px 12px;font-weight:700;min-width:82px}.mic{position:fixed;left:50%;bottom:86px;transform:translateX(-50%);width:72px;height:72px;border-radius:26px;background:#211d19;color:#fff;display:flex;align-items:center;justify-content:center;font-size:32px;box-shadow:0 16px 35px rgba(0,0,0,.28);z-index:1001}
.stButton>button{border-radius:18px;border:1px solid var(--line);background:#fffaf4;color:#211d19;font-weight:700}.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"]{border-radius:16px!important}
@media(max-width:640px){.block-container{padding-left:1rem;padding-right:1rem}.hero{padding:22px}.hero h1{font-size:29px}.grid{grid-template-columns:repeat(2,1fr)}.nav button{min-width:auto;font-size:12px;padding:9px 8px}.mic{bottom:82px}}
</style>
""", unsafe_allow_html=True)

# ---------- State ----------
if "page" not in st.session_state:
    st.session_state.page = "Centro"
if "items" not in st.session_state:
    st.session_state.items = [
        {"tipo":"🎙️ Nota de voz", "texto":"Ideas para vídeos de curiosidades históricas", "estado":"Por organizar"},
        {"tipo":"💡 Idea", "texto":"Serie: una foto, una historia", "estado":"Por organizar"},
    ]
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"texto":"Preparar base de contactos", "zona":"Hoy", "hecha":False},
        {"texto":"Crear banco de contenidos", "zona":"Semana", "hecha":False},
        {"texto":"Revisar agenda cultural", "zona":"Hoy", "hecha":False},
    ]
if "ideas_app" not in st.session_state:
    st.session_state.ideas_app = ["Mejorar dashboard móvil", "Añadir calendario real", "Conectar Drive"]

# ---------- Helpers ----------
def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def card(title, body_html):
    st.markdown(f'<div class="card"><h2>{title}</h2>{body_html}</div>', unsafe_allow_html=True)

def kpis():
    pendientes = sum(1 for t in st.session_state.tasks if not t["hecha"])
    semillas = len(st.session_state.items)
    oportunidades = 4
    ideas = len(st.session_state.ideas_app)
    st.markdown(f'''
    <div class="grid">
      <div class="kpi"><strong>{pendientes}</strong><span>Tareas</span></div>
      <div class="kpi"><strong>{semillas}</strong><span>Semillas</span></div>
      <div class="kpi"><strong>{oportunidades}</strong><span>Radar</span></div>
      <div class="kpi"><strong>{ideas}</strong><span>Ideas app</span></div>
    </div>
    ''', unsafe_allow_html=True)

def nav():
    cols = st.columns(5)
    labels = [("🏠", "Centro"), ("🌱", "Semillero"), ("✅", "Tareas"), ("🧭", "Radar"), ("☰", "Más")]
    for col, (ico, page) in zip(cols, labels):
        with col:
            if st.button(f"{ico}\n{page}", key=f"nav_{page}", use_container_width=True):
                st.session_state.page = page
                st.rerun()
    st.markdown('<div class="mic">🎙️</div>', unsafe_allow_html=True)

# ---------- Pages ----------
def centro():
    hero("Centro de Operaciones", "Buenos días, Irene · Aquí está lo que necesita tu atención.")
    kpis()
    card("🎯 Prioridades", "<ul><li>Preparar base de contactos</li><li>Crear banco de contenidos</li><li>Revisar agenda cultural</li></ul>")
    card("🧭 Brújula", "<p>Esta semana no intentaría hacerlo todo. Prioridad: dejar listo el sistema y empezar a mover la marca.</p>")
    card("🌱 Semillero", f"<p><strong>{len(st.session_state.items)}</strong> elementos por organizar.</p><p class='muted'>Notas, ideas, contactos y oportunidades entran aquí antes de decidir su destino.</p>")
    card("🔥 Radar rápido", "<ul><li>Presentación en FNAC Callao · Madrid</li><li>Concurso de relato histórico · cierra en 16 días</li><li>Buscar eventos de librerías en Getafe/Leganés</li></ul>")
    card("☕ Consejo de Dirección", "<p>No intentes hacerlo todo hoy. Primero dejamos funcionando el sistema; después construimos el plan de carrera.</p>")

def semillero():
    hero("🌱 Semillero", "Todo lo que todavía no tiene destino definitivo.")
    with st.form("nuevo_item"):
        tipo = st.selectbox("Tipo", ["🎙️ Nota de voz", "💡 Idea", "👤 Contacto", "📅 Evento", "📰 Noticia", "🏆 Concurso", "📌 Tarea"])
        texto = st.text_area("Contenido", placeholder="Escribe o transcribe aquí lo que quieres guardar...")
        ok = st.form_submit_button("Guardar en Semillero")
        if ok and texto.strip():
            st.session_state.items.insert(0, {"tipo": tipo, "texto": texto.strip(), "estado":"Por organizar"})
            st.success("Guardado en Semillero")
    for i, item in enumerate(st.session_state.items):
        with st.container(border=True):
            st.markdown(f"**{item['tipo']}** · {item['estado']}")
            st.write(item["texto"])
            if st.button("Marcar como organizado", key=f"org_{i}"):
                st.session_state.items.pop(i)
                st.rerun()

def tareas():
    hero("✅ Tareas", "Lo que hay que hacer, sin convertirlo en una lista infinita.")
    with st.form("nueva_tarea"):
        texto = st.text_input("Nueva tarea")
        zona = st.selectbox("Zona", ["Hoy", "Semana", "Próximamente", "Algún día"])
        if st.form_submit_button("Añadir tarea") and texto.strip():
            st.session_state.tasks.append({"texto":texto.strip(), "zona":zona, "hecha":False})
            st.success("Tarea añadida")
    for zona in ["Hoy", "Semana", "Próximamente", "Algún día"]:
        st.markdown(f"### {zona}")
        for idx, task in enumerate(st.session_state.tasks):
            if task["zona"] == zona:
                task["hecha"] = st.checkbox(task["texto"], value=task["hecha"], key=f"task_{idx}")

def radar():
    hero("🧭 Radar", "Oportunidades, eventos, concursos y señales del entorno literario.")
    for title, meta, tag in [
        ("Presentación en FNAC Callao", "Madrid · mañana 19:00", "Presentación"),
        ("Concurso de relato histórico", "Online · cierra en 16 días", "Concurso"),
        ("Agenda cultural Getafe/Leganés", "Buscar eventos de librerías", "Pendiente"),
        ("Artículo sobre lectura infantil", "Posible contenido para Cuentos Tita Nene", "Noticia"),
    ]:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(meta)
            st.markdown(f'<span class="pill tag">{tag}</span>', unsafe_allow_html=True)
            if st.button("Guardar en Semillero", key=f"rad_{title}"):
                st.session_state.items.insert(0, {"tipo":"🔥 Oportunidad", "texto":f"{title} · {meta}", "estado":"Por organizar"})
                st.success("Guardado")

def mas():
    hero("☰ Más", "Módulos de trabajo del Asistente de Carrera.")
    tab1, tab2, tab3, tab4 = st.tabs(["🎬 Estudio", "📚 Libros", "🤝 Relaciones", "💡 Ideas app"])
    with tab1:
        card("🎬 Estudio Editorial", "<p>Banco de contenidos, guiones, grabaciones, programación y publicaciones.</p><p><span class='pill'>247 ideas</span><span class='pill'>12 por grabar</span><span class='pill'>18 programadas</span></p>")
    with tab2:
        card("📚 Libros", "<p><strong>Libro activo:</strong> El libro mágico de Hugo e Inés</p><p>Estado: campaña inicial / preparación de visibilidad.</p>")
    with tab3:
        card("🤝 Relaciones", "<p>Contactos de librerías, bibliotecas, autores, prensa, editoriales e ilustradores.</p><p class='muted'>Próximo paso: crear base de contactos.</p>")
    with tab4:
        with st.form("idea_app"):
            idea = st.text_input("Nueva idea para mejorar la app")
            if st.form_submit_button("Guardar idea") and idea.strip():
                st.session_state.ideas_app.insert(0, idea.strip())
                st.success("Idea guardada")
        for idea in st.session_state.ideas_app:
            st.write(f"💡 {idea}")

# ---------- Render ----------
page = st.session_state.page
if page == "Centro": centro()
elif page == "Semillero": semillero()
elif page == "Tareas": tareas()
elif page == "Radar": radar()
else: mas()

nav()
