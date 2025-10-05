# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install deps
COPY pyproject.toml poetry.lock* /app/
RUN pip install --upgrade pip \
&& pip install poetry \
&& poetry config virtualenvs.create false \
&& poetry install --no-dev --no-interaction --no-ansi
COPY . /app
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]