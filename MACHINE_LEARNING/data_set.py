import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# --------------------------
# 1. Cargar archivos JSON
# --------------------------
with open("/mnt/data/fixture_completo.json") as f:
    fixture = json.load(f)

with open("/mnt/data/goles_local_visitante.json") as f:
    goles = json.load(f)

with open("/mnt/data/tabla_posiciones_fase_2.json") as f:
    tabla = json.load(f)

tabla_df = pd.DataFrame(tabla)

# --------------------------
# 2. Funciones helpers
# --------------------------
def get_team_features(team_name):
    row = tabla_df[tabla_df["equipo"] == team_name]

    if row.empty:
        return {
            "posicion": 0, "puntos": 0,
            "gf": 0, "gc": 0
        }

    row = row.iloc[0]
    return {
        "posicion": row["posicion"],
        "puntos": int(row["puntos"]),
        "gf": row["goles_a_favor"],
        "gc": row["goles_en_contra"]
    }

def get_goles_features(team_name):
    if team_name not in goles:
        return {"gf_local":0, "gf_vis":0, "gc_local":0, "gc_vis":0}
    
    g = goles[team_name]
    return {
        "gf_local": g["goles_local"],
        "gf_vis": g["goles_visitante"],
        "gc_local": g["recibidos_local"],
        "gc_vis": g["recibidos_visitante"]
    }

# --------------------------
# 3. Construcción del dataset
# --------------------------
rows = []

for match in fixture:
    local = match["home"]["name"]
    visitante = match["away"]["name"]

    score = match["scores"]["ft_score"]  # "3 - 0"
    gl, gv = map(int, score.split("-"))

    # Resultado objetivo
    if gl > gv:
        resultado = 2   # gana local
    elif gl < gv:
        resultado = 0   # gana visitante
    else:
        resultado = 1   # empate

    # Features
    f_local_tabla = get_team_features(local)
    f_local_goles = get_goles_features(local)

    f_vis_tabla = get_team_features(visitante)
    f_vis_goles = get_goles_features(visitante)

    row = {
        "local": local,
        "visitante": visitante,
        "goles_local": gl,
        "goles_visita": gv,
        "resultado": resultado,
        **{f"loc_{k}": v for k, v in f_local_tabla.items()},
        **{f"loc_{k}": v for k, v in f_local_goles.items()},
        **{f"vis_{k}": v for k, v in f_vis_tabla.items()},
        **{f"vis_{k}": v for k, v in f_vis_goles.items()},
    }

    rows.append(row)

df = pd.DataFrame(rows)

# --------------------------
# 4. Entrenar modelo de REGRESIÓN LOGÍSTICA
# --------------------------
X = df.drop(columns=["resultado", "local", "visitante"])
y = df["resultado"]

X = X.fillna(0)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = LogisticRegression(
    multi_class="multinomial",
    solver="lbfgs",
    max_iter=500
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("✔️ Evaluación del modelo:")
print(classification_report(y_test, y_pred))

# ---------------------------
# 5. Prediccion de partidos
# ---------------------------
# Ejemplo de uso:
# print(predecir("Team A", "Team B")) --esta es la funcion que debemos utilziar en el controller (interfaz grafica)
def predecir(local, visitante):
    f_loc = {**get_team_features(local), **get_goles_features(local)}
    f_vis = {**get_team_features(visitante), **get_goles_features(visitante)}

    row = {**{f"loc_{k}": v for k, v in f_loc.items()},
           **{f"vis_{k}": v for k, v in f_vis.items()}}

    X_new = pd.DataFrame([row]).fillna(0)
    pred = model.predict(X_new)[0]

    if pred == 2:
        return f"🏆 Gana {local}"
    elif pred == 0:
        return f"🏆 Gana {visitante}"
    else:
        return "🤝 Empate probable"