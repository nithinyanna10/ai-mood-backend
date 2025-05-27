
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

# Spotify auth setup
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

# Mood to search term mapping
MOOD_TO_SPOTIFY_QUERY = {
    "happy": "feel good",
    "hype": "party",
    "sad": "sad songs",
    "chill": "lofi",
    "dark": "moody",
    "neutral": "ambient"
}

# Mood to audio profile expectations
MOOD_AUDIO_FILTERS = {
    "happy": {"min_valence": 0.6, "min_energy": 0.4},
    "hype": {"min_valence": 0.6, "min_energy": 0.7},
    "sad": {"max_valence": 0.4},
    "chill": {"max_energy": 0.5},
    "dark": {"max_valence": 0.4, "max_energy": 0.6},
    "neutral": {}
}

def get_tracks_for_mood(mood: str):
    try:
        query = MOOD_TO_SPOTIFY_QUERY.get(mood.lower(), "mood")
        results = sp.search(q=query, type="track", limit=10)
        tracks = []

        for item in results["tracks"]["items"]:
            track_info = {
                "title": item["name"],
                "artist": item["artists"][0]["name"],
                "album_image": item["album"]["images"][0]["url"] if item["album"]["images"] else "",
                "preview_url": item["preview_url"],
                "external_url": item["external_urls"]["spotify"]
            }
            tracks.append(track_info)

        return tracks

    except Exception as e:
        print(f"Spotify API error: {e}")
        return []
