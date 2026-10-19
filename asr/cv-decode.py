import csv
from pathlib import Path

import requests
from tqdm import tqdm

API_URL = "http://127.0.0.1:8001/asr"
HERE = Path(__file__).parent  # paths below work from any working directory
CSV_PATH = HERE / "common_voice" / "cv-valid-dev.csv"
AUDIO_DIR = HERE / "common_voice" / "cv-valid-dev"  # CSV filenames are relative to this


def transcribe(filename):
    with open(AUDIO_DIR / filename, "rb") as f:
        response = requests.post(API_URL, files={"file": f})
    response.raise_for_status()
    result = response.json()
    return result["transcription"], result["duration"]


with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    columns = reader.fieldnames
    if "generated_text" not in columns:
        columns.append("generated_text")
    rows = list(reader)

for row in tqdm(rows):
    row["generated_text"], row["duration"] = transcribe(row["filename"])

with open(CSV_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)
