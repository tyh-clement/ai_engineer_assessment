# ai_engineer_assessment

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Download the model

The API only loads the model from disk and never downloads it. Download it once first:

```bash
python asr/download_model.py
```

The model is stored in `<base>/wav2vec2-large-960h`. The base directory defaults to `asr/models/`; change it with `--model-dir` or the `MODEL_DIR` env var (e.g. in `.env`). The API reads the same `MODEL_DIR`, so set it consistently:

```bash
python asr/download_model.py --model-dir /path/to/models
MODEL_DIR=/path/to/models fastapi dev asr/asr_api.py --port 8001
```

## Run the API

With the virtual environment activated, start the FastAPI development server:

```bash
fastapi dev asr/asr_api.py --port 8001
```

## Transcribe Common Voice (cv-decode.py)

With the API running on port 8001, transcribe every file listed in `common_voice/cv-valid-dev.csv`:

```bash
python cv-decode.py
```

This adds a `generated_text` column and saves it back to `common_voice/cv-valid-dev.csv`. The file is only written after all files are transcribed. Edit the constants at the top of the script to change the API URL or paths.
