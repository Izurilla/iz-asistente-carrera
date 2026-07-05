import streamlit as st
from datetime import date, datetime, timedelta

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")

# ---------- CSS ----------
st.markdown("""
<style>
:root{--bg:#f7f1e8;--card:#fffaf2;--ink:#24211d;--muted:#766f67;--accent:#29231d;--line:#e6d9c9;--soft:#eee3d5;}
.stApp{background:linear-gradient(180deg,#faf6ee 0%,#f2e8dc 100%); color:var(--ink);}
.block-container{padding:1.2rem 1rem 6rem; max-width:720px;}
h1,h2,h3{font-family:Georgia, 'Times New Roman', serif; color:var(--ink);}
.small{color:var(--muted); font-size:.95rem; margin-top:-.5rem;}
.card{background:rgba(255,250,242,.92); border:1px solid var(--line); border-radius:26px; padding:20px; margin:14px 0; box-shadow:0 10px 30px rgba(56,42,20,.06);}
.hero{background:linear-gradient(135deg,#fffaf2,#eadbc9); border:1px solid var(--line); border-radius:34px; padding:24px; margin:12px 0 18px;}
.pill{display:inline-block; padding:8px 14px; border-radius:999px; background:#efe4d7; color:#5c5148; font-weight:700; font-size:.9rem;}
.mic{position:fixed; left:50%; transform:translateX(-50%); bottom:20px; width:88px; height:88px; border-radius:34px; background:#1f1b16; color:white; display:flex; align-items:center; justify-content:center; font-size:42px; box-shadow:0 18px 45px rgba(31,27,22,.35); z-index:9999; border:8px solid rgba(255,250,242,.9);}
.navhint{position:fixed; left:0; right:0; bottom:0; background:rgba(255,250,242,.96); border-top:1px solid var(--line); height:76px; z-index:9998;}
button[kind="secondary"]{border-radius:18px!important;}
.stButton>button{border-radius:20px; min-height:44px; font-weight:700;}
.metric-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.metric{background:#fffaf2;border:1px dashed var(--line);border-radius:22px;padding:14px;}
</style>
""", unsafe_allow_html=True)

# ---------- State ----------
if "page" not in st.session_state: st.session_state.page = "Despacho"
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"txt":"Revisar calendario + noticias", "done":False, "tag":"Hoy"},
        {"txt":"Dejar una nota de voz para ideas de septiembre", "done":False, "tag":"Hoy"},
        {"txt":"Preparar 3 ideas de vídeo", "done":False, "tag":"Semana"},
    ]
if "ideas" not in st.session_state:
    st.session_state.ideas = ["¿Sabías que...? sobre libros antiguos", "Vídeo: una foto, una historia", "Post: por qué Irene Zurilla escribe"]
if "opps" not in st.session_state:
    st.session_state.opps = ["Presentación en FNAC Callao · Madrid", "Concurso de relato histórico · cierra en 16 días", "Buscar eventos de librerías en Getafe/Leganés"]
if "contacts" not in st.session_state:
    st.session_state.contacts = ["Librería Cervantes · revisar en 30 días", "Biblioteca Getafe · primer contacto pendiente", "Editorial · consultar presentaciones"]
if "inbox" not in st.session_state: st.session_state.inbox = []

PAGES = ["Despacho","Jornada","Radar","Estudio","Calendario","Noticias","Relaciones","Libros","Marca","Dirección","Drive"]

def nav_buttons():
    cols = st.columns(5)
    items = [("🏠","Despacho"),("📅","Jornada"),("🧭","Radar"),("🎬","Estudio"),("☰","Más")]
    for col,(ico,name) in zip(cols,items):
        with col:
            if st.button(f"{ico}\n{name}", use_container_width=True):
                st.session_state.page = "Más" if name=="Más" else name
                st.rerun()

