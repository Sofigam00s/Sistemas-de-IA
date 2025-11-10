"""
APLICACIÓN WEB STREAMLIT
Interfaz gráfica interactiva para el sistema de análisis de personalidad MBTI.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from agente import AgentePersonalidad
from razonamiento import SistemaRazonamiento, TIPOS_MBTI

# Configuración general
st.set_page_config(
    page_title="Test MBTI con IA",
    page_icon="🧠",
    layout="wide"
)

# Estilos CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 10px;
        font-weight: bold;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Preguntas del test (60 ítems)
# -------------------------------------------------------------
PREGUNTAS = [
    "Te sientes cómodo acercándote a alguien que te parece interesante y entablar una conversación",
    "Rara vez te preocupas por cómo tus acciones afectan a otras personas",
    "A menudo te sumerges tanto en lo que estás haciendo que pierdes la noción del tiempo",
    "Te molesta cuando las cosas están desordenadas o asimétricas",
    "Prefieres hacer tus planes con mucha anticipación",
    "Te resulta fácil mantenerte relajado y concentrado incluso cuando hay mucha presión",
    "A menudo te quedas despierto hasta tarde soñando despierto sobre cosas que podrían suceder",
    "Rara vez te sientes inseguro",
    "Tiendes a sentir mucha simpatía por otras personas",
    "Completas las cosas metódicamente sin saltarte nada",
    "En las reuniones sociales, rara vez intentas presentar personas nuevas",
    "Los debates filosóficos te interesan mucho",
    "Prefieres no llamar demasiado la atención",
    "Te resulta difícil empatizar con los sentimientos de otras personas",
    "Tiendes a posponer las decisiones durante el mayor tiempo posible",
    "Rara vez dudas de ti mismo",
    "Sientes que el mundo sería un lugar mejor si la gente se basara más en la racionalidad y menos en sus sentimientos",
    "Prefieres hacer las cosas a tu propio ritmo sin preocuparte demasiado por los plazos",
    "No te importa estar en el centro de atención",
    "Tienes una tendencia a pensar demasiado en las situaciones",
    "Tu área de trabajo suele estar ordenada y organizada",
    "Consideras que expresar afecto es algo que no te resulta natural",
    "Tiendes a preocuparte por cosas que podrían salir mal",
    "Crees firmemente en 'haz lo correcto' en lugar de 'lo que funciona'",
    "Te resulta difícil concentrarte a menos que hayas terminado todas tus tareas",
    "A menudo te sientes abrumado por las emociones de otras personas",
    "Completas las cosas de manera eficiente",
    "A menudo te encuentras perdido en tus pensamientos cuando caminas en la naturaleza",
    "Si alguien no responde a tus mensajes rápidamente, comienzas a preocuparte de haber dicho algo incorrecto",
    "Como regla general, tu lugar de trabajo actual es más funcional que decorativo",
    "Siempre te aseguras de tener un plan de respaldo",
    "Disfrutas reflexionar sobre la naturaleza de la existencia",
    "Tus emociones a menudo cambian rápidamente",
    "Te resulta fácil simpatizar con las personas cuyos experiencias son muy diferentes a las tuyas",
    "Por lo general, pierdes interés cuando se discuten teorías muy abstractas o impracticables",
    "Te resulta más satisfactorio mejorar algo familiar que crear algo desde cero",
    "Sientes que tus habilidades sociales son tu mayor fortaleza",
    "Te sientes muy ansioso en situaciones estresantes",
    "Estás dispuesto a asumir riesgos sociales o financieros si el potencial de recompensa es suficientemente alto",
    "Tu espacio de trabajo está lleno de diversos recuerdos, fotos u objetos personales",
    "Tiendes a postergar las tareas hasta el último momento posible",
    "Rara vez permites que tus impulsos te guíen",
    "A menudo te cuestionas la forma en que otras personas hacen las cosas",
    "Evitas tomar decisiones que se basan principalmente en sentimientos subjetivos",
    "A ti te gusta tener un horario claro para tu día",
    "Eres el tipo de persona que piensa 'no hay gente extraña, solo amigos que aún no has conocido'",
    "Rara vez te preocupas por cómo los demás perciben tus acciones",
    "Piensas que el mundo sería un lugar mejor si las personas fueran más compasivas y menos racionales",
    "Preferirías improvisar que seguir un plan cuidadoso",
    "Consideras que ser consistente es más importante que ser mente abierta",
    "Disfrutas discutiendo cuestiones éticas",
    "Te resulta fácil concentrarte en una tarea durante largos períodos",
    "A menudo te sientes atraído por actividades artísticas o creativas",
    "Tu felicidad depende más de los demás que de ti mismo",
    "Estás interesado en tantas cosas que te resulta difícil elegir qué probar a continuación",
    "Eres propenso a preocuparte de que las cosas podrían salir mal",
    "Evitas liderazgo o roles públicos",
    "Definitivamente no eres una persona artística",
    "Rara vez te preocupas por lo que otros piensen de ti",
    "Sabes a primera vista si alguien es una buena persona o no"
]


# Inicializar el estado
def inicializar_estado():
    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = [0] * 60
    if 'pagina' not in st.session_state:
        st.session_state.pagina = 0
    if 'resultado' not in st.session_state:
        st.session_state.resultado = None
    if 'agente' not in st.session_state:
        st.session_state.agente = AgentePersonalidad()

# Página: Test MBTI
def pagina_test():
    st.title("🧠 Test de Personalidad MBTI con Inteligencia Artificial")

    progreso = (st.session_state.pagina + 1) / len(PREGUNTAS)
    st.progress(progreso)
    st.write(f"Pregunta {st.session_state.pagina + 1} de {len(PREGUNTAS)}")

    pregunta_idx = st.session_state.pagina
    st.markdown(f"### {PREGUNTAS[pregunta_idx]}")

    respuesta = st.select_slider(
        "Tu respuesta:",
        options=[-3, -2, -1, 0, 1, 2, 3],
        value=st.session_state.respuestas[pregunta_idx],
        key=f"pregunta_{pregunta_idx}"
    )
    st.session_state.respuestas[pregunta_idx] = respuesta

    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.session_state.pagina > 0 and st.button("⬅️ Anterior"):
            st.session_state.pagina -= 1
            st.rerun()
    with col_next:
        if st.session_state.pagina < len(PREGUNTAS) - 1:
            if st.button("Siguiente ➡️"):
                st.session_state.pagina += 1
                st.rerun()
        else:
            if st.button("🎯 Analizar Resultado", type="primary"):
                with st.spinner("Analizando tu personalidad..."):
                    tipo_objetivo = st.session_state.get('tipo_objetivo', None)
                    resultado = st.session_state.agente.analizar_completo(
                        st.session_state.respuestas,
                        tipo_objetivo
                    )
                    st.session_state.resultado = resultado
                st.success("¡Análisis completado!")
                st.rerun()

# Página: Resultado
def pagina_resultado():
    if st.session_state.resultado is None:
        st.warning("Por favor completa el test primero.")
        return

    resultado = st.session_state.resultado
    st.title("🎯 Tu Resultado MBTI")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tu Tipo de Personalidad", resultado["tipo_predicho"])
    with col2:
        st.metric("Nivel de Confianza", resultado["confianza"])

    st.markdown("### 🧩 Análisis de Rasgos")
    for rasgo in resultado["razonamiento"]:
        st.write(f"✓ {rasgo}")

    tipo = resultado["tipo_predicho"]
    fig = go.Figure(data=[go.Bar(
        x=['Energía', 'Información', 'Decisiones', 'Estilo'],
        y=[1, 1, 1, 1],
        text=[tipo[0], tipo[1], tipo[2], tipo[3]],
        textposition='inside',
        marker_color=['#667eea', '#764ba2', '#667eea', '#764ba2']
    )])
    fig.update_layout(height=300, title="Componentes de tu personalidad MBTI", yaxis_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    if "planificacion" in resultado:
        plan = resultado["planificacion"]
        st.markdown("### 🗺️ Camino hacia tu Objetivo")
        st.write(" → ".join(plan["camino"]))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Repetir Test"):
            st.session_state.respuestas = [0] * 60
            st.session_state.pagina = 0
            st.session_state.resultado = None
            st.rerun()
    with col2:
        import json
        st.download_button(
            "📥 Descargar Resultado",
            data=json.dumps(resultado, indent=2, ensure_ascii=False),
            file_name="resultado_mbti.json",
            mime="application/json"
        )

# Navegación
def main():
    inicializar_estado()

    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/brain.png", width=100)
        opcion = st.radio(
            "Selecciona una sección:",
            ["🧪 Realizar Test", "📊 Ver Resultado"]
        )
        st.markdown("---")
        if st.checkbox("Establecer tipo objetivo"):
            tipo_obj = st.selectbox("Tipo MBTI objetivo", [""] + TIPOS_MBTI)
            st.session_state.tipo_objetivo = tipo_obj if tipo_obj else None

    if opcion == "🧪 Realizar Test":
        pagina_test()
    elif opcion == "📊 Ver Resultado":
        pagina_resultado()

if __name__ == "__main__":
    main()

