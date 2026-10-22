"""
Cliente de la API interna de www.fcf.cat (Federació Catalana de Futbol).
API pública sin autenticación: son las rutas /api/* del frontend Next.js.
Ver fcf/ENDPOINTS.md para el mapa completo.
"""

import json
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://www.fcf.cat/api"
ESCUDOS_URL = "https://files.fcf.cat/escudos/clubes/escudos/"
USER_AGENT = "Mozilla/5.0 (sinoficina fcf_client)"


def api_get(path, **params):
    """GET a un endpoint de /api. Los params con valor None se omiten."""
    query = urlencode({k: v for k, v in params.items() if v is not None})
    url = f"{BASE_URL}{path}" + (f"?{query}" if query else "")
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


# --- Catálogos -------------------------------------------------------------

def get_temporadas():
    return api_get("/competition/temporadas")


def get_disciplinas():
    return api_get("/competition/disciplines")


def get_competiciones(disciplina_id, temporada):
    return api_get("/competition/competicions", disciplinaId=disciplina_id, temporada=temporada)


def get_grupos(competicion_id):
    return api_get("/competition/grupos", competicioId=competicion_id)


# --- Grupo -----------------------------------------------------------------

def get_partidos(grup_id):
    """Calendario/resultados del grupo: dict {jornada: [partidos]} con CODACTA."""
    return api_get("/competition/partidos", grupId=grup_id)


def get_clasificacion(grup_id):
    return api_get("/competition/classificacio", grupId=grup_id)


def get_equipos(grup_id):
    return api_get("/competition/equipos", grupId=grup_id)


def get_goleadores(grup_id, temporada):
    return api_get("/competition/goleadores", grupId=grup_id, temporada=temporada)


def get_sanciones(grup_id, temporada):
    return api_get("/competition/sanciones", grupId=grup_id, temporada=temporada)


def get_joc_net(grup_id, temporada):
    return api_get("/competition/joc-net", grupId=grup_id, temporada=temporada)


# --- Partido / jugador -----------------------------------------------------

def get_acta(codacta):
    """Acta completa: cabecera, árbitros, alineaciones, técnicos, goles, tarjetas, cambios."""
    return api_get("/competition/acta", codacta=codacta)


def get_jugador_stats(jugador_id, codgrupo=None, temporada=None):
    """{"partidos", "goles", "sanciones"} del jugador (filtrable por grupo/temporada)."""
    return api_get("/competition/jugador-stats", jugadorId=jugador_id, codgrupo=codgrupo, temporada=temporada)


if __name__ == "__main__":
    codacta = sys.argv[1] if len(sys.argv) > 1 else "4149069"
    print(json.dumps(get_acta(codacta), ensure_ascii=False, indent=2))
