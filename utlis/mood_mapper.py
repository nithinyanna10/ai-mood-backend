import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

# Initialize Spotipy client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

# Mood → Spotify query mapping
MOOD_TO_SPOTIFY_QUERY = {
    "happy": "feel good",
    "hype": "workout",
    "sad": "sad songs",
    "chill": "lofi chill",
    "dark": "deep focus",
    "neutral": "ambient"
}

# Helper function if used elsewhere
def map_emotion_to_query(mood: str) -> str:
    return MOOD_TO_SPOTIFY_QUERY.get(mood.lower(), "mood")

# Main playlist fetch function
def get_playlists_for_mood(mood: str):
    try:
        query = map_emotion_to_query(mood)  # cleaner
        results = sp.search(q=query, type="playlist", limit=5)
        raw_items = results.get("playlists", {}).get("items", [])
        playlists = []

        for item in raw_items:
            if item is None:
                continue
            playlists.append({
                "name": item.get("name", "Untitled"),
                "url": item.get("external_urls", {}).get("spotify", "#"),
                "image": item.get("images", [{}])[0].get("url", ""),
                "description": item.get("description", "")
            })

        return playlists

    except Exception as e:
        print(f"Spotify API error: {e}")
        return []
