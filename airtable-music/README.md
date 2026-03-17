# Airtable Music Database - Warner Music Global

Proyecto de formación para gestionar una base de datos musical en Airtable,
con artistas del catálogo de **Warner Music Global**.

## Estructura

La base de datos imita la estructura de Spotify añadiendo campos de gestión musical profesional.

### Tablas principales

| Tabla | Descripción |
|-------|-------------|
| **Artistas** | Catálogo de artistas de Warner Music Global |
| **Álbumes** | Discografía completa de cada artista |
| **Canciones** | Tracks individuales con metadatos |
| **Playlists** | Listas de reproducción curadas |
| **Géneros** | Clasificación de géneros musicales |
| **Gestión** | Datos de management: contratos, representantes, sellos |

## Configuración

### Variables de entorno / Secrets de GitHub

| Variable | Descripción |
|----------|-------------|
| `AIRTABLE_API_KEY` | Personal Access Token de Airtable |
| `AIRTABLE_BASE_ID` | ID de la base: `appGiSPPxrhb0LXYe` |

### Uso

```bash
# Fetch de la estructura actual de la base
python scripts/fetch_base_schema.py

# Sincronizar datos de artistas Warner
python scripts/sync_warner_artists.py

# Poblar la base con datos iniciales
python scripts/seed_data.py
```

## Airtable Base

- **Base URL**: https://airtable.com/appGiSPPxrhb0LXYe
- **Table ID**: `tbleKxAUsF9ue7PCb`
- **View ID**: `viwJuBajnfRVqYAyM`
