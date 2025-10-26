
# При многоступенчатой сборке финальный образ изменил размер с 129MB до 112MB

###########################################################
# ===== STAGE 1: Builder =====
# На этом этапе мы собираем зависимости и создаём .whl-файлы.
# В финальный образ этот слой не попадёт — только его результат.
###########################################################
FROM python:3.11-alpine AS builder

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /build

# Копируем файл зависимостей (только его — чтобы кэш сборки не сбрасывался при изменении кода)
COPY app/backend/requirements.txt .

# Обновляем pip и собираем wheel-файлы (готовые бинарные пакеты)
# - pip wheel — компилирует зависимости в .whl, не устанавливая их
# - --no-cache-dir — не сохраняем кэш (экономим место)
# - --no-deps — берём зависимости только из requirements.txt (без автоподстановок)
# - -w /wheels — сохраняем результат в папку /wheels
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir -r requirements.txt -w /wheels

###########################################################
# ===== STAGE 2: Runtime =====
# Это финальный, минимальный образ. Здесь нет временных файлов.
# В нём только Python, зависимости и исходный код проекта.
###########################################################
FROM python:3.11-alpine

# Рабочая директория приложения внутри контейнера
WORKDIR /app

# Создаём отдельного пользователя для приложения
RUN addgroup -S app && adduser -S app -G app

# Переменные окружения:
# - PYTHONDONTWRITEBYTECODE=1  — не создавать *.pyc файлы (экономим место)
# - PYTHONUNBUFFERED=1         — вывод сразу идёт в stdout/stderr (важно для логов)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Копируем из builder stage только собранные wheel-файлы (готовые зависимости)
COPY --from=builder /wheels /wheels

# перенесём requirements.txt в /app
COPY app/backend/requirements.txt .

# Устанавливаем зависимости из wheel-файлов и удаляем временную папку
# RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
&& rm -rf /wheels

# Копируем код и даём пользователю права на него
COPY app/backend/ .
RUN chown -R app:app /app

# Переключаемся на нового пользователя
USER app

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Команда по умолчанию при запуске контейнера:
# - применяем миграции БД
# - запускаем dev-сервер Django (в продакшне заменяется на gunicorn/uvicorn)
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
