FROM python:3.11-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    zip \
    vim \
    unzip \
    git \
    curl \
    libpq-dev \ 
    python3-dev \
    && apt-get clean 

COPY ./service /app
COPY docker-env-prod/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt 

ENTRYPOINT ["/app/entrypoint.sh"]

