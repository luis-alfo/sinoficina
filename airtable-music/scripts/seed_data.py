"""
Seed the Airtable base with sample data: genres, albums, and songs
for the Warner Music Global training database.
"""

import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "appGiSPPxrhb0LXYe")
API_KEY = os.environ.get("AIRTABLE_API_KEY", "")

API_BASE = f"https://api.airtable.com/v0/{BASE_ID}"

GENRES = [
    {"Nombre": "Pop", "Color": "#FF6B6B"},
    {"Nombre": "Rock", "Color": "#4ECDC4"},
    {"Nombre": "Rock Alternativo", "Color": "#45B7D1", "Género Padre": "Rock"},
    {"Nombre": "Punk Rock", "Color": "#96CEB4", "Género Padre": "Rock"},
    {"Nombre": "Nu Metal", "Color": "#2C3E50", "Género Padre": "Rock"},
    {"Nombre": "R&B", "Color": "#9B59B6"},
    {"Nombre": "Hip Hop", "Color": "#E67E22"},
    {"Nombre": "Reggaetón", "Color": "#F39C12"},
    {"Nombre": "Trap Latino", "Color": "#E74C3C", "Género Padre": "Reggaetón"},
    {"Nombre": "Pop Latino", "Color": "#1ABC9C"},
    {"Nombre": "Flamenco", "Color": "#C0392B"},
    {"Nombre": "Electrónica", "Color": "#3498DB"},
]

# Sample albums for some artists
SAMPLE_ALBUMS = [
    {"Título": "÷ (Divide)", "Tipo": "Álbum", "Fecha Lanzamiento": "2017-03-03", "Sello": "Atlantic Records"},
    {"Título": "Future Nostalgia", "Tipo": "Álbum", "Fecha Lanzamiento": "2020-03-27", "Sello": "Warner Records"},
    {"Título": "24K Magic", "Tipo": "Álbum", "Fecha Lanzamiento": "2016-11-18", "Sello": "Atlantic Records"},
    {"Título": "Music of the Spheres", "Tipo": "Álbum", "Fecha Lanzamiento": "2021-10-15", "Sello": "Parlophone"},
    {"Título": "LYKE MIKE", "Tipo": "Álbum", "Fecha Lanzamiento": "2021-05-21", "Sello": "Warner Music Latina"},
    {"Título": "Motomami", "Tipo": "Álbum", "Fecha Lanzamiento": "2022-03-18", "Sello": "Atlantic Records"},
    {"Título": "Meteora", "Tipo": "Álbum", "Fecha Lanzamiento": "2003-03-25", "Sello": "Warner Records"},
    {"Título": "American Idiot", "Tipo": "Álbum", "Fecha Lanzamiento": "2004-09-21", "Sello": "Reprise Records"},
]


def post_records(table_name, records_data):
    """Create records in a specific table."""
    if not API_KEY:
        print("Error: AIRTABLE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    url = f"{API_BASE}/{table_name}"
    batch_size = 10
    created = 0

    for i in range(0, len(records_data), batch_size):
        batch = records_data[i:i + batch_size]
        records = [{"fields": item} for item in batch]
        payload = json.dumps({"records": records}).encode()

        req = Request(url, data=payload, method="POST", headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        })

        try:
            with urlopen(req) as resp:
                result = json.loads(resp.read().decode())
                created += len(result.get("records", []))
        except HTTPError as e:
            body = e.read().decode() if e.fp else ""
            print(f"Error in {table_name}: {e.code} {e.reason}\n{body}", file=sys.stderr)
            return created

    return created


def seed():
    # Remove linked fields that need record IDs (handle manually)
    genres_clean = [{k: v for k, v in g.items() if k != "Género Padre"} for g in GENRES]

    print("Seeding Géneros...")
    n = post_records("Géneros", genres_clean)
    print(f"  Created {n} genres")

    print("Seeding Álbumes...")
    n = post_records("Álbumes", SAMPLE_ALBUMS)
    print(f"  Created {n} albums")

    print("Seed complete!")


if __name__ == "__main__":
    seed()
