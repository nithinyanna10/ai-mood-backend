from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from emotion_detector import detect_emotion
from mood_enhancer import analyze_text_mood
from spotify_api import get_tracks_for_mood

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in prod
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
    tracks: List[Track]

@app.post("/predict", response_model=MoodResponse)
async def predict_mood(
    file: UploadFile = File(...),
    text: Optional[str] = Form(None)
):
    print("🔁 /predict called")

    emotion = detect_emotion(file)
    text_mood = analyze_text_mood(text) if text else None
    mood = text_mood or emotion

    tracks = get_tracks_for_mood(mood)

    print("✅ Mood:", mood)
    print("🎧 Tracks found:", len(tracks))

    return {
        "mood": mood,
        "emotion": emotion,
        "tracks": tracks
    }

# Optional local run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