def mic_button():
    st.markdown('<div class="navhint"></div><div class="mic">🎙️</div>', unsafe_allow_html=True)
    if st.button("🎙️ Cuéntamelo al Director", use_container_width=True, type="primary"):
        st.session_state.page = "Cuéntame"
        st.rerun()

def card(title, body=""):
    st.markdown(f"<div class='card'><h3>{title}</h3><div>{body}</div></div>", unsafe_allow_html=True)

# ---------- Pages ----------
def page_despacho():
    hour = datetime.now().hour
    saludo = "Buenos días" if hour < 14 else "Buenas tardes" if hour < 21 else "Buenas noches"
    st.markdown(f"<div class='hero'><h1>{saludo}, Irene</h1><p class='small'>Tu despacho de autora · V0.7 clean</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>🧭 Brújula</h3><p>Hoy revisaría <b>calendario + noticias</b> y dejaría una nota de voz con cualquier idea para septiembre.</p></div>", unsafe_allow_html=True)
    st.subheader("🎯 Prioridades")
    for i,t in enumerate(st.session_state.tasks[:3]):
        st.checkbox(t["txt"], value=t["done"], key=f"taskhome{i}")
    st.subheader("🔥 Oportunidades")
    for o in st.session_state.opps[:3]: st.write("•", o)
    st.subheader("☕ Consejo del Director")
    st.info("No intentes hacerlo todo hoy. Primero deja funcionando el sistema y luego construimos el plan de carrera.")

def page_jornada():
    st.markdown("<div class='hero'><h1>📅 Jornada</h1><p class='small'>Hoy · Mañana · Esta semana</p></div>", unsafe_allow_html=True)
    new = st.text_input("Nueva tarea")
    if st.button("+ Añadir tarea") and new:
        st.session_state.tasks.append({"txt":new,"done":False,"tag":"Hoy"}); st.rerun()
    for i,t in enumerate(st.session_state.tasks):
        col1,col2 = st.columns([.15,.85])
        with col1: t["done"] = st.checkbox("", value=t["done"], key=f"t{i}")
        with col2: st.write(f"**{t['txt']}**  · {t['tag']}")

def page_cuentame():
    st.markdown("<div class='hero'><h1>🎙️ Cuéntame</h1><p class='small'>Habla o escribe. En esta beta lo organizamos por categoría.</p></div>", unsafe_allow_html=True)
    cat = st.radio("Tipo", ["💡 Idea","🤝 Contacto","🎤 Evento","📅 Recordatorio","📰 Noticia","🗓 Fecha"], horizontal=True)
    text = st.text_area("¿Qué quieres contarme?", placeholder="Ej: Acabo de salir de una presentación. He conocido a Ana, librera en Getafe...")
    audio = st.audio_input("O graba una nota de voz")
    if st.button("🧭 Enviar al Asistente", type="primary", use_container_width=True):
        st.session_state.inbox.append({"cat":cat,"text": text or "Nota de voz pendiente de transcripción", "date":str(date.today())})
        st.success("Guardado en la bandeja del Director.")
    st.subheader("Bandeja del Director")
    for item in reversed(st.session_state.inbox[-5:]):
        st.write(f"{item['cat']} · {item['date']} — {item['text']}")

def page_radar():
    st.markdown("<div class='hero'><h1>🧭 Radar</h1><p class='small'>Oportunidades, eventos, concursos y Madrid literario</p></div>", unsafe_allow_html=True)
    tabs = st.tabs(["⭐ Recomendadas","🎤 Presentaciones","🏆 Concursos","📚 Librerías","🏛 Historia"])
    for tab in tabs:
        with tab:
            for o in st.session_state.opps: st.write("•", o)
            new = st.text_input("Añadir oportunidad", key=str(tab))
            if st.button("Guardar", key="save"+str(tab)) and new:
                st.session_state.opps.append(new); st.rerun()

