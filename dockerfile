FROM python:3.10.11

RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

ENV  SECRET_KEY afasfssegasgcgeges
ENV  DEBUG 0
ENV  DB_ENGINE django.db.backends.sqlite3
ENV  DB_NAME db_sqlite3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD service nginx start && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic && \
    gunicorn stocks_products.wsgi:application --bind 0.0.0.0:8000