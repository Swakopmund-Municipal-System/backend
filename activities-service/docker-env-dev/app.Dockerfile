FROM python:3.10-slim-bullseye

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


WORKDIR /app

CMD tail -f /dev/null

