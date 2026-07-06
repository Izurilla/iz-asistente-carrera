import streamlit as st

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")

if "semillero_items" not in st.session_state:
    st.session_state.semillero_items = [
        {"tipo": "Nota de voz", "texto": "Idea para vídeo: ¿sabías que...? sobre libros antiguos", "estado": "Por organizar"},
        {"tipo": "Idea", "texto": "Crear banco de contenidos de septiembre", "estado": "Por organizar"},
    ]
if "tareas" not in st.session_state:
    st.session_state.tareas = ["Revisar calendario + noticias", "Preparar base de contactos", "Crear banco de contenidos"]
if "ideas_app" not in st.session_state:
    st.session_state.ideas_app = ["Menú compacto con tres puntos", "Libros y relatos terminados", "Notas de voz reales"]

st.markdown("""
<style>
.stApp{background:linear-gradient(180deg,#fbf4ea 0%,#f7eadb 100%);color:#191919;}
.block-container{max-width:760px!important;padding-top:1.2rem!important;padding-bottom:6rem!important;}
.hero{background:linear-gradient(135deg,#fffaf4,#ead7c5);border:1px solid #ead9c8;border-radius:28px;padding:28px 30px;margin:8px 0 22px;box-shadow:0 12px 30px rgba(60,40,20,.08)}
.hero h1{font-size:42px;line-height:1.05;margin:0 0 10px;font-weight:900;letter-spacing:-1px;}
.hero p{font-size:18px;color:#746c64;margin:0;}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px 0 22px;}
.kpi{background:#fffaf4;border:1px solid #ead9c8;border-radius:18px;padding:14px 8px;text-align:center;box-shadow:0 8px 18px rgba(60,40,20,.06)}
.kpi b{font-size:28px;color:#5b497e;display:block;}
.kpi span{font-size:13px;color:#4b443e;}
.card{background:#fffaf4;border:1px solid #ead9c8;border-radius:24px;padding:24px 26px;margin:14px 0;box-shadow:0 12px 28px rgba(60,40,20,.07)}
.card h2{font-size:26px;margin:0 0 14px;}
.card p,.card li{font-size:17px;line-height:1.55;}
.badge{display:inline-block;background:#ead7c5;border:1px solid #dec8b5;border-radius:999px;padding:8px 14px;margin:4px 6px 4px 0;color:#2b2724;}
.voice{position:fixed;right:22px;bottom:24px;width:78px;height:78px;border-radius:28px;background:#201b17;color:white;display:flex;align-items:center;justify-content:center;font-size:38px;z-index:999;box-shadow:0 16px 38px rgba(0,0,0,.25);}
.small{color:#746c64;font-size:14px;}
@media(max-width:640px){.block-container{padding-left:18px!important;padding-right:18px!important}.hero{padding:24px 22px}.hero h1{font-size:32px}.kpis{grid-template-columns:repeat(2,1fr)}.card{padding:21px 20px}.voice{right:18px;bottom:20px;width:72px;height:72px}}
</style>
<div class="voice">🎙️</div>
""", unsafe_allow_html=True)

MODULES = ["Centro de Operaciones", "Semillero", "Tareas", "Radar", "Estudio", "Calendario", "Relaciones", "Libros y relatos", "Ideas para la app", "Ajustes"]
page = st.selectbox("☰ Menú", MODULES, label_visibility="collapsed")


def hero(title, subtitle=""):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def kpis():
    semillas = len(st.session_state.get("semillero_items", []))
    tareas_count = len(st.session_state.get("tareas", []))
    oportunidades = 4
    eventos = 2
    st.markdown(f"""
    <div class="kpis">
      <div class="kpi"><b>{tareas_count}</b><span>Tareas</span></div>
      <div class="kpi"><b>{semillas}</b><span>Semillas</span></div>
      <div class="kpi"><b>{oportunidades}</b><span>Oportunidades</span></div>
      <div class="kpi"><b>{eventos}</b><span>Eventos</span></div>
    </div>
    """, unsafe_allow_html=True)


def card(title, body):
    st.markdown(f'<div class="card"><h2>{title}</h2>{body}</div>', unsafe_allow_html=True)


