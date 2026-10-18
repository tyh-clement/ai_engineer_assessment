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

## Run the API

With the virtual environment activated, start the FastAPI development server:

```bash
fastapi dev asr/asr_api.py --port 8001
```
