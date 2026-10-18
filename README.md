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

The model is stored in `<base>/wav2vec2-large-960h`. The base directory defaults to `models/` in the repo root; change it with `--model-dir` or the `MODEL_DIR` env var (e.g. in `.env`). The API reads the same `MODEL_DIR`, so set it consistently:

```bash
python asr/download_model.py --model-dir /path/to/models
MODEL_DIR=/path/to/models fastapi dev asr/asr_api.py --port 8001
```

## Run the API

With the virtual environment activated, start the FastAPI development server:

```bash
fastapi dev asr/asr_api.py --port 8001
```
