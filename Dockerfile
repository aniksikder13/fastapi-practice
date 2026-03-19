ARG PYTHON_VERSION=3.14

# -------- Builder Stage --------
FROM python:${PYTHON_VERSION}-alpine AS builder

COPY requirements.txt /tmp/

RUN apk add --no-cache \
        postgresql-dev \
        gcc \
        musl-dev && \
    python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /tmp/requirements.txt && \
    apk del gcc musl-dev


# -------- Final Stage --------
FROM python:${PYTHON_VERSION}-alpine AS final

COPY --from=builder /venv /venv

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
        postgresql-libs

ENV PATH="/venv/bin:$PATH"

WORKDIR /app

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]