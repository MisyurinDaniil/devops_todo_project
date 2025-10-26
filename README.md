## TODO Project

---

## Сборка и запуск проекта

```bash
# Собрать проект
docker compose build

# Запустить проект с двумя репликами backend
docker compose up -d --scale backend=2
```

Frontend проекта доступен по адресу:

[http://localhost:8080/]

---

## Prometheus UI

```bash
# Проверка здоровья/готовности
curl -s http://localhost:9090/-/healthy
curl -s http://localhost:9090/-/ready
```

Открой в браузере:
[http://localhost:9090/targets]

**Должны быть видны job'ы:**  
`django`, `nginx`, `postgres` — и все они должны быть **UP**.

Prometheus сам по себе — просто сборщик метрик.  
Чтобы он мог собирать данные, **Nginx**, **Postgres** и **Django** должны отдавать метрики в формате Prometheus.

Если сервис (например, Nginx или Postgres) не умеет отдавать метрики напрямую — используется **exporter**, отдельный контейнер, который «переводит» данные в формат Prometheus.

---

## Grafana

Перейти к дашбордам можно по адресу:  
[http://localhost:3000/dashboards]

**Login / Password:**  
```
admin / admin
```

## Дашборд "TODO"

Grafana показывает на дашборде следующие метрики:

- Количество активных реплик backend  
- Состояние (UP/DOWN) каждой реплики backend  
- Доступность Postgres  
- Доступность Nginx  
- Количество активных соединений в Nginx  
- Количество подключений к базе данных  
- Работает ли экспортер Nginx  
- Работает ли экспортер Postgres

---

## Unit-тесты для Django REST API

Для запуска тестов:

```bash
docker compose run --rm backend python manage.py test
```
---

## Backup Postgres

```bash
docker compose exec db sh -c \
  'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > /backups/backup_$(date +%Y-%m-%d_%H-%M-%S).sql'
```
## Restore Postgres

# Остановить backend (чтобы не было коннектов)
```bash
docker compose stop backend
```

# Зайти в контейнер Postgres и пересоздать БД
```bash
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -c "DROP DATABASE IF EXISTS \"$POSTGRES_DB\";"'
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -c "CREATE DATABASE \"$POSTGRES_DB\" OWNER \"$POSTGRES_USER\";"'
```

# Восстановить дамп
```bash
docker compose exec db sh -c \
  'psql -U "$POSTGRES_USER" "$POSTGRES_DB" < /backups/backup_2025-10-26_19-32-10.sql'
```

# Запускаем обратно backend
```bash
docker compose start backend
```


© 2025 TODO — DevOps Observability Example