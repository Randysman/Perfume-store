FROM python:3.11-alpine
RUN apk add --no-cache \
    python3-dev \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    linux-headers \
    bash

RUN addgroup -S djangogroup && adduser -S djangouser -G djangogroup

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=djangouser:djangogroup . .

RUN chmod +x entrypoint.sh

USER djangouser

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD ["gunicorn", "django_project.wsgi:application", "--bind", "0.0.0.0:8000"]