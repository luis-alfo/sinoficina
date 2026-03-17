"""
Seed the Airtable base with genres and albums.
"""

from airtable_client import create_records

GENRES = [
    {"Nombre": "Pop", "Color": "#FF6B6B"},
    {"Nombre": "Rock", "Color": "#4ECDC4"},
    {"Nombre": "Rock Alternativo", "Color": "#45B7D1"},
    {"Nombre": "Punk Rock", "Color": "#96CEB4"},
    {"Nombre": "Nu Metal", "Color": "#2C3E50"},
    {"Nombre": "R&B", "Color": "#9B59B6"},
    {"Nombre": "Hip Hop", "Color": "#E67E22"},
    {"Nombre": "Reggaetón", "Color": "#F39C12"},
    {"Nombre": "Trap Latino", "Color": "#E74C3C"},
    {"Nombre": "Pop Latino", "Color": "#1ABC9C"},
    {"Nombre": "Flamenco", "Color": "#C0392B"},
    {"Nombre": "Electrónica", "Color": "#3498DB"},
]

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


def seed_genres():
    print(f"Seeding {len(GENRES)} genres...")
    n = create_records("Géneros", GENRES)
    print(f"Created {n} genres")
    return n


def seed_albums():
    print(f"Seeding {len(SAMPLE_ALBUMS)} albums...")
    n = create_records("Álbumes", SAMPLE_ALBUMS)
    print(f"Created {n} albums")
    return n


def seed_all():
    seed_genres()
    seed_albums()


if __name__ == "__main__":
    seed_all()
