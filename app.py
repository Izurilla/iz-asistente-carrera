import streamlit as st
import pandas as pd
from datetime import date, datetime
from pathlib import Path
import json

st.set_page_config(page_title="IZ | Asistente de Carrera", page_icon="🧭", layout="centered")
DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)

def load_json(name, default):
    p = DATA / name
    if p.exists():
        try:
            return json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            return default
    p.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding='utf-8')
    return default

def save_json(name, data):
    (DATA / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

seed = {
 'tasks':[{'text':'Revisar calendario','done':False},{'text':'Añadir 3 ideas de contenido','done':False},{'text':'Mirar Radar Madrid','done':False}],
 'ideas':['¿Sabías que...? sobre libros antiguos','Vídeo: una foto, una historia','Post: por qué Irene Zurilla escribe'],
 'events':[{'title':'Presentación FNAC Callao','when':'Viernes 19:00','type':'Presentación','place':'Madrid'},{'title':'Concurso relato histórico','when':'Cierra en 16 días','type':'Concurso','place':'Online'}],
 'contacts':[{'name':'Librería Cervantes','note':'Revisar contacto','days':52},{'name':'Biblioteca Getafe','note':'Posible actividad infantil','days':0}],
 'notes':[]
}
state = load_json('iz_data.json', seed)

st.markdown('''<style>
.stApp{background:#f7f1e8;color:#27231f}.block-container{padding:1.2rem 1rem 6rem;max-width:760px}.card{background:rgba(255,255,255,.55);border:1px solid #e4d9ca;border-radius:28px;padding:22px;margin:14px 0;box-shadow:0 6px 20px rgba(80,55,20,.05)}.hero{background:linear-gradient(135deg,#fffaf1,#efe0cf);border-radius:32px;padding:24px;margin:12px 0 22px}.title{font-size:38px;font-weight:800;line-height:1.05}.muted{color:#776e65}.pill{display:inline-block;border:1px solid #e1d5c6;border-radius:999px;padding:8px 14px;background:#f6eadc}.mic{background:#211e19;color:white;text-align:center;border-radius:999px;padding:18px;font-size:20px;font-weight:800;margin:12px 0}.bottom{position:fixed;left:0;right:0;bottom:0;background:rgba(255,250,240,.96);border-top:1px solid #e2d8ca;padding:8px 10px;z-index:999}.bottom a{text-decoration:none;color:#5f574f;font-weight:700;margin:0 8px}.bigmic{display:inline-block;background:#43378f;color:white;border-radius:50%;width:76px;height:76px;line-height:76px;text-align:center;font-size:34px;box-shadow:0 0 0 18px rgba(67,55,143,.10)}
</style>''', unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page='Despacho'
if 'cuentame' not in st.session_state: st.session_state.cuentame=False

def nav_button(label):
    if st.button(label, use_container_width=True): st.session_state.page=label.split(' ',1)[1] if ' ' in label else label

st.markdown('### 🧭 IZ | Asistente de Carrera &nbsp;&nbsp; <span class="pill">V0.5</span>', unsafe_allow_html=True)

if st.session_state.cuentame:
    st.markdown('<div class="card"><div class="title">🎙 Cuéntame</div><p class="muted">Habla o escribe. En esta beta lo guardamos en Bandeja de entrada.</p>', unsafe_allow_html=True)
    cat=st.selectbox('Tipo', ['Idea','Contacto','Evento','Recordatorio','Noticia','Fecha','Nota libre'])
    txt=st.text_area('¿Qué quieres contarme?', placeholder='Ej: Acabo de salir de una presentación...')
    c1,c2=st.columns(2)
    if c1.button('🧭 Enviar al Asistente', use_container_width=True):
        if txt.strip():
            state['notes'].append({'date':datetime.now().isoformat(timespec='minutes'),'type':cat,'text':txt.strip()})
            if cat=='Idea': state['ideas'].insert(0, txt.strip())
            save_json('iz_data.json', state)
            st.success('Guardado y organizado.')
    if c2.button('Cerrar', use_container_width=True): st.session_state.cuentame=False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

page=st.session_state.page

def despacho():
    h=datetime.now().hour; saludo='Buenos días' if h<14 else 'Buenas tardes' if h<21 else 'Buenas noches'
    st.markdown(f'<div class="hero"><div class="title">{saludo}, Irene</div><p class="muted">Tu despacho de autora · {date.today().strftime("%d/%m/%Y")}</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>🧭 Brújula</h3><p>Hoy revisaría <b>calendario + noticias</b> y dejaría una nota de voz con ideas para septiembre.</p></div>', unsafe_allow_html=True)
    if st.button('🎙 Contárselo al Director', use_container_width=True): st.session_state.cuentame=True; st.rerun()
    st.markdown('<div class="card"><h3>🎯 Prioridades</h3>', unsafe_allow_html=True)
    for i,t in enumerate(state['tasks'][:3]):
        done=st.checkbox(t['text'], value=t['done'], key=f'top{i}')
        state['tasks'][i]['done']=done
    save_json('iz_data.json', state)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>🔥 Oportunidad destacada</h3><b>Presentación FNAC Callao</b><br><span class="muted">Viernes · 19:00 · Madrid</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>⏳ Próximo hito</h3><b>Publicación del libro</b><br><span style="font-size:36px;font-weight:800">143</span> días</div>', unsafe_allow_html=True)

def jornada():
    st.markdown('<div class="hero"><div class="title">📅 Jornada</div><p class="muted">Hoy, mañana y esta semana.</p></div>', unsafe_allow_html=True)
    new=st.text_input('Nueva tarea')
    if st.button('Añadir tarea') and new.strip():
        state['tasks'].append({'text':new.strip(),'done':False}); save_json('iz_data.json', state); st.rerun()
    for i,t in enumerate(state['tasks']):
        state['tasks'][i]['done']=st.checkbox(t['text'], value=t['done'], key=f'task{i}')
    save_json('iz_data.json', state)

def radar():
    st.markdown('<div class="hero"><div class="title">🧭 Radar</div><p class="muted">Eventos, noticias y oportunidades.</p></div>', unsafe_allow_html=True)
    tabs=st.tabs(['Madrid','Noticias','Concursos','Favoritos'])
    with tabs[0]:
        for e in state['events']:
            st.markdown(f'<div class="card"><b>{e["title"]}</b><br><span class="muted">{e["when"]} · {e["place"]}</span></div>', unsafe_allow_html=True)
    with tabs[1]:
        st.info('Noticias reales se conectarán en la siguiente fase. Aquí aparecerán libros, historia, editoriales y cultura.')
    with tabs[2]: st.write('Concursos guardados y plazos.')
    with tabs[3]: st.write('FNAC, Casa del Libro, librerías, bibliotecas y espacios favoritos.')

def estudio():
    st.markdown('<div class="hero"><div class="title">🎬 Estudio Editorial</div><p class="muted">Banco de contenidos y producción.</p></div>', unsafe_allow_html=True)
    idea=st.text_input('Nueva idea')
    if st.button('Guardar idea') and idea.strip():
        state['ideas'].insert(0, idea.strip()); save_json('iz_data.json', state); st.rerun()
    st.markdown('<div class="card"><h3>💡 Ideas</h3>', unsafe_allow_html=True)
    for x in state['ideas']: st.write('💡', x)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><b>🎙 Grabar</b><br>Curiosidad: primer bestseller<br>Vídeo: por qué me gusta la historia</div>', unsafe_allow_html=True)

def calendario():
    st.markdown('<div class="hero"><div class="title">🗓 Calendario</div><p class="muted">Fechas clave y próximos hitos.</p></div>', unsafe_allow_html=True)
    for x in ['Viernes: Radar del fin de semana','Domingo tarde: Reunión de Dirección','23 abril: Día del Libro','Diciembre: campaña de lanzamiento']:
        st.markdown(f'<div class="card">{x}</div>', unsafe_allow_html=True)

def mas():
    st.markdown('<div class="hero"><div class="title">☰ Más</div><p class="muted">Relaciones, libros, marca y dirección.</p></div>', unsafe_allow_html=True)
    for name in ['🤝 Relaciones','📚 Libros','🛡 Marca','📈 Dirección','📥 Bandeja de entrada']:
        if st.button(name, use_container_width=True): st.session_state.page=name.split(' ',1)[1]; st.rerun()

def relaciones():
    st.markdown('<div class="hero"><div class="title">🤝 Relaciones</div></div>', unsafe_allow_html=True)
    for c in state['contacts']: st.markdown(f'<div class="card"><b>{c["name"]}</b><br><span class="muted">{c["note"]} · hace {c["days"]} días</span></div>', unsafe_allow_html=True)

def libros():
    st.markdown('<div class="hero"><div class="title">📚 Libros</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>El libro mágico de Hugo e Inés</h3><p>Estado: preparando campaña · Editorial: pendiente · Próximo paso: materiales de autora.</p></div>', unsafe_allow_html=True)

def bandeja():
    st.markdown('<div class="hero"><div class="title">📥 Bandeja</div><p class="muted">Todo lo que le cuentas al Director.</p></div>', unsafe_allow_html=True)
    for n in reversed(state['notes']): st.markdown(f'<div class="card"><b>{n["type"]}</b><br>{n["text"]}<br><span class="muted">{n["date"]}</span></div>', unsafe_allow_html=True)

pages={'Despacho':despacho,'Jornada':jornada,'Radar':radar,'Estudio':estudio,'Calendario':calendario,'Más':mas,'Relaciones':relaciones,'Libros':libros,'Bandeja de entrada':bandeja,'Marca':lambda: st.write('🛡 Marca en construcción'),'Dirección':lambda: st.write('📈 Dirección en construcción')}
pages.get(page, despacho)()

st.markdown('<div style="height:90px"></div>', unsafe_allow_html=True)
st.markdown('<div class="bottom"><div style="display:flex;align-items:center;justify-content:space-around"><a href="#" onclick="return false;">🏠</a><a href="#" onclick="return false;">📅</a><span class="bigmic">🎙</span><a href="#" onclick="return false;">🧭</a><a href="#" onclick="return false;">☰</a></div></div>', unsafe_allow_html=True)
cols=st.columns(5)
for label,col in zip(['Despacho','Jornada','Cuéntame','Radar','Más'], cols):
    if col.button(label, use_container_width=True):
        if label=='Cuéntame': st.session_state.cuentame=True
        else: st.session_state.page=label
        st.rerun()
