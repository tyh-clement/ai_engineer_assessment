FROM python:3.12-slim
RUN pip install --no-cache-dir "elasticsearch>=8,<9"
COPY cv-index.py .
CMD ["python", "cv-index.py"]