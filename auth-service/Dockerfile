FROM python:3.13-slim as builder

ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONHASHSEED=random
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_VERSION=2.1.1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-root --no-interaction --no-ansi --only main


FROM python:3.13-slim as runtime

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

RUN useradd -m swakopmund_marine

WORKDIR /app

RUN chown swakopmund_marine:swakopmund_marine /app

USER swakopmund_marine

COPY --chown=swakopmund_marine:swakopmund_marine . .

EXPOSE 9080

CMD ["daphne", "-b", "0.0.0.0", "-p",  "9080", "authservice.asgi:application" ]