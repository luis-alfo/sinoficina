"""
Sync Warner Music Global artists to the Airtable base.
"""

from airtable_client import create_records

WARNER_ARTISTS = [
    {
        "Nombre": "Ed Sheeran",
        "País": "Reino Unido",
        "Sello": "Atlantic Records",
        "Verificado": True,
        "Biografía": "Cantautor y músico británico. Uno de los artistas más exitosos del siglo XXI.",
        "Spotify URL": "https://open.spotify.com/artist/6eUKZXaKkcviH0Ku9w2n3V",
    },
    {
        "Nombre": "Dua Lipa",
        "País": "Reino Unido",
        "Sello": "Warner Records",
        "Verificado": True,
        "Biografía": "Cantante y compositora británica de origen kosovar-albanés.",
        "Spotify URL": "https://open.spotify.com/artist/6M2wZ9GZgrQXHCFfjv46we",
    },
    {
        "Nombre": "Bruno Mars",
        "País": "Estados Unidos",
        "Sello": "Atlantic Records",
        "Verificado": True,
        "Biografía": "Cantante, compositor, productor y bailarín estadounidense.",
        "Spotify URL": "https://open.spotify.com/artist/0du5cEVh5yTK9QJze8zA0C",
    },
    {
        "Nombre": "Coldplay",
        "País": "Reino Unido",
        "Sello": "Parlophone",
        "Verificado": True,
        "Biografía": "Banda británica de rock alternativo formada en Londres en 1996.",
        "Spotify URL": "https://open.spotify.com/artist/4gzpq5DPGxSnKTe4SA8HAU",
    },
    {
        "Nombre": "Myke Towers",
        "País": "Puerto Rico",
        "Sello": "Warner Music Latina",
        "Verificado": True,
        "Biografía": "Rapero y cantante puertorriqueño de trap latino y reggaetón.",
        "Spotify URL": "https://open.spotify.com/artist/7iK8PXO48WeuP03g8YR51W",
    },
    {
        "Nombre": "Anitta",
        "País": "Brasil",
        "Sello": "Warner Records",
        "Verificado": True,
        "Biografía": "Cantante, compositora, actriz y empresaria brasileña.",
        "Spotify URL": "https://open.spotify.com/artist/7FNnA9vBm6EKceENgCGRMb",
    },
    {
        "Nombre": "Linkin Park",
        "País": "Estados Unidos",
        "Sello": "Warner Records",
        "Verificado": True,
        "Biografía": "Banda de rock estadounidense formada en Agoura Hills, California.",
        "Spotify URL": "https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz",
    },
    {
        "Nombre": "Green Day",
        "País": "Estados Unidos",
        "Sello": "Reprise Records",
        "Verificado": True,
        "Biografía": "Banda de punk rock estadounidense formada en 1987.",
        "Spotify URL": "https://open.spotify.com/artist/7oPftvlwr6VrsViSDV7fJY",
    },
    {
        "Nombre": "Rosalía",
        "País": "España",
        "Sello": "Atlantic Records",
        "Verificado": True,
        "Biografía": "Cantante y compositora española que fusiona flamenco con música urbana.",
        "Spotify URL": "https://open.spotify.com/artist/7ltDVBr6mKbRvohxheJ9h1",
    },
    {
        "Nombre": "Lizzo",
        "País": "Estados Unidos",
        "Sello": "Atlantic Records",
        "Verificado": True,
        "Biografía": "Cantante, rapera y flautista estadounidense.",
        "Spotify URL": "https://open.spotify.com/artist/56oDRnqbIiwx4mymNEv7dS",
    },
    {
        "Nombre": "Manuel Turizo",
        "País": "Colombia",
        "Sello": "Warner Music Latina",
        "Verificado": True,
        "Biografía": "Cantante y compositor colombiano de música urbana.",
        "Spotify URL": "https://open.spotify.com/artist/0tmwSHipWxN12fsoLcFU3B",
    },
    {
        "Nombre": "Muse",
        "País": "Reino Unido",
        "Sello": "Warner Records",
        "Verificado": True,
        "Biografía": "Banda de rock alternativo inglesa formada en Teignmouth en 1994.",
        "Spotify URL": "https://open.spotify.com/artist/12Chz98pHFMPJEknJQMWvI",
    },
]


def sync():
    print(f"Syncing {len(WARNER_ARTISTS)} Warner artists...")
    n = create_records("Artistas", WARNER_ARTISTS)
    print(f"Created {n} artist records")


if __name__ == "__main__":
    sync()