def page_estudio():
    st.markdown("<div class='hero'><h1>🎬 Estudio Editorial</h1><p class='small'>Banco de contenidos y producción</p></div>", unsafe_allow_html=True)
    st.metric("Ideas", len(st.session_state.ideas))
    for idea in st.session_state.ideas: st.write("💡", idea)
    new = st.text_input("Nueva idea de contenido")
    if st.button("+ Nueva idea") and new:
        st.session_state.ideas.append(new); st.rerun()
    st.markdown("<div class='metric-row'><div class='metric'><b>🎙️ Grabar</b><br>2 piezas</div><div class='metric'><b>🗓 Programado</b><br>1 post</div></div>", unsafe_allow_html=True)

def page_calendario():
    st.markdown("<div class='hero'><h1>🗓 Calendario</h1><p class='small'>Fechas clave y planificación</p></div>", unsafe_allow_html=True)
    today = date.today()
    events=[("📚 Día del Libro", date(today.year,4,23)),("🎄 Campaña Navidad", date(today.year,12,1)),("📖 Lanzamiento previsto", date(today.year,12,15)),("🎭 Radar fin de semana", today + timedelta(days=(4-today.weekday())%7))]
    for name,d in events:
        delta=(d-today).days
        st.write(f"**{name}** · {d.strftime('%d/%m/%Y')} · {'hoy' if delta==0 else str(delta)+' días'}")

def page_noticias():
    st.markdown("<div class='hero'><h1>📰 Noticias</h1><p class='small'>Radar editorial y cultural</p></div>", unsafe_allow_html=True)
    st.warning("En esta V0.7 las noticias son manuales. La búsqueda web automática llegará en la siguiente fase.")
    for n in ["Tendencias de lectura infantil", "Eventos literarios en Madrid", "Convocatorias para autores noveles"]: st.write("📰", n)

def page_relaciones():
    st.markdown("<div class='hero'><h1>🤝 Relaciones</h1><p class='small'>Contactos que cuidar</p></div>", unsafe_allow_html=True)
    new=st.text_input("Nuevo contacto")
    if st.button("+ Añadir contacto") and new:
        st.session_state.contacts.append(new); st.rerun()
    for c in st.session_state.contacts: st.write("•", c)

def page_libros():
    st.markdown("<div class='hero'><h1>📚 Libros</h1><p class='small'>Obras, campañas y presentaciones</p></div>", unsafe_allow_html=True)
    st.progress(.35)
    st.write("**Libro activo:** primer libro previsto para finales de año")
    st.write("**Próximo paso:** preparar plan de campaña y contactos base")

def page_mas():
    st.markdown("<div class='hero'><h1>☰ Más</h1><p class='small'>Módulos de dirección</p></div>", unsafe_allow_html=True)
    for p in ["Calendario","Noticias","Relaciones","Libros","Marca","Dirección","Drive"]:
        if st.button(p, use_container_width=True): st.session_state.page=p; st.rerun()

def page_simple(name, text):
    st.markdown(f"<div class='hero'><h1>{name}</h1><p class='small'>{text}</p></div>", unsafe_allow_html=True)

# ---------- Router ----------
st.markdown("<span class='pill'>🧭 IZ | Asistente de Carrera</span>", unsafe_allow_html=True)
page=st.session_state.page
if page=="Despacho": page_despacho()
elif page=="Jornada": page_jornada()
elif page=="Cuéntame": page_cuentame()
elif page=="Radar": page_radar()
elif page=="Estudio": page_estudio()
elif page=="Calendario": page_calendario()
elif page=="Noticias": page_noticias()
elif page=="Relaciones": page_relaciones()
elif page=="Libros": page_libros()
elif page=="Más": page_mas()
elif page=="Marca": page_simple("🛡 Marca", "Patrimonio de marca, registros, dominios y material oficial.")
elif page=="Dirección": page_simple("📈 Dirección", "Reuniones, prioridades y decisiones estratégicas.")
elif page=="Drive": page_simple("☁️ Drive", "Pendiente: conexión con Google Drive para datos vivos y documentos.")

mic_button()
nav_buttons()
