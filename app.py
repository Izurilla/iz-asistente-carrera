import streamlit as st
from datetime import date, datetime, timedelta

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")

st.markdown("""
<style>
:root { --bg:#f8f1e8; --card:#fffaf3; --ink:#24211d; --muted:#766e64; --accent:#24211d; --soft:#eadfce; }
.stApp { background: linear-gradient(180deg,#fbf5ed 0%,#f5eadc 100%); color: var(--ink); }
.block-container { max-width: 760px; padding-top: 1.5rem; padding-bottom: 6rem; }
.hero { background: linear-gradient(135deg,#fffaf3,#eadfce); padding: 28px; border-radius: 26px; border:1px solid #eadfce; box-shadow:0 10px 30px rgba(70,50,30,.08); margin-bottom:24px; }
.card { background:#fffaf3; border:1px solid #eadfce; border-radius:22px; padding:20px; margin:14px 0; box-shadow:0 8px 24px rgba(70,50,30,.06); }
.small { color:#766e64; font-size:.95rem; }
.pill { display:inline-block; padding:7px 12px; background:#eee2d2; border-radius:999px; margin:3px; font-size:.88rem; }
.nav { position:fixed; left:0; right:0; bottom:0; z-index:999; background:rgba(255,250,243,.95); border-top:1px solid #eadfce; padding:10px 8px; box-shadow:0 -8px 25px rgba(70,50,30,.10); }
.mic { position:fixed; bottom:48px; left:50%; transform:translateX(-50%); z-index:1000; background:#211d18; color:white; border-radius:28px; padding:18px 26px; box-shadow:0 10px 30px rgba(0,0,0,.25); font-size:28px; }
.version { float:right; background:#eee2d2; border-radius:999px; padding:8px 14px; color:#766e64; font-size:.9rem; }
button[kind="primary"] { background:#211d18!important; border-radius:18px!important; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Despacho"
if "inbox" not in st.session_state:
    st.session_state.inbox = []
if "tasks" not in st.session_state:
    st.session_state.tasks = ["Revisar calendario + noticias", "Dejar una nota de voz para septiembre", "Preparar 3 ideas de vídeo"]
if "ideas" not in st.session_state:
    st.session_state.ideas = ["¿Sabías que...? libros antiguos", "Una foto, una historia", "Por qué Irene Zurilla escribe"]

pages = ["Despacho", "Jornada", "Radar", "Estudio", "Más"]

def set_page(p):
    st.session_state.page = p

st.markdown("<span class='version'>V0.8 beta</span>", unsafe_allow_html=True)
st.markdown("### 🧭 IZ | Asistente de Carrera")

page = st.session_state.page

if page == "Despacho":
    saludo = "Buenos días" if datetime.now().hour < 14 else "Buenas tardes" if datetime.now().hour < 21 else "Buenas noches"
    st.markdown(f"""
    <div class='hero'>
      <h1>{saludo}, Irene</h1>
      <p class='small'>Tu despacho de autora · versión con bandeja de entrada</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>🧭 Brújula</h3><p>Hoy revisaría <b>calendario + noticias</b> y dejaría una nota de voz con cualquier idea para septiembre.</p></div>", unsafe_allow_html=True)
    st.subheader("🎯 Prioridades")
    for t in st.session_state.tasks:
        st.checkbox(t, key=f"task_{t}")
    st.subheader("🔥 Oportunidades")
    st.markdown("""
• Presentación en FNAC Callao · Madrid  
• Concurso de relato histórico · cierra en 16 días  
• Buscar eventos de librerías en Getafe/Leganés
""")
    st.subheader("📥 Bandeja de entrada")
    if st.session_state.inbox:
        for item in st.session_state.inbox[-3:][::-1]:
            st.markdown(f"<div class='card'><b>{item['tipo']}</b><br>{item['texto']}<br><span class='small'>{item['fecha']}</span></div>", unsafe_allow_html=True)
    else:
        st.info("Aún no has enviado nada al Asistente.")

elif page == "Jornada":
    st.markdown("<div class='hero'><h1>📅 Jornada</h1><p class='small'>Hoy, mañana y esta semana.</p></div>", unsafe_allow_html=True)
    nueva = st.text_input("Nueva tarea rápida")
    if st.button("+ Añadir tarea") and nueva:
        st.session_state.tasks.append(nueva)
        st.rerun()
    for t in st.session_state.tasks:
        st.checkbox(t, key=f"j_{t}")
    st.markdown("<div class='card'><h3>Esta semana</h3><p>12 tareas · 7 hechas · 5 pendientes</p></div>", unsafe_allow_html=True)

elif page == "Radar":
    st.markdown("<div class='hero'><h1>📰 Radar</h1><p class='small'>Noticias, eventos y oportunidades.</p></div>", unsafe_allow_html=True)
    tabs = st.tabs(["Eventos", "Noticias", "Concursos", "Madrid"])
    with tabs[0]:
        st.markdown("<div class='card'><b>Presentación en FNAC Callao</b><br>Mañana · 19:00 · Madrid</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'><b>Firma de libros</b><br>Librería Alberti · Viernes</div>", unsafe_allow_html=True)
    with tabs[1]:
        st.markdown("<div class='card'><b>Tendencias del sector editorial</b><br>Guardar para posible Reel.</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'><b>Lectura infantil</b><br>Idea para Cuentos Tita Nene.</div>", unsafe_allow_html=True)
    with tabs[2]:
        st.markdown("<div class='card'><b>Concurso de relato histórico</b><br>Cierra en 16 días.</div>", unsafe_allow_html=True)
    with tabs[3]:
        st.markdown("<div class='card'><b>Madrid Literario</b><br>Priorizar eventos de tarde y fines de semana.</div>", unsafe_allow_html=True)

elif page == "Estudio":
    st.markdown("<div class='hero'><h1>🎬 Estudio Editorial</h1><p class='small'>Banco de contenidos y producción.</p></div>", unsafe_allow_html=True)
    idea = st.text_input("Nueva idea de contenido")
    if st.button("+ Guardar idea") and idea:
        st.session_state.ideas.append(idea)
        st.rerun()
    st.subheader("💡 Ideas")
    for idea in st.session_state.ideas:
        st.markdown(f"<div class='card'>💡 {idea}</div>", unsafe_allow_html=True)
    st.markdown("<span class='pill'>Guion: 3</span><span class='pill'>Grabar: 2</span><span class='pill'>Programado: 1</span>", unsafe_allow_html=True)

else:
    st.markdown("<div class='hero'><h1>☰ Más</h1><p class='small'>Relaciones, libros, marca, dirección y Drive.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>🤝 Relaciones</h3><p>Librerías, editoriales, bibliotecas, autores, prensa.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>📚 Libros</h3><p>Libro activo: El libro mágico de Hugo e Inés.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>🛡 Marca</h3><p>Irene Zurilla · Cuentos Tita Nene · dominios · registro.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>☁️ Drive</h3><p>Próxima fase: tus datos vivirán en Google Drive.</p></div>", unsafe_allow_html=True)

with st.expander("🎙 Cuéntamelo al Director", expanded=False):
    tipo = st.selectbox("Tipo", ["💡 Idea", "🤝 Contacto", "🎤 Evento", "📅 Recordatorio", "📰 Noticia", "📝 Nota libre"])
    texto = st.text_area("¿Qué quieres contarme hoy?", placeholder="Ej: Acabo de salir de una presentación. He conocido a Ana, librera en Getafe...")
    if st.button("🧭 Enviar al Asistente", type="primary") and texto:
        st.session_state.inbox.append({"tipo": tipo, "texto": texto, "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")})
        st.success("Guardado en Bandeja de entrada del Despacho.")

st.markdown("<div class='mic'>🎙</div>", unsafe_allow_html=True)
st.markdown("<div class='nav'>", unsafe_allow_html=True)
cols = st.columns(5)
for col, p, icon in zip(cols, pages, ["🏠", "📅", "📰", "🎬", "☰"]):
    with col:
        st.button(f"{icon}\n{p}", key=f"nav_{p}", on_click=set_page, args=(p,), use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
