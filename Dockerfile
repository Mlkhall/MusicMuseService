# Используем официальный образ Python в качестве базового
FROM python:3.12.5

# Устанавливаем зависимости для PostgreSQL и других необходимых библиотек
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости проекта
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=music_muse.settings

ENV DEBUG=true
ENV SECRET_KEY=secret_key
ENV POSTGRESQL_HOST=0.0.0.0
ENV POSTGRESQL_PORT=5432
ENV POSTGRESQL_USER=user
ENV POSTGRESQL_PASSWORD="password"
ENV POSTGRESQL_DBNAME=default

# Открываем порт для приложения
EXPOSE 8000

# Выполняем миграции и собираем статические файлы
RUN poetry run python manage.py migrate \
    && poetry run python manage.py collectstatic --noinput

# Команда для запуска приложения
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]