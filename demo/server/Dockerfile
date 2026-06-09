# DR-Classifier demo backend. Build context = repo root (needs experiments/):
#   docker build -f demo/server/Dockerfile -t dr-demo .
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY server/requirements.txt server/requirements.txt
RUN pip install --no-cache-dir -r server/requirements.txt

# Reused experiments code (preprocessing + models) and the server itself.
COPY experiments/src     /app/experiments/src
COPY experiments/configs /app/experiments/configs
COPY server              /app/server

# experiments/ is added to sys.path by server/app/__init__.py, but exporting it
# here makes `import src.*` work from any entry point too.
ENV PYTHONPATH=/app/experiments:/app

# Checkpoint + norm stats are expected under server/checkpoints/ (bake via LFS
# or mount at runtime). HuggingFace Spaces requires port 7860.
EXPOSE 7860
ENV PORT=7860
CMD ["uvicorn", "server.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
