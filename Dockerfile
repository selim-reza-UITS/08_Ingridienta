FROM python:3.11.13-slim-bullseye

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (including Redis server)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose the port you want the app to run on
EXPOSE 8000

CMD /bin/bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && \
    python manage.py runserver 0.0.0.0:8000"