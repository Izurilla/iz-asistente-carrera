import streamlit as st
from datetime import datetime

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")

st.markdown("""
<style>
:root{--bg:#fbf4ea;--card:#fffaf2;--ink:#241f1b;--muted:#7d7166;--line:#eadcca;--accent:#4b3f72;--dark:#1f1b17;}
[data-testid="stAppViewContainer"]{background:linear-gradient(180deg,#fffaf3 0%,#f6eadc 100%);} 
.block-container{padding-top:1.1rem; padding-bottom:7rem; max-width:720px;}
h1,h2,h3,p,li,div,span{font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color:var(--ink);} 
.hero{background:linear-gradient(135deg,#fffaf2,#eadccb); border:1px solid var(--line); border-radius:30px; padding:24px 24px; box-shadow:0 16px 35px rgba(70,48,27,.08); margin-bottom:16px;}
.hero h1{font-size:34px; margin:0 0 6px 0; line-height:1.1;}
.hero p{font-size:17px; color:var(--muted); margin:0;}
.grid{display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin:12px 0 16px;}
.kpi{background:#efe2d4; border-radius:22px; padding:15px 8px; text-align:center; border:1px solid #ead9c7;}
.kpi strong{display:block; color:var(--accent); font-size:28px; line-height:1;}
.kpi span{font-size:13px; color:#4b4139; font-weight:650;}
.card{background:rgba(255,250,242,.92); border:1px solid var(--line); border-radius:26px; padding:18px 20px; box-shadow:0 14px 30px rgba(70,48,27,.07); margin:12px 0;}
.card h3{margin:0 0 10px; font-size:22px;}
.compact-list{margin:0; padding-left:18px; line-height:1.9; font-size:16px;}
.pillrow{display:flex; gap:9px; flex-wrap:wrap; margin-top:10px;}
.pill{background:#fff; border:1px solid #eadcca; border-radius:999px; padding:8px 12px; font-size:14px; font-weight:650;}
.voice-float{position:fixed; left:50%; transform:translateX(-50%); bottom:22px; z-index:9999; width:78px; height:78px; background:#211d19; border-radius:28px; box-shadow:0 12px 35px rgba(0,0,0,.28); display:flex; align-items:center; justify-content:center; border:8px solid rgba(255,255,255,.85);}
.voice-float span{font-size:36px; color:white;}
.nav{position:fixed; left:0; right:0; bottom:0; background:rgba(255,250,242,.96); border-top:1px solid #e8d8c5; padding:10px 10px 104px; display:flex; justify-content:center; gap:8px; z-index:9998; backdrop-filter: blur(10px);} 
.nav a{background:white; border:1px solid #eadcca; border-radius:18px; padding:10px 13px; text-decoration:none; color:#2b241e; font-size:13px; font-weight:700; box-shadow:0 4px 12px rgba(70,48,27,.05);} 
.small-note{color:var(--muted); font-size:14px; margin-top:8px;}
.section-title{font-size:26px; font-weight:800; margin:22px 0 8px;}
.stButton>button{border-radius:18px; background:#211d19; color:white; border:0; padding:.7rem 1rem; font-weight:800; width:100%;}
.stTextArea textarea,.stTextInput input{border-radius:18px!important;}
@media(max-width:640px){.block-container{padding-left:1rem; padding-right:1rem;} .hero h1{font-size:28px}.grid{grid-template-columns:repeat(2,1fr)} .nav a{font-size:12px; padding:9px 10px}.voice-float{bottom:18px}}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Centro"
if "items" not in st.session_state:
    st.session_state.items = [
        {"tipo":"💡 Idea", "texto":"Serie de vídeos: curiosidades de libros e historia", "estado":"Por organizar"},
        {"tipo":"🎙️ Nota", "texto":"Preparar banco de contenidos para septiembre", "estado":"Por organizar"},
    ]
if "tasks" not in st.session_state:
    st.session_state.tasks = ["Preparar base de contactos", "Crear banco de contenidos", "Revisar agenda cultural"]
if "app_ideas" not in st.session_state:
    st.session_state.app_ideas = ["Mejorar dashboard móvil", "Añadir calendario real", "Conectar Drive"]

def go(page):
    st.session_state.page = page

def nav_buttons():
    c1,c2,c3,c4,c5 = st.columns(5)
    if c1.button("🏠 Centro", use_container_width=True): go("Centro")
    if c2.button("🌱 Semillero", use_container_width=True): go("Semillero")
    if c3.button("✅ Tareas", use_container_width=True): go("Tareas")
    if c4.button("🧭 Radar", use_container_width=True): go("Radar")
    if c5.button("☰ Más", use_container_width=True): go("Mas")


def voice_box():
    with st.expander("🎙️ Notas de voz / captura rápida", expanded=False):
        tipo = st.selectbox("Tipo", ["🎙️ Nota de voz", "💡 Idea", "✅ Tarea", "📅 Evento", "🤝 Contacto", "📰 Noticia", "💡 Idea para la app"])
        texto = st.text_area("Escribe o pega aquí lo que quieras guardar", placeholder="Ej: Se me ocurre un vídeo sobre bibliotecas antiguas...")
        if st.button("Guardar en la app"):
            if texto.strip():
                if tipo == "✅ Tarea":
                    st.session_state.tasks.append(texto.strip())
                elif tipo == "💡 Idea para la app":
                    st.session_state.app_ideas.append(texto.strip())
                else:
                    st.session_state.items.append({"tipo": tipo, "texto": texto.strip(), "estado": "Por organizar"})
                st.success("Guardado.")
            else:
                st.warning("Escribe algo antes de guardar.")

def centro():
    hora = datetime.now().hour
    saludo = "Buenos días" if hora < 14 else "Buenas tardes" if hora < 21 else "Buenas noches"
    st.markdown(f"""
    <div class='hero'>
      <h1>Centro de Operaciones</h1>
      <p>{saludo}, Irene · Aquí está lo que necesita tu atención.</p>
    </div>
    <div class='grid'>
      <div class='kpi'><strong>{len(st.session_state.tasks)}</strong><span>Tareas</span></div>
      <div class='kpi'><strong>{len(st.session_state.items)}</strong><span>Semillero</span></div>
      <div class='kpi'><strong>4</strong><span>Radar</span></div>
      <div class='kpi'><strong>{len(st.session_state.app_ideas)}</strong><span>Ideas app</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='card'><h3>🎯 Prioridad de hoy</h3><ul class='compact-list'><li>Dejar estable el sistema.</li><li>Recuperar la usabilidad del dashboard.</li><li>No añadir más módulos hasta que el Centro funcione bien.</li></ul></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>🧭 Brújula</h3><p>Esta versión vuelve a ser un panel de control: menos scroll, más decisión rápida y acciones visibles.</p><div class='pillrow'><span class='pill'>Móvil primero</span><span class='pill'>Notas de voz</span><span class='pill'>Centro visual</span></div></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>🔥 Radar rápido</h3><ul class='compact-list'><li>Presentaciones en Madrid y alrededores.</li><li>Concursos abiertos.</li><li>Noticias editoriales que puedan servir para contenido.</li></ul></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>📚 Libro activo</h3><p><strong>El libro mágico de Hugo e Inés</strong></p><p class='small-note'>Campaña infantil en preparación · Presentaciones, colegios y Majadahonda como territorio prioritario.</p></div>", unsafe_allow_html=True)
    voice_box()

def semillero():
    st.markdown("<div class='hero'><h1>🌱 Semillero</h1><p>Todo lo que todavía está por organizar.</p></div>", unsafe_allow_html=True)
    voice_box()
    for i, item in enumerate(st.session_state.items):
        st.markdown(f"<div class='card'><h3>{item['tipo']}</h3><p>{item['texto']}</p><span class='pill'>{item['estado']}</span></div>", unsafe_allow_html=True)

def tareas():
    st.markdown("<div class='hero'><h1>✅ Tareas</h1><p>Lo que mueve la carrera esta semana.</p></div>", unsafe_allow_html=True)
    nueva = st.text_input("Nueva tarea")
    if st.button("Añadir tarea") and nueva.strip():
        st.session_state.tasks.append(nueva.strip())
        st.success("Tarea añadida.")
    st.markdown("<div class='section-title'>🔥 Hoy</div>", unsafe_allow_html=True)
    for idx, t in enumerate(st.session_state.tasks):
        st.checkbox(t, key=f"task_{idx}")

def radar():
    st.markdown("<div class='hero'><h1>🧭 Radar</h1><p>Oportunidades para visibilidad, contactos y contenidos.</p></div>", unsafe_allow_html=True)
    oportunidades = [
        ("🎤 Presentaciones", "Revisar FNAC, Casa del Libro y librerías independientes de Madrid."),
        ("🏆 Concursos", "Buscar convocatorias para relatos inéditos y oportunidades infantiles."),
        ("🏛 Madrid cultural", "Priorizar eventos desde las 18:30 entre semana y fines de semana."),
        ("📰 Noticias", "Guardar noticias de libros, historia y escritura para vídeos cortos."),
    ]
    for title, txt in oportunidades:
        st.markdown(f"<div class='card'><h3>{title}</h3><p>{txt}</p></div>", unsafe_allow_html=True)

def estudio():
    st.markdown("<div class='hero'><h1>🎬 Estudio</h1><p>Producción de contenido con semanas de ventaja.</p></div>", unsafe_allow_html=True)
    cols = st.columns(3)
    cols[0].metric("Ideas", "247")
    cols[1].metric("Guiones", "18")
    cols[2].metric("Programados", "6")
    st.markdown("<div class='card'><h3>Próximos contenidos</h3><ul class='compact-list'><li>¿Sabías que...? libros antiguos</li><li>Una foto, una historia</li><li>Por qué Irene Zurilla escribe</li></ul></div>", unsafe_allow_html=True)

def mas():
    st.markdown("<div class='hero'><h1>☰ Más</h1><p>Módulos de gestión.</p></div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    if c1.button("🎬 Estudio", use_container_width=True): go("Estudio")
    if c2.button("💡 Ideas app", use_container_width=True): go("IdeasApp")
    if c1.button("📅 Calendario", use_container_width=True): go("Calendario")
    if c2.button("🤝 Relaciones", use_container_width=True): go("Relaciones")
    if c1.button("📚 Libros", use_container_width=True): go("Libros")
    if c2.button("📈 Dirección", use_container_width=True): go("Direccion")

def simple_page(title, subtitle, body):
    st.markdown(f"<div class='hero'><h1>{title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'>{body}</div>", unsafe_allow_html=True)

def ideas_app():
    st.markdown("<div class='hero'><h1>💡 Ideas para la app</h1><p>Mejoras que iremos revisando por versiones.</p></div>", unsafe_allow_html=True)
    nueva = st.text_input("Nueva idea para la app")
    if st.button("Guardar idea") and nueva.strip():
        st.session_state.app_ideas.append(nueva.strip())
        st.success("Idea guardada.")
    for idea in st.session_state.app_ideas:
        st.markdown(f"<div class='card'><p>💡 {idea}</p><span class='pill'>Nueva</span></div>", unsafe_allow_html=True)

# Render
page = st.session_state.page
if page == "Centro": centro()
elif page == "Semillero": semillero()
elif page == "Tareas": tareas()
elif page == "Radar": radar()
elif page == "Estudio": estudio()
elif page == "IdeasApp": ideas_app()
elif page == "Calendario": simple_page("📅 Calendario", "Fechas clave, eventos y publicaciones.", "<p>Próxima fase: vista semanal y mensual.</p>")
elif page == "Relaciones": simple_page("🤝 Relaciones", "Contactos profesionales y seguimiento.", "<p>Librerías, editoriales, bibliotecas, autores, prensa e ilustradores.</p>")
elif page == "Libros": simple_page("📚 Libros", "Estado de obras y campañas.", "<p>Libro activo: <strong>El libro mágico de Hugo e Inés</strong>.</p>")
elif page == "Direccion": simple_page("📈 Dirección", "Consejo estratégico de autora.", "<p>Reunión domingo tarde · Radar viernes · revisión mensual.</p>")

nav_buttons()
st.markdown("<div class='voice-float'><span>🎙️</span></div>", unsafe_allow_html=True)
