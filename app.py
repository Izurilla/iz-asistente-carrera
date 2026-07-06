import streamlit as st
from datetime import datetime

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")

CSS = """
<style>
:root{--bg:#f7efe4;--card:#fffaf2;--soft:#eadfce;--ink:#1f1d1b;--muted:#71675d;--accent:#7b5fa4;--dark:#1f1b18;}
.stApp{background:linear-gradient(180deg,#fbf4ea 0%,#f1e3d2 100%); color:var(--ink);} 
.block-container{max-width:720px!important; padding:1rem 1rem 7rem!important;}
[data-testid="stHeader"]{background:transparent;}
.hero{background:linear-gradient(135deg,#fff8ef,#ead8c4); border:1px solid #e4d6c5; border-radius:28px; padding:24px; box-shadow:0 18px 45px rgba(70,43,20,.08); margin-bottom:16px;}
.hero h1{font-size:2.1rem; margin:0 0 6px 0; line-height:1.05;}
.hero p{font-size:1rem; color:var(--muted); margin:0;}
.topbar{display:flex; align-items:center; justify-content:space-between; gap:12px; margin:.3rem 0 1rem;}
.brand{display:flex; align-items:center; gap:8px; font-weight:800; font-size:1.45rem;}
.badge{border:1px solid #e1d2c0; background:#fff8ef; border-radius:999px; padding:8px 14px; color:#695d52; font-size:.9rem;}
.card{background:rgba(255,250,242,.88); border:1px solid #e5d8c7; border-radius:24px; padding:20px; margin:14px 0; box-shadow:0 14px 36px rgba(70,43,20,.07);}
.card h2,.card h3{margin-top:0;}
.kpis{display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin:12px 0;}
.kpi{background:#fffaf2; border:1px solid #e5d8c7; border-radius:18px; padding:14px 8px; text-align:center; box-shadow:0 8px 20px rgba(70,43,20,.05);}
.kpi strong{display:block; font-size:1.55rem; color:#5f477f;}
.kpi span{font-size:.78rem; color:#504840;}
.module-grid{display:grid; grid-template-columns:repeat(2,1fr); gap:10px;}
.module{background:#fffaf2; border:1px solid #e5d8c7; border-radius:18px; padding:16px; font-weight:700; text-align:center;}
.fab{position:fixed; left:50%; transform:translateX(-50%); bottom:22px; z-index:9999; width:86px; height:86px; border-radius:30px; background:#201c19; display:flex; align-items:center; justify-content:center; color:white; font-size:38px; box-shadow:0 14px 38px rgba(0,0,0,.28),0 0 0 12px rgba(255,255,255,.48);}
.small{color:var(--muted); font-size:.92rem;}
.pill{display:inline-block; background:#eadfce; border:1px solid #dccab8; border-radius:999px; padding:8px 14px; margin:4px 4px 4px 0;}
hr{border:0; border-top:1px solid #e5d8c7; margin:16px 0;}
button[kind="secondary"]{border-radius:999px!important;}
.stButton>button{border-radius:999px!important; border:1px solid #dfcfbd!important; background:#fffaf2!important;}
.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"]{border-radius:16px!important;}
@media(max-width:520px){.block-container{padding-left:.9rem!important; padding-right:.9rem!important;}.hero h1{font-size:1.7rem}.kpis{grid-template-columns:repeat(2,1fr)}.module-grid{grid-template-columns:1fr}.card{padding:18px}.topbar{align-items:flex-start}.brand{font-size:1.2rem}.fab{width:76px;height:76px;font-size:34px;bottom:18px}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Centro de Operaciones"
if "items" not in st.session_state:
    st.session_state.items = [
        {"tipo":"Nota de voz", "texto":"Idea para vídeo: ¿sabías que...? sobre libros antiguos", "estado":"Por organizar"},
        {"tipo":"Idea", "texto":"Serie: una foto, una historia", "estado":"Por organizar"},
    ]
if "tasks" not in st.session_state:
    st.session_state.tasks = ["Revisar calendario + noticias", "Preparar base de contactos", "Crear banco de contenidos"]
if "app_ideas" not in st.session_state:
    st.session_state.app_ideas = ["Menú compacto en botón de tres puntos", "Notas de voz con grabación real", "Libros debe incluir relatos terminados"]
if "works" not in st.session_state:
    st.session_state.works = [
        {"titulo":"El libro mágico de Hugo e Inés", "tipo":"Cuento infantil", "estado":"En publicación"},
        {"titulo":"Preludio de un ocaso", "tipo":"Relato", "estado":"Terminado"},
    ]

PAGES = ["Centro de Operaciones","Semillero","Tareas","Radar","Estudio","Calendario","Relaciones","Libros y relatos","Noticias","Dirección","Ideas para la app","Ajustes"]

def top():
    st.markdown('<div class="topbar"><div class="brand">🧭 IZ</div><div class="badge">V2.1 móvil</div></div>', unsafe_allow_html=True)
    # Compact menu: selectbox styled as menu, replaces bottom buttons
    page = st.selectbox("☰ Menú", PAGES, index=PAGES.index(st.session_state.page), label_visibility="collapsed")
    st.session_state.page = page

def voice_box():
    with st.expander("🎙️ Notas de voz / captura rápida", expanded=False):
        st.caption("Por ahora guarda texto dictado/escrito. La grabación real de audio será el siguiente paso técnico.")
        tipo = st.selectbox("Tipo", ["Nota de voz","Idea","Contacto","Evento","Recordatorio","Noticia","Concurso","Sugerencia app"], key="voice_tipo")
        texto = st.text_area("Contenido", placeholder="Escribe o dicta desde el teclado del móvil…", key="voice_text")
        if st.button("Guardar", key="save_voice"):
            if texto.strip():
                if tipo == "Sugerencia app":
                    st.session_state.app_ideas.append(texto.strip())
                else:
                    st.session_state.items.insert(0,{"tipo":tipo,"texto":texto.strip(),"estado":"Por organizar"})
                st.success("Guardado.")
            else:
                st.warning("Escribe algo antes de guardar.")

def center():
    st.markdown('<div class="hero"><h1>Centro de Operaciones</h1><p>Buenos días, Irene · Aquí está lo que necesita tu atención.</p></div>', unsafe_allow_html=True)
    st.markdown(f'''<div class="kpis">
    <div class="kpi"><strong>{len(st.session_state.tasks)}</strong><span>Tareas</span></div>
    <div class="kpi"><strong>{len(st.session_state.items)}</strong><span>Semillero</span></div>
    <div class="kpi"><strong>4</strong><span>Oportunidades</span></div>
    <div class="kpi"><strong>2</strong><span>Eventos</span></div>
    </div>''', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>🎯 Prioridad del día</h3><p>Preparar base de contactos · Crear banco de contenidos · Revisar agenda cultural.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>🔥 Radar rápido</h3><p>4 oportunidades detectadas para revisar esta semana.</p><span class="pill">Madrid</span><span class="pill">Librerías</span><span class="pill">Concursos</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>📚 Libro activo</h3><p><b>El libro mágico de Hugo e Inés</b><br><span class="small">Fase: publicación / campaña inicial</span></p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card"><h3>🌱 Semillero</h3><p>{len(st.session_state.items)} elementos por organizar.</p></div>', unsafe_allow_html=True)

def semillero():
    st.title("🌱 Semillero")
    voice_box()
    for i,item in enumerate(st.session_state.items):
        with st.container():
            st.markdown(f'<div class="card"><h3>{item["tipo"]}</h3><p>{item["texto"]}</p><span class="pill">{item["estado"]}</span></div>', unsafe_allow_html=True)

def tareas():
    st.title("✅ Tareas")
    nueva = st.text_input("Nueva tarea")
    if st.button("Añadir tarea") and nueva.strip():
        st.session_state.tasks.append(nueva.strip())
        st.success("Tarea añadida")
    st.subheader("🔥 Hoy")
    done=[]
    for idx,t in enumerate(st.session_state.tasks):
        if st.checkbox(t, key=f"task_{idx}"):
            done.append(idx)
    if done:
        st.caption("Marcadas como hechas en esta sesión.")
    st.markdown('<div class="card"><h3>📅 Esta semana</h3><p>Preparar base de contactos · Crear banco de contenidos · Revisar agenda cultural.</p></div>', unsafe_allow_html=True)

def radar():
    st.title("🧭 Radar")
    tab1,tab2,tab3,tab4 = st.tabs(["⭐ Recomendado","🎤 Eventos","🏆 Concursos","📰 Noticias"])
    with tab1:
        for txt in ["Presentación en FNAC Callao · Madrid", "Concurso de relato histórico · cierra en 16 días", "Buscar eventos de librerías en Getafe/Leganés"]:
            st.markdown(f'<div class="card"><h3>Oportunidad</h3><p>{txt}</p><span class="pill">Revisar</span></div>', unsafe_allow_html=True)
    with tab2: st.info("Aquí iremos conectando agenda cultural de Madrid y alrededores.")
    with tab3: st.info("Aquí aparecerán concursos literarios relevantes.")
    with tab4: st.info("Aquí irán noticias del sector editorial, libros e historia.")

def estudio():
    st.title("🎬 Estudio")
    for title,count in [("Ideas",247),("Guiones",18),("Pendiente de grabar",12),("Programado",18),("Publicado",56)]:
        st.markdown(f'<div class="card"><h3>{title}</h3><p>{count} elementos</p></div>', unsafe_allow_html=True)

def calendario():
    st.title("📅 Calendario")
    st.markdown('<div class="card"><h3>Hoy</h3><p>Revisar radar · Preparar ideas · Grabar nota de voz.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>Esta semana</h3><p>Reunión de dirección el domingo · Radar del fin de semana el viernes.</p></div>', unsafe_allow_html=True)

def relaciones():
    st.title("🤝 Relaciones")
    st.markdown('<div class="card"><h3>Librerías</h3><p>FNAC · Casa del Libro · Librerías de Getafe/Leganés.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>Seguimiento</h3><p>Aquí estarán personas y entidades a revisar cada cierto tiempo.</p></div>', unsafe_allow_html=True)

def libros():
    st.title("📚 Libros y relatos")
    st.caption("Aquí entrará todo lo terminado: publicado, pendiente de publicar, cuentos, relatos y manuscritos cerrados.")
    titulo = st.text_input("Añadir obra terminada o en curso")
    tipo = st.selectbox("Tipo", ["Cuento infantil","Relato","Novela","Artículo","Otro"])
    estado = st.selectbox("Estado", ["Idea","En escritura","Terminado","Enviado","En publicación","Publicado"])
    if st.button("Añadir obra") and titulo.strip():
        st.session_state.works.append({"titulo":titulo.strip(),"tipo":tipo,"estado":estado})
        st.success("Obra añadida")
    for w in st.session_state.works:
        st.markdown(f'<div class="card"><h3>{w["titulo"]}</h3><p>{w["tipo"]} · {w["estado"]}</p></div>', unsafe_allow_html=True)

def noticias():
    st.title("📰 Noticias")
    st.info("Pendiente de conexión web: sector editorial, libros, historia, cultura y eventos.")

def direccion():
    st.title("📈 Dirección")
    st.markdown('<div class="card"><h3>Consejo de Dirección</h3><p>Prioridad: dejar el sistema estable y empezar el plan de carrera en paralelo.</p></div>', unsafe_allow_html=True)

def ideas_app():
    st.title("💡 Ideas para la app")
    idea = st.text_area("Nueva idea o mejora")
    if st.button("Guardar idea") and idea.strip():
        st.session_state.app_ideas.insert(0, idea.strip())
        st.success("Idea guardada")
    for i in st.session_state.app_ideas:
        st.markdown(f'<div class="card"><p>{i}</p><span class="pill">Nueva</span></div>', unsafe_allow_html=True)

def ajustes():
    st.title("⚙️ Ajustes")
    st.markdown('<div class="card"><h3>Drive</h3><p>Pendiente de conectar. La app guardará datos en Drive/Sheets cuando activemos sincronización.</p></div>', unsafe_allow_html=True)

# Render
top()
page=st.session_state.page
if page == "Centro de Operaciones": center()
elif page == "Semillero": semillero()
elif page == "Tareas": tareas()
elif page == "Radar": radar()
elif page == "Estudio": estudio()
elif page == "Calendario": calendario()
elif page == "Relaciones": relaciones()
elif page == "Libros y relatos": libros()
elif page == "Noticias": noticias()
elif page == "Dirección": direccion()
elif page == "Ideas para la app": ideas_app()
elif page == "Ajustes": ajustes()

st.markdown('<div class="fab">🎙️</div>', unsafe_allow_html=True)
