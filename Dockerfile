FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

ENV GEMINI_API_KEY=1
ENV GEMINI_API_MODEL=gemini-pro
ENV NEO4J_URL=bolt://54.227.205.14:7687
ENV NEO4J_USERNAME=1
ENV NEO4J_PASSWORD=1
ENV MONGODB_HOST=eventure.vayhjdx.mongodb.net
ENV MONGODB_NAME=eventure_ai
ENV MONGODB_USERNAME=1
ENV MONGODB_PASSWORD=1
ENV MONGODB_COLLECTION_NAME_RELATED_EVENT=related_event
ENV MONGODB_INDEX_NAME_RELATED_EVENT=related_event_index

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "5", "--worker-class", "uvicorn.workers.UvicornWorker", "main:app"]
# uvicorn --host 0.0.0.0 --port 8000 main:app
# gunicorn --bind 0.0.0.0:8000 --workers 5 --worker-class uvicorn.workers.UvicornWorker main:app