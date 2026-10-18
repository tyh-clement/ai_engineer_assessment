import io
from dotenv import load_dotenv

import librosa
from fastapi import FastAPI, File, HTTPException, UploadFile

from asr_model import SAMPLE_RATE, ASRModel

app = FastAPI()
model = ASRModel()


@app.get("/ping")
def ping():
    return "pong"


@app.post("/asr")
async def asr(file: UploadFile = File(...)):
    data = await file.read()
    try:
        audio, _ = librosa.load(io.BytesIO(data), sr=SAMPLE_RATE, mono=True)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not decode audio file")

    return {
        "transcription": model.transcribe(audio),
        "duration": str(round(len(audio) / SAMPLE_RATE, 1)),
    }