"""
Sync Warner Music Global artists to the Airtable base.
Creates or updates records in the Artistas table with a curated list
of Warner artists for the training session.
"""

import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "appGiSPPxrhb0LXYe")
TABLE_ID = os.environ.get("AIRTABLE_TABLE_ID", "tbleKxAUsF9ue7PCb")
API_KEY = os.environ.get("AIRTABLE_API_KEY", "")

API_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"

# Artistas destacados de Warner Music Global para la formación
WARNER_ARTISTS = [
    {
        "Nombre": "Ed Sheeran",
        "País": "Reino Unido",
        "Sello": "Atlantic Records",
        "Género Principal": "Pop",
        "Verificado": True,
        "Biografía": "Cantautor y músico británico. Uno de los artistas más exitosos del siglo XXI.",
        "Spotify URL": "https://open.spotify.com/artist/6eUKZXaKkcviH0Ku9w2n3V",
    },
    {
        "Nombre": "Dua Lipa",
        "País": "Reino Unido",
        "Sello": "Warner Records",
        "Género Principal": "Pop",
        "Verificado": True,
        "Biografía": "Cantante y compositora británica de origen kosovar-albanés.",
        "Spotify URL": "https://open.spotify.com/artist/6M2wZ9GZgrQXHCFfjv46we",
    },
    {
        "Nombre": "Bruno Mars",
        "País": "Estados Unidos",
        "Sello": "Atlantic Records",
        "Género Principal": "Pop/R&B",
        "Verificado": True,
        "Biografía": "Cantante, compositor, productor y bailarín estadounidense.",
        "Spotify URL": "https://open.spotify.com/artist/0du5cEVh5yTK9QJze8zA0C",
    },
    {
        "Nombre": "Coldplay",
        "País": "Reino Unido",
        "Sello": "Parlophone",
        "Género Principal": "Rock Alternativo",
        "Verificado": True,
        "Biografía": "Banda británica de rock alternativo formada en Londres en 1996.",
        "Spotify URL": "https://open.spotify.com/artist/4gzpq5DPGxSnKTe4SA8HAU",
    },
    {
        "Nombre": "Myke Towers",
        "País": "Puerto Rico",
        "Sello": "Warner Music Latina",
        "Género Principal": "Reggaetón/Trap",
        "Verificado": True,
        "Biografía": "Rapero y cantante puertorriqueño de trap latino y reggaetón.",
        "Spotify URL": "https://open.spotify.com/artist/7iK8PXO48WeuP03g8YR51W",
    },
    {
        "Nombre": "Anitta",
        "País": "Brasil",
        "Sello": "Warner Records",
        "Género Principal": "Pop Latino/Reggaetón",
        "Verificado": True,
        "Biografía": "Cantante, compositora, actriz y empresaria brasileña.",
        "Spotify URL": "https://open.spotify.com/artist/7FNnA9vBm6EKceENgCGRMb",
    },
    {
        "Nombre": "Linkin Park",
        "País": "Estados Unidos",
        "Sello": "Warner Records",
        "Género Principal": "Rock/Nu Metal",
        "Verificado": True,
        "Biografía": "Banda de rock estadounidense formada en Agoura Hills, California.",
        "Spotify URL": "https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz",
    },
    {
        "Nombre": "Green Day",
        "País": "Estados Unidos",
        "Sello": "Reprise Records",
        "Género Principal": "Punk Rock",
        "Verificado": True,
        "Biografía": "Banda de punk rock estadounidense formada en 1987.",
        "Spotify URL": "https://open.spotify.com/artist/7oPftvlwr6VrsViSDV7fJY",
    },
    {
        "Nombre": "Rosalía",
        "País": "España",
        "Sello": "Atlantic Records",
        "Género Principal": "Pop/Flamenco",
        "Verificado": True,
        "Biografía": "Cantante y compositora española que fusiona flamenco con música urbana.",
        "Spotify URL": "https://open.spotify.com/artist/7ltDVBr6mKbRvohxheJ9h1",
    },
    {
        "Nombre": "Lizzo",
        "País": "Estados Unidos",
        "Sello": "Atlantic Records",
        "Género Principal": "Pop/Hip Hop",
        "Verificado": True,
        "Biografía": "Cantante, rapera y flautista estadounidense.",
        "Spotify URL": "https://open.spotify.com/artist/56oDRnqbIiwx4mymNEv7dS",
    },
    {
        "Nombre": "Manuel Turizo",
        "País": "Colombia",
        "Sello": "Warner Music Latina",
        "Género Principal": "Reggaetón/Pop Latino",
        "Verificado": True,
        "Biografía": "Cantante y compositor colombiano de música urbana.",
        "Spotify URL": "https://open.spotify.com/artist/0tmwSHipWxN12fsoLcFU3B",
    },
    {
        "Nombre": "Muse",
        "País": "Reino Unido",
        "Sello": "Warner Records",
        "Género Principal": "Rock Alternativo",
        "Verificado": True,
        "Biografía": "Banda de rock alternativo inglesa formada en Teignmouth en 1994.",
        "Spotify URL": "https://open.spotify.com/artist/12Chz98pHFMPJEknJQMWvI",
    },
]


def create_records(artists):
    if not API_KEY:
        print("Error: AIRTABLE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Airtable API accepts max 10 records per request
    batch_size = 10
    created = 0

    for i in range(0, len(artists), batch_size):
        batch = artists[i:i + batch_size]
        records = []
        for artist in batch:
            # Remove "Género Principal" as it's a linked record, needs special handling
            fields = {k: v for k, v in artist.items() if k != "Género Principal"}
            records.append({"fields": fields})

        payload = json.dumps({"records": records}).encode()

        req = Request(API_URL, data=payload, method="POST", headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        })

        try:
            with urlopen(req) as resp:
                result = json.loads(resp.read().decode())
                created += len(result.get("records", []))
        except HTTPError as e:
            body = e.read().decode() if e.fp else ""
            print(f"Error creating records: {e.code} {e.reason}\n{body}", file=sys.stderr)
            sys.exit(1)

    print(f"Created {created} artist records in Airtable")


if __name__ == "__main__":
    create_records(WARNER_ARTISTS)
