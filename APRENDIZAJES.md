# Aprendizajes — Sinoficina / Airtable Music DB

Documento de lecciones aprendidas durante el desarrollo del sistema de automatización
Airtable Music DB con GitHub Actions.

---

## 1. Airtable API — Errores comunes

### Los nombres de tabla con acentos deben ir URL-encoded
- Tablas como `Géneros` o `Álbumes` rompen las llamadas a la API si se pasan tal cual.
- **Solución:** usar `urllib.parse.quote(table_name, safe="")` en todas las URLs.
- Commit: `a42431d`

### El primer campo de cada tabla debe ser `singleLineText`
- Airtable exige que el campo primario sea de texto. Si intentas crear una tabla cuyo primer campo es `multipleSelects` o similar, falla con 422.
- **Solución:** asegurar que el primer campo definido en el schema sea siempre `singleLineText` (ej: campo "Referencia" en la tabla Gestión).

### Los campos `rating` requieren la opción `icon`
- Al crear un campo de tipo `rating`, la API devuelve: `"options.icon is missing"`.
- **Solución:** incluir `"icon": "star"` (u otro valor válido) en las options del campo.
- Commit: `4943685`

### Los campos `checkbox` requieren options (aunque sea `{}`)
- Campos como `Verificado`, `Explícito`, `Pública` necesitan `"options": {"icon": "check", "color": "greenBright"}` o al menos un objeto vacío.

### Las opciones de `singleSelect` / `multipleSelects` deben existir de antemano
- Si haces seed de datos con valores que no están en las opciones predefinidas del campo, la API los rechaza silenciosamente o falla.
- **Solución:** definir todas las opciones posibles en `provision_schema.py`.

---

## 2. GitHub Actions — Errores y configuración

### Warning de Node.js 20 en actions
- `actions/setup-python@v5` usa internamente Node.js 20, que está deprecado desde 2025.
- GitHub muestra un warning amarillo pero **no causa fallos** — es solo informativo.
- A partir de junio 2026, GitHub forzará Node.js 24 como default.
- Actualizar a `actions/checkout@v6` ya resuelve el warning para checkout.

### Los errores silenciosos hacen que Actions reporte éxito falso
- Si `api_request()` captura excepciones y retorna `None` sin re-lanzar, el script termina con exit code 0 aunque todas las llamadas API hayan fallado.
- **Solución:** propagar errores (`raise`) para que GitHub Actions detecte el fallo real.
- Commit: `0deb5c7`

### Los inputs opcionales de `workflow_dispatch` necesitan defaults
- Sin valores por defecto, los inputs opcionales como `table` y `data` llegan como cadena vacía, causando errores en los scripts.
- **Solución:** poner `default: '-'` y manejar ese valor en los scripts.

### El workflow solo corre desde la branch donde está definido
- Si haces un fix en un branch pero disparas el workflow desde `main`, usará la versión de `main` (sin el fix).
- **Solución:** hacer merge a `main` antes de ejecutar el workflow, o dispararlo desde el branch correcto.

---

## 3. Arquitectura — Decisiones clave

### Cliente centralizado (`airtable_client.py`)
- Inicialmente cada script tenía su propia lógica HTTP. Esto causaba duplicación y errores inconsistentes.
- Se creó `airtable_client.py` con funciones compartidas: `api_request()`, `get_records()`, `create_records()`, `update_records()`.
- Todos los scripts importan de este módulo.

### Cliente Spotify (`spotify_client.py`)
- Autenticación Client Credentials (no requiere usuario).
- Funciones: `get_artist()`, `get_album()`, `search()`, `get_playlist()`.
- Se usa para poblar fotos de artistas, portadas de álbumes, y sincronizar playlists.

### Provision antes de Seed
- El workflow ejecuta `provision_schema.py` automáticamente antes de acciones de Spotify.
- `provision_schema.py` detecta tablas/campos existentes y solo crea los que faltan (idempotente).

### PYTHONPATH en el workflow
- Los scripts están en `airtable-music/scripts/` y se importan entre sí.
- Se configuró `PYTHONPATH: ${{ github.workspace }}/airtable-music/scripts` en el workflow para que los imports funcionen.

---

## 4. Flujo de trabajo recomendado

```
1. provision-schema  → Crea tablas y campos
2. seed-genres       → Poblar géneros
3. sync-artists      → Importar artistas Warner
4. seed-albums       → Poblar álbumes
5. seed-songs        → Poblar canciones
6. fetch-spotify-images → Fotos y portadas desde Spotify
7. sync-playlists    → Playlists de Warner desde Spotify
```

Cada paso es idempotente y puede re-ejecutarse sin duplicar datos (los scripts verifican existencia antes de crear).

---

## 5. Secretos necesarios en GitHub

| Secret | Uso |
|--------|-----|
| `AIRTABLE_API_KEY` | Personal access token de Airtable |
| `SPOTIFY_CLIENT_ID` | App credentials de Spotify Developer |
| `SPOTIFY_CLIENT_SECRET` | App credentials de Spotify Developer |

El `AIRTABLE_BASE_ID` está hardcodeado en el workflow (`appGiSPPxrhb0LXYe`).

---

*Última actualización: 2026-03-17*
