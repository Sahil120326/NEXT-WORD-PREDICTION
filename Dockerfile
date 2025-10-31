# Containerize the Flask app for deployment
FROM python:3.11-slim AS base

WORKDIR /app

# Faster installs: avoid bytecode and pip cache
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps (optional, minimal)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Port is provided by platform; default to 8080 for local runs
ENV PORT=8080
EXPOSE 8080

# Start with gunicorn (2 workers, threads for light concurrency)
CMD ["sh", "-c", "gunicorn -w 2 -k gthread -b 0.0.0.0:${PORT} app:app"]