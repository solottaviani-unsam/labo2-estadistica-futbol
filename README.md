# labo2-estadistica-futbol

Para ejecutar la interfaz gráfica del proyecto, utiliza el siguiente comando en la terminal:

```
streamlit run interface/controller.py
```

# Predicción de Resultados de Fútbol con Machine Learning
## 📌 Descripción del Proyecto

Este proyecto consiste en la creación de un sistema de predicción de resultados de fútbol utilizando datos reales de partidos.
A partir de múltiples archivos JSON obtenidos mediante requests a una API, el sistema procesa estadísticas históricas de los equipos y entrena un modelo de Machine Learning capaz de predecir el resultado más probable de un partido entre dos equipos seleccionados.

El proyecto incluye:

- Procesamiento y normalización de datos desde archivos JSON.

- Construcción de un dataset unificado con estadísticas relevantes.

- Entrenamiento de un modelo de Machine Learning.

- Interfaz web (Streamlit) para consultar predicciones.

## 📂 Datos utilizados

Los datos provienen de los siguientes archivos JSON:

- fixture_completo.json → Contiene todos los partidos jugados, equipos, goles y resultados.

- fixture_25.json → Estadísticas del torneo (rendimientos globales).

- goles_local_visitante.json → Goles de cada equipo como local y visitante.

- tabla_posiciones_fase_2.json → Posiciones, puntos, goles a favor y en contra.

A partir de estos datos se armaron variables predictoras como:

- Posición en la tabla del equipo local y visitante

- Puntos acumulados

- Goles a favor y en contra

- Rendimiento ofensivo/defensivo como local y visitante

- Resultado real del partido (variable objetivo)

## 🧪 Objetivo del Modelo

El modelo debe predecir el resultado de un partido entre:

2 → Gana el equipo local

1 → Empate

0 → Gana el visitante

Es decir, se trata de un problema de clasificación multiclase.

## 🤖 Tipo de Machine Learning utilizado
### ✔️ Regresión Logística Multinomial

Se eligió este modelo porque:

- Es uno de los algoritmos más utilizados para tareas de clasificación multiclase.

- Es fácil de entrenar, interpretar y explicar.

- No requiere una enorme cantidad de datos, por lo que se adapta bien al dataset disponible.

- Es un modelo lineal, lo que evita sobreajustes y genera predicciones estables.

- Cumple con los requerimientos del curso: usar un modelo de Machine Learning entrenado con datos reales.

**La regresión logística funciona extendiendo la idea de un modelo lineal, pero en lugar de predecir valores numéricos continuos, estima probabilidades para cada clase y selecciona la más probable.**

## ⚙️ Entrenamiento del Modelo

1. Se construyó un dataset tomando cada partido del fixture_completo.json como una fila.

2. Para cada partido se agregaron estadísticas del equipo local y visitante.

3. Se definió la variable objetivo (resultado) con valores 0, 1 y 2.

4. Se dividió el dataset en entrenamiento y prueba.

5. Se entrenó el modelo con:

```
model = LogisticRegression(
    multi_class="multinomial",
    solver="lbfgs",
    max_iter=500
)
```

6. Se evaluó el modelo con classification_report para obtener precisión, recall y f1-score.

## 🖥️ Interfaz para el Usuario (Streamlit)

El proyecto incluye una pequeña app donde el usuario puede:

1. Seleccionar un equipo local

2. Seleccionar un equipo visitante

3. Consultar la predicción del modelo

La app muestra:

- Probabilidad de victoria local

- Probabilidad de empate

- Probabilidad de victoria visitante

## 🧠 ¿Por qué no usamos otros modelos?

Aunque probamos opciones como Random Forest o redes neuronales, la regresión logística fue elegida porque:
- Es simple y fácil de interpretar. 

- Evita sobreajustes en datasets pequeños.

- Los resultados fueron estables y suficientemente precisos.

- El objetivo del trabajo es aprender, interpretar y explicar el modelo.
