import streamlit as st
import sys
import os


sys.path.append(os.path.abspath("../MACHINE_LEARNING")) 

# Importo las funciones del modelo
from data_set import predecir, obtener_equipos



st.title("📊 Predicción de Partidos - Liga Argentina")
st.write("proyecto laboratorio 2")



equipos = obtener_equipos()

col1, col2 = st.columns(2)

with col1:
    local = st.selectbox("Equipo Local", equipos)

with col2:
    visitante = st.selectbox("Equipo Visitante", equipos)

if st.button("Predecir Resultado"):
    if local == visitante:
        st.error("Los equipos no pueden ser iguales.")
    else:
        resultado = predecir(local, visitante)
        st.success(resultado)

        
with st.expander("📌 ¿En qué se basa el modelo?"):
    st.write("""
    El modelo se entrenó utilizando datos históricos de la Liga Argentina.  
    A partir de estos datos se construyeron las siguientes **variables predictoras**:

    - **Posición en la tabla** del equipo local y visitante  
    - **Puntos acumulados** por cada equipo  
    - **Goles a favor y en contra**  
    - **Rendimiento ofensivo y defensivo** como local y visitante  
    - **Resultado real del partido** (variable objetivo que se buscó predecir)

    Estas variables permiten que el modelo aprenda patrones reales del desempeño de cada equipo
    y pueda estimar el resultado más probable de un nuevo enfrentamiento.
    """)