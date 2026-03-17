# Airtable Music DB — Contexto para Claude

## Qué es este proyecto
Sistema de automatización para gestionar una base de datos musical en Airtable (Warner Music Global) usando GitHub Actions y scripts Python.

## Estructura
- `scripts/` — Scripts Python (todos importan de `airtable_client.py` y `spotify_client.py`)
- `schemas/` — Snapshots del schema de Airtable (se actualizan automáticamente)
- Workflow: `.github/workflows/airtable-sync.yml`

## Aprendizajes y errores conocidos
Ver `/APRENDIZAJES.md` en la raíz del repo para lecciones detalladas sobre:
- Errores comunes de la API de Airtable (URL-encoding, campos rating, checkbox, etc.)
- Configuración de GitHub Actions (Node.js warnings, errores silenciosos, inputs)
- Decisiones de arquitectura

## Reglas importantes
- Los scripts son idempotentes: verifican existencia antes de crear
- `provision_schema.py` debe correr antes de cualquier seed o fetch de Spotify
- El cliente compartido `airtable_client.py` debe propagar errores (nunca silenciarlos)
- Los nombres de tabla con acentos (Géneros, Álbumes) deben ir URL-encoded
- El primer campo de cada tabla Airtable debe ser `singleLineText`
- Campos `rating` requieren `"icon": "star"` en options

## Secrets necesarios en GitHub
- `AIRTABLE_API_KEY` — Personal access token de Airtable
- `SPOTIFY_CLIENT_ID` — Spotify Developer app
- `SPOTIFY_CLIENT_SECRET` — Spotify Developer app
- `AIRTABLE_BASE_ID` está hardcodeado: `appGiSPPxrhb0LXYe`

## Orden de ejecución del workflow
1. `provision-schema` → 2. `seed-genres` → 3. `sync-artists` → 4. `seed-albums` → 5. `seed-songs` → 6. `fetch-spotify-images` → 7. `sync-playlists`
