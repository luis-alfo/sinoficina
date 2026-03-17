"""
Sync Warner Music playlists from Spotify to the Airtable Playlists table.

Sources:
  - Warner Music official Spotify profiles
  - Search for key Warner/Atlantic/Elektra playlists

Each playlist gets: name, description, cover, creator, track count,
follower count, and dates.
"""

import sys
import time
from airtable_client import list_records, create_records, update_records
from spotify_client import (
    get_playlist, search_playlists, get_user_playlists,
    get_best_image, extract_spotify_id,
)

# Warner Music Spotify user IDs and curated playlist IDs
WARNER_PROFILES = [
    "wmg_lobby",                    # Warner Music Group (official)
    "warnerrecordsofficial",        # Warner Records
    "warnermusicnashville",         # Warner Records Nashville
    "warner.music.central.europe",  # Warner Music Central Europe
    "atlanticrecords",              # Atlantic Records
    "nonesuchrecords",              # Nonesuch Records
]

# Known Warner Music / subsidiary playlist IDs (verified from Spotify)
KNOWN_PLAYLIST_IDS = [
    "4G8YMEnXpljdSERHuKCbxD",  # Now Playing at Warner Records
    "3d4GqpwBY7JJ0sipGzpuhy",  # Soundrop — Warner Records
    "7AD9l3ss4fOiXHeMWEdtVa",  # Eric Clapton Discography — Warner Records
    "51nLCHXyNwAn9SZfFPyXYD",  # Welcome Back + Top Songs — Warner Records
    "6r5va1sKbfAaUXsi1qzVmR",  # NMF — Warner Music Group
    "5pELxwpjobVQmsYjCt6BTI",  # Warner Music Group
    "1vNxw7TgapvufJqj35Dafd",  # New Warner Music
    "0TJY4WN5dmKpbSZf77VAJe",  # Warner Music Greatest Hits — Topsify UK
    "4sjY92ZWVdLJYdPmhpJQXh",  # Atlantic Records: Presents
    "1HyGbAS20bjdtBGBTO5YlO",  # SCOOB! Soundtrack — Atlantic Records
    "4EMqp0WlIjXtzl8Df4FhNM",  # Wake Up! It's The Holidays — Atlantic Records
    "6dxtJsxSK9zpAPjf473CJz",  # Ultimate EDM Playlist — Atlantic Records
    "4IpYGUkrEXL7C8dWYFBEKo",  # Atlantic Records Celebrates: Black Music Month
    "3wJXF52EXPj8EL583RCqp4",  # New Music from Elektra — Elektra Records
    "4ywfF9SyZgVY8Mr8ZFlZB9",  # CABRA: Creator Collection — Warner Chappell Music
]

# Search queries to find Warner-related playlists
SEARCH_QUERIES = [
    "Warner Music",
    "Warner Records",
    "Atlantic Records",
    "Elektra Records",
    "Warner Music Latin",
    "Parlophone Records",
    "Nonesuch Records",
    "Warner Chappell",
]


def get_existing_playlists():
    """Get existing playlist names from Airtable to avoid duplicates."""
    records = list_records("Playlists", fields=["Nombre", "Spotify URL"])
    existing = {}
    for r in records:
        name = r["fields"].get("Nombre", "")
        url = r["fields"].get("Spotify URL", "")
        if name:
            existing[name.lower()] = r
        if url:
            pid = extract_spotify_id(url)
            if pid:
                existing[pid] = r
    return existing


def playlist_to_airtable(playlist_data):
    """Convert Spotify playlist data to Airtable fields."""
    tracks = playlist_data.get("tracks", {})
    total_tracks = tracks.get("total", 0)

    # Calculate total duration from track items
    total_duration_s = 0
    for item in tracks.get("items", []):
        track = item.get("track")
        if track and track.get("duration_ms"):
            total_duration_s += track["duration_ms"] // 1000

    owner = playlist_data.get("owner", {})
    image_url = get_best_image(playlist_data.get("images", []))
    spotify_url = playlist_data.get("external_urls", {}).get("spotify", "")

    fields = {
        "Nombre": playlist_data.get("name", "Sin nombre"),
        "Descripción": playlist_data.get("description", "") or "",
        "Creador": owner.get("display_name", owner.get("id", "")),
        "Pública": playlist_data.get("public", False) or False,
        "Seguidores": playlist_data.get("followers", {}).get("total", 0),
    }

    if image_url:
        fields["Portada"] = [{"url": image_url}]

    if total_duration_s > 0:
        fields["Duración Total"] = total_duration_s

    if spotify_url:
        fields["Spotify URL"] = spotify_url

    return fields


def collect_playlist_ids():
    """Collect playlist IDs from profiles and search."""
    playlist_ids = set()

    # 1. From known IDs
    for pid in KNOWN_PLAYLIST_IDS:
        playlist_ids.add(pid)

    # 2. From Warner user profiles
    for user_id in WARNER_PROFILES:
        print(f"  Fetching playlists from user: {user_id}")
        playlists = get_user_playlists(user_id)
        for p in playlists:
            if p and p.get("id"):
                playlist_ids.add(p["id"])
        print(f"    Found {len(playlists)} playlists")
        time.sleep(0.2)

    # 3. From search
    for query in SEARCH_QUERIES:
        print(f"  Searching: '{query}'")
        results = search_playlists(query, limit=5)
        for p in results:
            if p and p.get("id"):
                playlist_ids.add(p["id"])
        print(f"    Found {len(results)} results")
        time.sleep(0.2)

    return playlist_ids


def sync_playlists():
    """Main sync: fetch Warner playlists from Spotify and push to Airtable."""
    print("=" * 60)
    print("WARNER MUSIC PLAYLIST SYNC")
    print("=" * 60)

    # Get existing playlists to avoid duplicates
    existing = get_existing_playlists()
    print(f"Existing playlists in Airtable: {len(existing)}\n")

    # Collect all playlist IDs
    print("Collecting playlist IDs...")
    playlist_ids = collect_playlist_ids()
    print(f"\nTotal unique playlists found: {len(playlist_ids)}\n")

    # Fetch full data and prepare records
    new_records = []
    updates = []

    for pid in playlist_ids:
        data = get_playlist(pid)
        if not data:
            print(f"  [fail] {pid} — could not fetch")
            continue

        name = data.get("name", "?")
        fields = playlist_to_airtable(data)

        # Check if already exists
        existing_record = existing.get(name.lower()) or existing.get(pid)
        if existing_record:
            # Update with fresh data (followers, duration, etc.)
            updates.append({
                "id": existing_record["id"],
                "fields": {k: v for k, v in fields.items() if k != "Nombre"},
            })
            print(f"  [update] {name}")
        else:
            new_records.append(fields)
            print(f"  [new] {name}")

        time.sleep(0.15)

    # Push to Airtable
    if new_records:
        print(f"\nCreating {len(new_records)} new playlists...")
        n = create_records("Playlists", new_records)
        print(f"Created {n} playlists")

    if updates:
        print(f"\nUpdating {len(updates)} existing playlists...")
        n = update_records("Playlists", updates)
        print(f"Updated {n} playlists")

    if not new_records and not updates:
        print("\nNo changes needed")

    print("\n" + "=" * 60)
    print("SYNC COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    sync_playlists()
