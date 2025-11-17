import streamlit as st

# Importo las funciones del modelo
from machine_learning.data_set import predecir, obtener_equipos
from machine_learning.data_set import get_team_features, get_goles_features


st.title("📊 Predicción de Partidos - Liga Argentina")
st.write("proyecto laboratorio 2")

#obtengo todos los equipos que estaban en el dataset de machine learning
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

        # Generar razones simples para mostrar
        f_loc = {**get_team_features(local), **get_goles_features(local)}
        f_vis = {**get_team_features(visitante), **get_goles_features(visitante)}

        with st.expander("📌 ¿Por qué se predijo ese resultado?"):
            st.write(f"📌 {local}: posición {f_loc['posicion']}, puntos {f_loc['puntos']}, GF {f_loc['gf']}, GC {f_loc['gc']}")
            st.write(f"📌 {visitante}: posición {f_vis['posicion']}, puntos {f_vis['puntos']}, GF {f_vis['gf']}, GC {f_vis['gc']}")
            st.write(f"📊 Goles como local: {f_loc['gf_local']} / visitante: {f_vis['gf_vis']}")
            st.write(f"🛡️ Goles recibidos local: {f_loc['gc_local']} / visitante: {f_vis['gc_vis']}")

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
