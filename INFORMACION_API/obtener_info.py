import requests
import json

# CREDENCIALES
API_KEY = '5kW8o9bTC8dl47dX'       # Reemplazá con tu clave real
SECRET = 'SY4dFa5AvLSDa2zgnvoLFAFiISDMZQJS'         # Reemplazá con tu secreto real

# URL BASE
BASE_URL = 'https://livescore-api.com/api-client'
COMPETITION_ID = 23  # Liga Profesional Argentina

#OBTENER TODA LA DATA DE TABLA DE POSICIONES 
standings_url = f'{BASE_URL}/competitions/standings.json?key={API_KEY}&secret={SECRET}&competition_id=23&season_id=54&stage_id=3351&phase_id=2'
r = requests.get(standings_url)
data = r.json()
#FILTRO DATA PARA OBTENER SOLO LA FASE 2
tabla = []
for i in data['data']['table']:
    if i.get('stage_name') == 'Phase 2':
        tabla.append({
        'equipo': i['name'],
        'posicion': int(i['rank']),
        'puntos': i['points'],
        'jugados': int(i['matches']),
        'ganados': int(i['won']),
        'empates': int(i['drawn']),
        'perdidos': int(i['lost']),
        'goles_a_favor': int(i['goals_scored']),
        'goles_en_contra': int(i['goals_conceded'])
    })
with open('tabla_posiciones_fase_2.json', 'w') as f:
    json.dump(tabla, f, indent=2)
print("Tabla de posiciones guardada exitosamente.")



#OBTENER EL FIXTURE DE PARTIDOS, EL CUAL TIENE 7 PAGINAS
all_matches = []
for page in range(1, 8):  # Hay 7 páginas
    url = f'{BASE_URL}/matches/history.json?key={API_KEY}&secret={SECRET}&competition_id={COMPETITION_ID}&from=2025-07-10&to=2025-11-02&page={page}'
    response = requests.get(url)
    data = response.json()
    all_matches.extend(data['data']['match'])

#GUARDO EN UN JSON EL FIXTURE COMPLETO
with open('fixture_completo.json', 'w') as f:
    json.dump(all_matches, f, indent=2)

print("Fixture completo guardado con las 7 páginas.")
# PROCESAR GOLES LOCALES Y VISITANTES
estadisticas = {}
for match in all_matches:
    if match.get('status') != 'FINISHED':
        continue

    home_team = match['home']['name']
    away_team = match['away']['name']
    score_str = match.get('scores', {}).get('ft_score', '')

    if not score_str or ' - ' not in score_str:
        continue

    try:
        home_goals, away_goals = map(int, score_str.strip().split(' - '))
    except ValueError:
        continue

    # Inicializar equipos si no existen
    for team in [home_team, away_team]:
        if team not in estadisticas:
            estadisticas[team] = {
                'goles_local': 0,
                'goles_visitante': 0,
                'recibidos_local': 0,
                'recibidos_visitante': 0
            }

    # Acumular estadísticas
    estadisticas[home_team]['goles_local'] += home_goals
    estadisticas[home_team]['recibidos_local'] += away_goals
    estadisticas[away_team]['goles_visitante'] += away_goals
    estadisticas[away_team]['recibidos_visitante'] += home_goals
# GUARDAR ESTADÍSTICAS EN UN ARCHIVO JSON
with open('goles_local_visitante.json', 'w') as f:
    json.dump(estadisticas, f, indent=2)

print("Goles local/visitante procesados correctamente.")