def centro():
    hero("Centro de Operaciones", "Buenos días, Irene · Aquí está lo que necesita tu atención.")
    kpis()
    card("🎯 Prioridad del día", "<ul><li>Preparar base de contactos.</li><li>Crear banco de contenidos.</li><li>Revisar agenda cultural.</li></ul>")
    card("🔥 Radar rápido", '<p>4 oportunidades detectadas para revisar esta semana.</p><span class="badge">Madrid</span><span class="badge">Librerías</span><span class="badge">Concursos</span>')
    card("📚 Libro activo", "<p><strong>El libro mágico de Hugo e Inés</strong><br>Fase: preparación de publicación.</p>")
    card("🎙️ Última nota de voz", "<p>Idea para vídeo: ¿sabías que...? sobre libros antiguos.</p><p class='small'>Estado: por organizar</p>")


def semillero():
    hero("🌱 Semillero", "Notas, ideas y capturas pendientes de organizar.")
    tipo = st.selectbox("Tipo", ["Nota de voz", "Idea", "Contacto", "Evento", "Noticia", "Concurso", "Relato terminado"])
    texto = st.text_area("Contenido", placeholder="Guarda aquí algo que todavía no sabes dónde colocar...")
    if st.button("Guardar en Semillero") and texto.strip():
        st.session_state.semillero_items.append({"tipo": tipo, "texto": texto.strip(), "estado": "Por organizar"})
        st.success("Guardado en Semillero")
    st.subheader("Por organizar")
    for i, item in enumerate(st.session_state.get("semillero_items", [])):
        with st.container(border=True):
            st.markdown(f"**{item['tipo']}**")
            st.write(item["texto"])
            st.caption(item.get("estado", "Por organizar"))


def tareas():
    hero("✅ Tareas", "Lo que hay que hacer, sin perder el foco.")
    nueva = st.text_input("Nueva tarea")
    if st.button("Añadir tarea") and nueva.strip():
        st.session_state.tareas.append(nueva.strip())
        st.success("Tarea añadida")
    st.subheader("🔥 Hoy")
    for idx, t in enumerate(list(st.session_state.get("tareas", []))):
        st.checkbox(t, key=f"task_{idx}")
    card("📅 Esta semana", "<p>Preparar base de contactos · Crear banco de contenidos · Revisar agenda cultural.</p>")


def radar():
    hero("🧭 Radar", "Oportunidades, eventos, concursos y señales útiles.")
    tabs = st.tabs(["⭐ Recomendado", "🎤 Eventos", "🏆 Concursos", "📰 Noticias"])
    with tabs[0]:
        for txt in ["Presentación en FNAC Callao · Madrid", "Concurso de relato histórico · cierra en 16 días", "Buscar eventos de librerías en Getafe/Leganés"]:
            with st.container(border=True):
                st.subheader("Oportunidad")
                st.write(txt)
                st.button("Revisar", key=txt)
    with tabs[1]:
        st.write("Eventos literarios pendientes de conectar.")
    with tabs[2]:
        st.write("Concursos pendientes de conectar.")
    with tabs[3]:
        st.write("Noticias pendientes de conectar.")


def simple_page(title, subtitle, body):
    hero(title, subtitle)
    card("Estado", body)

if page == "Centro de Operaciones":
    centro()
elif page == "Semillero":
    semillero()
elif page == "Tareas":
    tareas()
elif page == "Radar":
    radar()
elif page == "Estudio":
    simple_page("🎬 Estudio", "Banco de contenidos y producción.", "<p>Ideas · Guiones · Grabar · Editar · Programar · Publicado.</p>")
elif page == "Calendario":
    simple_page("📅 Calendario", "Fechas importantes y próximos hitos.", "<p>Vista mensual pendiente. Aquí irán eventos, tareas y campañas.</p>")
elif page == "Relaciones":
    simple_page("🤝 Relaciones", "Contactos de autora.", "<p>Librerías · Editoriales · Bibliotecas · Autores · Prensa.</p>")
elif page == "Libros y relatos":
    simple_page("📚 Libros y relatos", "Todo lo terminado, publicado o no.", "<p>Libros, cuentos, relatos terminados, concursos y campañas.</p>")
elif page == "Ideas para la app":
    hero("💡 Ideas para la app", "Mejoras que se te ocurran mientras la usas.")
    idea = st.text_input("Nueva idea")
    if st.button("Guardar idea") and idea.strip():
        st.session_state.ideas_app.append(idea.strip())
        st.success("Idea guardada")
    for idea in st.session_state.get("ideas_app", []):
        st.write("• " + idea)
else:
    simple_page("⚙️ Ajustes", "Configuración y futuras conexiones.", "<p>Drive, copias, privacidad y preferencias.</p>")
