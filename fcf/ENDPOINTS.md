# API interna de fcf.cat — ingeniería inversa

Origen: acta https://www.fcf.cat/ca/competicio/acta/4149069
(Quarta Catalana, Grup 20, J5: GUINARDÓ C.F. A 5–0 SANT IGNASI C.E. C, 17/10/2026).

## Cómo funciona la web

- `www.fcf.cat` es un frontend **Next.js (App Router, Turbopack)** detrás de CloudFront.
- La página del acta se renderiza **en servidor** (RSC): el HTML ya trae los datos y el
  navegador no llama a ninguna API para pintarla.
- El mismo frontend expone rutas `/api/*` (Next.js route handlers) que hacen de proxy al
  backend de la federación. **No requieren autenticación, cookies ni tokens.**
- Los nombres de campos (`CODACTA`, `CODEQUIPO_CASA`, `GOLES_FUERA`…) vienen tal cual de la
  base de datos de la FCF (en castellano y mayúsculas); los route handlers añaden algunos
  campos en minúsculas (`nombre_competicion`, `jugadores_equipo_local`…).
- Las rutas se descubrieron leyendo los chunks JS de `/_next/static/chunks/*.js`.
  `/api/competition/acta` no aparece en el JS cliente (la usa solo el servidor); su
  parámetro (`codacta`) se encontró probando nombres.

## Endpoint principal: el acta

```
GET https://www.fcf.cat/api/competition/acta?codacta=4149069
```

| Campo | Contenido |
|---|---|
| `CODACTA`, `CODTEMPORADA`, `CODGRUPO`, `JORNADA` | Identificadores del partido |
| `CODEQUIPO_CASA`, `CODEQUIPO_FUERA` | IDs de equipo |
| `COMIENZO1`, `FECHA` | Hora/fecha (ver nota de zona horaria) |
| `CAMPO`, `CODIGO_CAMPO` | Campo (→ `/api/camps/{CODIGO_CAMPO}`) |
| `GOLES_CASA`, `GOLES_FUERA`, `PENALTIS_*` | Resultado |
| `CERRADA`, `ESTADO` | `1` = acta cerrada |
| `CODDELEGADO_CAMPO/CASA/FUERA` | `-1` si no hay |
| `temporada_nombre`, `nombre_grupo`, `nombre_competicion` | Etiquetas legibles |
| `arbitros[]` | `CODARBITRO`, `nombre_arbitro`, `rol` ("Principal"…), `delegacion` |
| `equipo_local`, `equipo_visitante` | `CODEQUIPO`, `NOMBRE_EQUIPO`, `CODCLUB`, `escudo` |
| `jugadores_equipo_local/visitante[]` | `id`, `nombre`, `dorsal`, `titular`, `capitan`, `portero` (`"0"/"1"`) |
| `tecnicos_equipo_local/visitante[]` | `id`, `nombre`, `tipo_nombre` (`D` delegado, `ET` entrenador titular…) |
| `goles_equipo_local/visitante[]` | `id_jugador`, `nombre_jugador`, `dorsal`, `minuto`, `tipo_gol` |
| `penaltis_equipo_local/visitante[]` | Tanda de penaltis |
| `tarjetas_equipo_local/visitante[]` | `id_jugador`, `tipo_tarjeta`, `minuto`, `segunda_amarilla` |
| `sustituciones_equipo_local/visitante[]` | Cambios |

Códigos observados: `tipo_gol = "100"` → gol normal; `tipo_tarjeta = "100"` → amarilla.
La web distingue además gol de penalti, gol en propia, doble amarilla y roja, pero esos
códigos no se han visto todavía en un acta real (confirmar cuando aparezcan).

## Resto de endpoints

Base: `https://www.fcf.cat/api`. IDs de ejemplo del mismo partido:
temporada `22`, disciplina Futbol 11 `19308233`, grupo `58161913`, equipo `40574`, club `1578`, campo `68`.

| Endpoint | Devuelve |
|---|---|
| `/competition/temporadas` | `[{value:"22", label:"2026-2027"}, …]` |
| `/competition/disciplines` | Futbol 11, Futbol 7, Futbol Sala, Femení… |
| `/competition/competicions?disciplinaId=&temporada=` | Competiciones (`value` = competicioId) |
| `/competition/grupos?competicioId=` | Grupos (`value` = grupId) |
| `/competition/partidos?grupId=` | `{ "1": [partidos J1], "2": … }` — cada partido trae `CODACTA`, equipos, escudos, resultado, campo, lat/long |
| `/competition/classificacio?grupId=` | `{data:[…], promociones:[…]}` |
| `/competition/equipos?grupId=` | Equipos (`value`/`label`) |
| `/competition/equipacions?grupId=` | Colores de equipación por equipo |
| `/competition/goleadores?grupId=&temporada=` | Pichichi del grupo |
| `/competition/goles-favor?grupId=&equipId=` | `[{total}]` |
| `/competition/goles-contra?grupId=&equipId=` | `[{total}]` |
| `/competition/goles?jugadorId=` | `[{total}]` goles del jugador |
| `/competition/sanciones?grupId=&temporada=` | `{jornada: [sanciones]}` con texto del comité |
| `/competition/joc-net?grupId=&temporada=` | Clasificación de juego limpio |
| `/competition/jugador-stats?jugadorId=&codgrupo=&temporada=` | `{partidos, goles, sanciones}` |
| `/camps/{id}` | Ficha del campo (dirección, CP…) |
| `/clubs/{clubId}/team/{equipId}?temporadaId=` | Ficha del equipo (equipaciones, plantilla…) |
| `/search?q=&locale=ca` | Buscador: clubs, camps, news, competicions… |
| `/news/list/1?page=1` | Noticias |

Escudos: `https://files.fcf.cat/escudos/clubes/escudos/{escudo}`.

## Recorrido típico para sacar todas las actas de un grupo

```
temporadas → disciplines → competicions → grupos → partidos (CODACTA) → acta?codacta=
```

## Avisos

- **Zona horaria:** `acta.COMIENZO1` llega como `2026-10-17T20:00:00.000Z`, pero en `partidos`
  es `2026-10-17T20:00:00` sin zona. Es hora local de Catalunya marcada como UTC (los horarios del grupo —12:00, 14:15, 20:15— solo cuadran como hora local):
  no convertir.
- Errores devuelven HTTP 500 con `{"error":"Failed to fetch competition data"}` (p. ej. parámetro
  mal nombrado). Rutas inexistentes → 404 JSON.
- API no documentada ni oficial: puede cambiar sin aviso. Cachear y no martillear (CloudFront
  cachea las páginas 300 s).

Cliente: [`fcf_client.py`](fcf_client.py) — `python3 fcf/fcf_client.py 4149069` imprime el acta.
