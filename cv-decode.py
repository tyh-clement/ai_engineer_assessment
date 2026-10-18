import csv

import requests
from tqdm import tqdm

API_URL = "http://127.0.0.1:8001/asr"
CSV_PATH = "common_voice/cv-valid-dev.csv"
AUDIO_DIR = "common_voice/cv-valid-dev/"  # CSV filenames are relative to this


def transcribe(filename):
    with open(AUDIO_DIR + filename, "rb") as f:
        response = requests.post(API_URL, files={"file": f})
    response.raise_for_status()
    return response.json()["transcription"]


with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    columns = reader.fieldnames + ["generated_text"]
    rows = list(reader)

for row in tqdm(rows):
    row["generated_text"] = transcribe(row["filename"])

with open(CSV_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)
