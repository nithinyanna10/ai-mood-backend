from pydantic import BaseModel
from typing import List, Optional

class Playlist(BaseModel):
    name: str
    url: str
    image: Optional[str]
    description: Optional[str]

class MoodResponse(BaseModel):
    mood: str
    emotion: str
    playlists: List[Playlist]
