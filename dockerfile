FROM python:3.11-alpine
RUN apk add --no-cache \
    python3-dev

RUN addgroup -S djangogroup && adduser -S djangouser -G djangogroup

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


COPY --chown=djangouser:djangogroup . .

RUN chmod +x entrypoint.sh

USER djangouser

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD ["gunicorn", "django_project.wsgi:application", "--bind", "0.0.0.0:8000"]