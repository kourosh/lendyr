FROM python:3.11-slim

# System deps required by ibm_db
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2 \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY db.py .
COPY data/ ./data/
COPY routers/ ./routers/

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
