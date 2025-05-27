from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict

from emotion_detector import detect_emotion
from mood_enhancer import analyze_text_mood
from spotify_api import get_tracks_for_mood

app = FastAPI()

# Enable CORS for frontend (adjust origin for production!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Track(BaseModel):
    title: str
    artist: str
    album_image: Optional[str]
    preview_url: Optional[str]
    external_url: str

class MoodResponse(BaseModel):
    mood: str
    emotion: str
    tracks: List[Track]  # ✅ Fixed field name and type

@app.post("/predict", response_model=MoodResponse)
async def predict_mood(
    file: UploadFile = File(...),
    text: Optional[str] = Form(None)
):
    print("🔁 Received /predict request")

    emotion = detect_emotion(file)
    text_mood = analyze_text_mood(text) if text else None

    # Choose best mood
    mood = text_mood or emotion

    tracks = get_tracks_for_mood(mood)

    print("✅ Returning mood:", mood)
    print("🎵 Tracks:", len(tracks))

    return {
        "mood": mood,
        "emotion": emotion,
        "tracks": tracks  # ✅ renamed from 'playlists'
    }
