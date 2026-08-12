FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY elt ./elt
COPY sql ./sql
COPY src ./src
COPY main.py .env.example ./

CMD ["python", "main.py"]

