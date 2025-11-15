import streamlit as st
import sys
import os

# --------------------------------------------
# Agregar al path la carpeta "machinelearni"
# --------------------------------------------
sys.path.append(os.path.abspath("../MACHINE_LEARNING"))

# Importar tu modelo y función de predicción
from data_set import predecir, obtener_equipos

# --------------------------------------------
# Interfaz
# --------------------------------------------
st.title("📊 Predicción de Partidos - Liga Argentina")
st.write("Modelo cargado desde machinelearni/data_set.py")

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
