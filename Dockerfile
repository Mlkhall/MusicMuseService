# Используем официальный образ Python в качестве базового
FROM python:3.12.5

# Устанавливаем Poetry
RUN pip install -U poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости проекта
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main


# Открываем порт для приложения
EXPOSE 8080

# Выполняем миграции и собираем статические файлы
RUN poetry run python manage.py migrate \
    && poetry run python manage.py collectstatic --noinput

# Команда для запуска приложения
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8080"]