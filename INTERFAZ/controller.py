import streamlit as st
import random

# Configuración de la página
st.set_page_config(
    page_title="Predictor de Fútbol",
    page_icon="⚽",
    layout="centered"
)

# Título principal
st.title("⚽ Predictor de Partidos de Fútbol")
st.markdown("---")

# Descripción
st.write(
    "Ingresa los nombres de dos equipos y descubre cuál tiene "
    "mayor probabilidad de ganar"
)

# Espaciado
st.write("")

# Crear dos columnas para los inputs
col1, col2 = st.columns(2)

with col1:
    equipo1 = st.text_input(
        "🏟️ Equipo Local",
        placeholder="Ej: Barcelona",
        key="equipo1"
    )

with col2:
    equipo2 = st.text_input(
        "🏟️ Equipo Visitante",
        placeholder="Ej: Real Madrid",
        key="equipo2"
    )

# Botón de análisis
st.write("")
if st.button("🔍 Analizar Partido", type="primary", use_container_width=True):
    if equipo1 and equipo2:
        # Simulación de análisis (por ahora aleatorio)
        st.markdown("---")
        st.subheader("📊 Resultados del Análisis")
        
        # Generar probabilidades aleatorias
        prob_equipo1 = random.randint(30, 70)
        prob_empate = random.randint(10, 30)
        prob_equipo2 = 100 - prob_equipo1 - prob_empate
        
        # Mostrar probabilidades en columnas
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric(
                label=f"Victoria {equipo1}",
                value=f"{prob_equipo1}%"
            )
        
        with col_b:
            st.metric(
                label="Empate",
                value=f"{prob_empate}%"
            )
        
        with col_c:
            st.metric(
                label=f"Victoria {equipo2}",
                value=f"{prob_equipo2}%"
            )
        
        # Determinar el ganador más probable
        st.write("")
        if prob_equipo1 > prob_equipo2 and prob_equipo1 > prob_empate:
            st.success(
                f"🏆 **{equipo1}** tiene mayor probabilidad de ganar"
            )
        elif prob_equipo2 > prob_equipo1 and prob_equipo2 > prob_empate:
            st.success(
                f"🏆 **{equipo2}** tiene mayor probabilidad de ganar"
            )
        else:
            st.info("⚖️ El partido está muy parejo, alta probabilidad de empate")
        
        # Barra de progreso visual
        st.write("")
        st.progress(prob_equipo1 / 100)
        st.caption(f"Probabilidad de victoria para {equipo1}")
        
    else:
        st.warning("⚠️ Por favor, ingresa el nombre de ambos equipos")

# Footer
st.markdown("---")
st.caption("💡 Nota: Los datos mostrados son simulados. "
           "Próximamente se integrarán estadísticas reales.")

