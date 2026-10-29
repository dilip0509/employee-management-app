FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
COPY tests/ ./tests/
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py db.py ./
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
