ENV фалйы специально запушил на GIT.


# TODO Monitoring Project

Полный стек с Prometheus + Grafana для мониторинга Django backend, Nginx и Postgres.

http://localhost:8080/
---

## Сборка и запуск проекта

```bash
# Собрать контейнеры
docker compose build

# Запустить проект с двумя репликами backend
docker compose up -d --scale backend=2
```

---

## Prometheus

Prometheus сам по себе — просто сборщик метрик.  
Чтобы он мог собирать данные, **Nginx**, **Postgres** и **Django** должны отдавать метрики в формате Prometheus.

Если сервис (например, Nginx или Postgres) не умеет отдавать метрики напрямую — используется **exporter**, отдельный контейнер, который «переводит» данные в формат Prometheus.

## Интерфейс Prometheus UI

```bash
# Проверка здоровья/готовности
curl -s http://localhost:9090/-/healthy
curl -s http://localhost:9090/-/ready
```

Открой в браузере:
[http://localhost:9090/targets](http://localhost:9090/targets)

**Должны быть видны job'ы:**  
`django`, `nginx`, `postgres` — и все они должны быть **UP**.

---

## Grafana

Интерфейс: [http://localhost:3000](http://localhost:3000)

**Login / Password:**  
```
admin / admin
```

## Дашборд "TODO Monitoring"

Grafana показывает на дашборде следующие метрики:

- Количество активных реплик backend  
- Состояние (UP/DOWN) каждой реплики backend  
- Доступность Postgres  
- Доступность Nginx  
- Количество активных соединений в Nginx  
- Количество подключений к базе данных  
- Работает ли экспортер Nginx  
- Работает ли экспортер Postgres

Перейти к дашбордам можно по адресу:  
[http://localhost:3000/dashboards](http://localhost:3000/dashboards)

---

## Unit-тесты для Django REST API

Для запуска тестов:

```bash
docker compose run --rm backend python manage.py test
```
---

© 2025 TODO Monitoring Stack — DevOps Observability Example