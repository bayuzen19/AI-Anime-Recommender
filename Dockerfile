FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/list/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFER=1

EXPOSE 8000
EXPOSE 8501

CMD ["uvicorn","api.main:app","--host","0.0.0.0","--port","8000"]
