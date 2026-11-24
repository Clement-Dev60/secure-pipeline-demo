FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_PATH=/data/items.db

WORKDIR /app

COPY requirements.txt .
# pip n'est utile qu'à l'installation : on le retire de l'image finale
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y pip

COPY app.py .

RUN useradd --system --uid 10001 --no-create-home appuser \
    && mkdir /data \
    && chown appuser /data
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:create_app()"]
