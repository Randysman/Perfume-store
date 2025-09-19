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

RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'set -e' >> /entrypoint.sh && \
    echo 'echo "Applying migrations"' >> /entrypoint.sh && \
    echo 'python manage.py migrate --noinput' >> /entrypoint.sh && \
    echo 'echo "Collecting static files"' >> /entrypoint.sh && \
    echo 'python manage.py collectstatic --noinput --clear' >> /entrypoint.sh && \
    echo 'exec "$@"' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

USER djangouser

ENTRYPOINT [ "/entrypoint.sh" ]

CMD ["gunicorn", "shop.wsgi:application", "--bind", "0.0.0.0:8000"]