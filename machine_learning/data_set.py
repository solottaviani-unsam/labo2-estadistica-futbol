import json
from pathlib import Path #importo esta libreria porque me ayuda por un error de importacion que estaba teniendo
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 1. CARGA DE JSON 
# Esto evita depender del `cwd` desde el que se ejecute Streamlit/Python que me estaba fallando
BASE_DIR = Path(__file__).resolve().parent.parent
INFO_DIR = BASE_DIR / "info"

#load_json: Carga un archivo JSON y maneja los errores asi puedo replicar en todos los archivos necesarios
def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {path}. Usando valor por defecto.")
        return default
    except json.JSONDecodeError as e:
        print(f"No se pudo parsear JSON {path}: {e}")


fixture = load_json(INFO_DIR / "fixture_completo.json", [])
goles = load_json(INFO_DIR / "goles_local_visitante.json", {})
tabla = load_json(INFO_DIR / "tabla_posiciones_fase_2.json", [])

tabla_df = pd.DataFrame(tabla)

# 2. FUNCIONES HELPERS
#get_team_features: Devuelve posición, puntos, goles a favor y en contra
def get_team_features(team_name):
    row = tabla_df[tabla_df["equipo"] == team_name]

    #si la fila esta vacia retorno los valores en 0
    if row.empty:
        return {"posicion": 0, "puntos": 0, "gf": 0, "gc": 0}

    #selecciono la primera fila (debería ser la única)
    row = row.iloc[0]
    return {
        "posicion": row["posicion"],
        "puntos": int(row["puntos"]),
        "gf": row["goles_a_favor"],
        "gc": row["goles_en_contra"]
    }

#get_goles_features: Devuelve estadísticas de goles local/visitante
def get_goles_features(team_name):
    #si el equipo no está en el json de goles, retorno ceros
    if team_name not in goles:
        return {"gf_local": 0, "gf_vis": 0, "gc_local": 0, "gc_vis": 0}

    g = goles[team_name]
    return {
        "gf_local": g["goles_local"],
        "gf_vis": g["goles_visitante"],
        "gc_local": g["recibidos_local"],
        "gc_vis": g["recibidos_visitante"]
    }

# 3. CONSTRUCCIÓN DEL DATASET
# (sin goles_local y goles_visita para evitar data leakage)
rows = []

for match in fixture:
    local = match["home"]["name"]
    visitante = match["away"]["name"]

    score = match["scores"]["ft_score"]  #Ejemplo: "3 - 0"
    gl, gv = map(int, score.split("-"))

    # Resultado objetivo
    if gl > gv:
        resultado = 2   # gana local
    elif gl < gv:
        resultado = 0   # gana visitante
    else:
        resultado = 1   # empate

    f_local_tabla = get_team_features(local)
    f_local_goles = get_goles_features(local)
    f_vis_tabla = get_team_features(visitante)
    f_vis_goles = get_goles_features(visitante)

    row = {
        "local": local,
        "visitante": visitante,
        "resultado": resultado,

        # armo un nuevo diccionario features del local
        #{
        #   "loc_posicion": 4,
        #   "loc_puntos": 27,
        #   "loc_gf": 18,
        #   "loc_gc": 12
        #}
        **{f"loc_{k}": v for k, v in f_local_tabla.items()},
        **{f"loc_{k}": v for k, v in f_local_goles.items()},

        # tambien armo un nuevo diccionario features del visitante
        **{f"vis_{k}": v for k, v in f_vis_tabla.items()},
        **{f"vis_{k}": v for k, v in f_vis_goles.items()},
    }

    rows.append(row)

df = pd.DataFrame(rows)

# 4. ENTRENAR EL MODELO DE REGRESIÓN LOGÍSTICA (magia)
X = df.drop(columns=["resultado", "local", "visitante"])
y = df["resultado"]

X = X.fillna(0)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = LogisticRegression(
    multi_class="multinomial",
    solver="lbfgs",
    max_iter=1000
)

model.fit(X_train, y_train)

print("funciona?")
print(classification_report(y_test, y_pred := model.predict(X_test)))

# 5. FUNCIÓN DE PREDICCIÓN PARA LA INTERFAZ GRAFICA
def predecir(local, visitante):
    f_loc = {**get_team_features(local), **get_goles_features(local)}
    f_vis = {**get_team_features(visitante), **get_goles_features(visitante)}

    row = {
        **{f"loc_{k}": v for k, v in f_loc.items()},
        **{f"vis_{k}": v for k, v in f_vis.items()}
    }

    X_new = pd.DataFrame([row]).fillna(0)

    pred = model.predict(X_new)[0]

    if pred == 2:
        return f"🏆 Gana {local}"
    elif pred == 0:
        return f"🏆 Gana {visitante}"
    else:
        return "🤝 Empate probable"

# 6. DEVOLVER LISTA DE EQUIPOS AL FRONTEND
def obtener_equipos():
    return sorted(tabla_df["equipo"].unique())
