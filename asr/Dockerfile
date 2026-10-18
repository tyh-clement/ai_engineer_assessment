FROM python:3.12-slim

ENV PIP_ROOT_USER_ACTION=ignore \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.asr.txt .
RUN pip install --no-cache-dir -r requirements.asr.txt

COPY asr_api.py asr_model.py ./

# The model is not baked into the image; mount it at /models (see docker-compose.yml)
ENV MODEL_DIR=/models

EXPOSE 8001

CMD ["fastapi", "run", "asr_api.py", "--host", "0.0.0.0", "--port", "8001"]
