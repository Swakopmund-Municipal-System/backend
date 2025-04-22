FROM python:3.10-slim-bullseye

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

COPY ./app /app

RUN pip install --no-cache-dir -r requirements.txt 

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "run:app"]

