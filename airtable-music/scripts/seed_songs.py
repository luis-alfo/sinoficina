"""
Seed the Canciones table with sample songs from Warner artists.
"""

from airtable_client import create_records

SAMPLE_SONGS = [
    # Ed Sheeran - Divide
    {"Título": "Shape of You", "Productores": "Steve Mac, Ed Sheeran", "Compositores": "Ed Sheeran, Steve Mac, Johnny McDaid", "BPM": 96, "Tonalidad": "C#", "Explícito": False},
    {"Título": "Castle on the Hill", "Productores": "Benny Blanco", "Compositores": "Ed Sheeran, Benny Blanco", "BPM": 135, "Tonalidad": "D", "Explícito": False},
    {"Título": "Galway Girl", "Productores": "Ed Sheeran", "Compositores": "Ed Sheeran, Foy Vance, Johnny McDaid", "BPM": 100, "Tonalidad": "A", "Explícito": False},
    # Dua Lipa - Future Nostalgia
    {"Título": "Don't Start Now", "Productores": "Ian Kirkpatrick", "Compositores": "Dua Lipa, Caroline Ailin, Ian Kirkpatrick, Emily Warren", "BPM": 124, "Tonalidad": "B", "Explícito": False},
    {"Título": "Levitating", "Productores": "Stuart Price, Koz", "Compositores": "Dua Lipa, Clarence Coffee Jr., Sarah Hudson, Stephen Kozmeniuk", "BPM": 103, "Tonalidad": "B", "Explícito": False},
    {"Título": "Physical", "Productores": "Jason Evigan", "Compositores": "Dua Lipa, Jason Evigan, Clarence Coffee Jr., Sarah Hudson", "BPM": 148, "Tonalidad": "F#", "Explícito": False},
    # Bruno Mars - 24K Magic
    {"Título": "24K Magic", "Productores": "Bruno Mars, Shampoo Press & Curl", "Compositores": "Bruno Mars, Philip Lawrence, Chris Brown", "BPM": 107, "Tonalidad": "F#", "Explícito": False},
    {"Título": "That's What I Like", "Productores": "Bruno Mars, Shampoo Press & Curl", "Compositores": "Bruno Mars, Philip Lawrence, James Fauntleroy", "BPM": 134, "Tonalidad": "D", "Explícito": False},
    # Coldplay - Music of the Spheres
    {"Título": "My Universe", "Productores": "Max Martin", "Compositores": "Chris Martin, Max Martin, Oscar Holter", "BPM": 105, "Tonalidad": "D", "Explícito": False},
    {"Título": "Higher Power", "Productores": "Max Martin", "Compositores": "Chris Martin, Max Martin, Oscar Holter, Bill Rahko", "BPM": 115, "Tonalidad": "E", "Explícito": False},
    # Rosalía - Motomami
    {"Título": "SAOKO", "Productores": "El Guincho, Rosalía", "Compositores": "Rosalía, El Guincho, Dylan Wiggins", "BPM": 100, "Tonalidad": "G", "Explícito": True},
    {"Título": "BIZCOCHITO", "Productores": "El Guincho, Rosalía", "Compositores": "Rosalía, El Guincho", "BPM": 130, "Tonalidad": "A", "Explícito": True},
    {"Título": "DESPECHÁ", "Productores": "El Guincho, Rosalía", "Compositores": "Rosalía, El Guincho", "BPM": 125, "Tonalidad": "C", "Explícito": False},
    # Linkin Park - Meteora
    {"Título": "Numb", "Productores": "Don Gilmore", "Compositores": "Linkin Park", "BPM": 110, "Tonalidad": "F#", "Explícito": False},
    {"Título": "Somewhere I Belong", "Productores": "Don Gilmore", "Compositores": "Linkin Park", "BPM": 80, "Tonalidad": "B", "Explícito": False},
    {"Título": "Faint", "Productores": "Don Gilmore", "Compositores": "Linkin Park", "BPM": 135, "Tonalidad": "D", "Explícito": False},
    # Green Day - American Idiot
    {"Título": "Boulevard of Broken Dreams", "Productores": "Rob Cavallo, Green Day", "Compositores": "Billie Joe Armstrong, Green Day", "BPM": 83, "Tonalidad": "F", "Explícito": False},
    {"Título": "Holiday", "Productores": "Rob Cavallo, Green Day", "Compositores": "Billie Joe Armstrong, Green Day", "BPM": 148, "Tonalidad": "F", "Explícito": True},
    # Myke Towers
    {"Título": "LA FALDA", "Productores": "Caleb Calloway, Chris Jedi", "Compositores": "Myke Towers", "BPM": 96, "Tonalidad": "A", "Explícito": True},
    # Manuel Turizo
    {"Título": "La Bachata", "Productores": "Slow Mike, Kevyn Cruz", "Compositores": "Manuel Turizo", "BPM": 130, "Tonalidad": "G#", "Explícito": False},
]


def seed():
    print(f"Seeding {len(SAMPLE_SONGS)} songs...")
    n = create_records("Canciones", SAMPLE_SONGS)
    print(f"Created {n} songs")


if __name__ == "__main__":
    seed()
