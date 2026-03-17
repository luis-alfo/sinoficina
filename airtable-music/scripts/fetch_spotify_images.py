"""
Fetch artist photos and album covers from Spotify and update Airtable.

- Artists: uses the Spotify URL field to get artist images -> Foto field
- Albums: searches Spotify by title + artist name -> Portada field

Airtable attachment fields accept [{"url": "https://..."}] format.
"""

import time
from airtable_client import list_records, update_records
from spotify_client import (
    get_artist, search_album, extract_artist_id, get_best_image,
)


def fetch_artist_images():
    """Fetch artist photos from Spotify and update the Foto field in Airtable."""
    print("Fetching artists from Airtable...")
    artists = list_records("Artistas", fields=["Nombre", "Spotify URL", "Foto"])
    print(f"Found {len(artists)} artists\n")

    updates = []
    for record in artists:
        fields = record["fields"]
        name = fields.get("Nombre", "?")

        # Skip if already has a photo
        if fields.get("Foto"):
            print(f"  [skip] {name} — already has photo")
            continue

        spotify_url = fields.get("Spotify URL")
        artist_id = extract_artist_id(spotify_url)
        if not artist_id:
            print(f"  [skip] {name} — no Spotify URL")
            continue

        artist_data = get_artist(artist_id)
        if not artist_data:
            print(f"  [fail] {name} — Spotify API error")
            continue

        image_url = get_best_image(artist_data.get("images", []))
        if not image_url:
            print(f"  [skip] {name} — no image on Spotify")
            continue

        updates.append({
            "id": record["id"],
            "fields": {
                "Foto": [{"url": image_url}],
                "Oyentes Mensuales": artist_data.get("followers", {}).get("total", 0),
            }
        })
        print(f"  [ok] {name} — {image_url[:60]}...")
        time.sleep(0.1)

    if updates:
        print(f"\nUpdating {len(updates)} artists in Airtable...")
        n = update_records("Artistas", updates)
        print(f"Updated {n} artists")
    else:
        print("\nNo artists to update")


def fetch_album_covers():
    """Fetch album covers from Spotify and update the Portada field in Airtable."""
    print("Fetching albums from Airtable...")
    albums = list_records("Álbumes", fields=["Título", "Sello", "Portada"])
    print(f"Found {len(albums)} albums\n")

    updates = []
    for record in albums:
        fields = record["fields"]
        title = fields.get("Título", "?")

        # Skip if already has a cover
        if fields.get("Portada"):
            print(f"  [skip] {title} — already has cover")
            continue

        album_data = search_album(title)
        if not album_data:
            print(f"  [skip] {title} — not found on Spotify")
            continue

        image_url = get_best_image(album_data.get("images", []))
        if not image_url:
            print(f"  [skip] {title} — no cover on Spotify")
            continue

        updates.append({
            "id": record["id"],
            "fields": {"Portada": [{"url": image_url}]}
        })
        print(f"  [ok] {title} — {image_url[:60]}...")
        time.sleep(0.1)

    if updates:
        print(f"\nUpdating {len(updates)} albums in Airtable...")
        n = update_records("Álbumes", updates)
        print(f"Updated {n} albums")
    else:
        print("\nNo albums to update")


def fetch_all():
    """Fetch both artist images and album covers."""
    print("=" * 60)
    print("SPOTIFY IMAGE SYNC")
    print("=" * 60)

    print("\n[1/2] Artist photos...")
    fetch_artist_images()

    print("\n[2/2] Album covers...")
    fetch_album_covers()

    print("\n" + "=" * 60)
    print("SYNC COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "all"
    if action == "artists":
        fetch_artist_images()
    elif action == "albums":
        fetch_album_covers()
    else:
        fetch_all()
