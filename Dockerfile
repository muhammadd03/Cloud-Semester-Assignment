FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps if needed (e.g. psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Collect static (optional, if you use static files)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run migrations then start gunicorn
CMD ["bash", "-c", "python manage.py migrate && gunicorn mysite.wsgi:application --bind 0.0.0.0:8000"]
