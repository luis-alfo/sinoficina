"""
Spotify API client using Client Credentials flow.
No user login required — read-only access to public data.
"""

import json
import os
import time
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")

_token_cache = {"token": None, "expires": 0}


def get_token():
    """Get or refresh Spotify access token via Client Credentials."""
    if _token_cache["token"] and time.time() < _token_cache["expires"]:
        return _token_cache["token"]

    if not CLIENT_ID or not CLIENT_SECRET:
        raise RuntimeError("SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set")

    import base64
    creds = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    req = Request("https://accounts.spotify.com/api/token", method="POST",
                  data=b"grant_type=client_credentials",
                  headers={
                      "Authorization": f"Basic {creds}",
                      "Content-Type": "application/x-www-form-urlencoded",
                  })

    with urlopen(req) as resp:
        data = json.loads(resp.read().decode())

    _token_cache["token"] = data["access_token"]
    _token_cache["expires"] = time.time() + data.get("expires_in", 3600) - 60
    return _token_cache["token"]


def spotify_request(url):
    """Make an authenticated GET request to the Spotify API."""
    token = get_token()
    req = Request(url, headers={"Authorization": f"Bearer {token}"})

    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"Spotify API Error: {e.code} {e.reason}\n{body}")
        return None


def get_artist(artist_id):
    """Get artist data by Spotify ID."""
    return spotify_request(f"https://api.spotify.com/v1/artists/{artist_id}")


def get_album(album_id):
    """Get album data by Spotify ID."""
    return spotify_request(f"https://api.spotify.com/v1/albums/{album_id}")


def search_album(query, artist_name=None):
    """Search for an album. Returns the first match."""
    q = query
    if artist_name:
        q = f"album:{query} artist:{artist_name}"
    params = urlencode({"q": q, "type": "album", "limit": 5})
    result = spotify_request(f"https://api.spotify.com/v1/search?{params}")
    if not result:
        return None
    items = result.get("albums", {}).get("items", [])
    return items[0] if items else None


def get_playlist(playlist_id):
    """Get playlist metadata (without paginating all tracks)."""
    fields = "name,description,owner,images,external_urls,public,followers,tracks.total"
    result = spotify_request(
        f"https://api.spotify.com/v1/playlists/{playlist_id}?fields={fields}"
    )
    return result


def search_playlists(query, limit=10):
    """Search for playlists on Spotify."""
    params = urlencode({"q": query, "type": "playlist", "limit": limit})
    result = spotify_request(f"https://api.spotify.com/v1/search?{params}")
    if not result:
        return []
    return result.get("playlists", {}).get("items", [])


def get_user_playlists(user_id, limit=50):
    """Get public playlists from a Spotify user."""
    params = urlencode({"limit": limit})
    result = spotify_request(
        f"https://api.spotify.com/v1/users/{user_id}/playlists?{params}"
    )
    if not result:
        return []
    return result.get("items", [])


def extract_spotify_id(spotify_url):
    """Extract ID from any Spotify URL (artist, playlist, album, track)."""
    if not spotify_url:
        return None
    parts = spotify_url.rstrip("/").split("/")
    return parts[-1].split("?")[0] or None


def extract_artist_id(spotify_url):
    """Extract artist ID from a Spotify URL like https://open.spotify.com/artist/XXXXX."""
    if not spotify_url:
        return None
    parts = spotify_url.rstrip("/").split("/")
    # Handle URLs with query params
    artist_id = parts[-1].split("?")[0]
    return artist_id if len(artist_id) == 22 else None


def get_best_image(images):
    """Get the largest image URL from a Spotify images array."""
    if not images:
        return None
    # Sort by size descending, take largest
    sorted_imgs = sorted(images, key=lambda x: x.get("width", 0), reverse=True)
    return sorted_imgs[0]["url"]
