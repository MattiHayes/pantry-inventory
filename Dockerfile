FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

RUN groupadd --system --gid 10001 pantry \
    && useradd --system --uid 10001 --gid pantry --no-create-home pantry \
    && mkdir -p /data \
    && chown pantry:pantry /data

USER pantry
WORKDIR /data

EXPOSE 5000

CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "--call", "src.app:create_app"]
