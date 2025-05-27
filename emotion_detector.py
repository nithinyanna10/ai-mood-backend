from deepface import DeepFace
import tempfile
from fastapi import UploadFile
from PIL import Image
import numpy as np

def detect_emotion(file: UploadFile) -> str:
    # Save the uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        contents = file.file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    # Run DeepFace analysis
    try:
        result = DeepFace.analyze(img_path=tmp_path, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
    except Exception as e:
        print(f"DeepFace error: {e}")
        emotion = "neutral"

    return emotion.lower()
