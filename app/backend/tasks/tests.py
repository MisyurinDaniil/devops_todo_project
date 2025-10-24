"""
Тесты для REST API эндпоинтов модели Task.

Используется Django REST Framework (DRF) и его тестовый клиент.
Проверяется корректность CRUD-операций, сериализации и сортировки задач.

Структура API задаётся во views.py:
    class TaskViewSet(ModelViewSet):
        queryset = Task.objects.all().order_by('-created_at')
        serializer_class = TaskSerializer

Router (urls.py) автоматически создаёт два основных маршрута:
    /api/tasks/        — список задач + создание (list, create)
    /api/tasks/<id>/   — отдельная задача (retrieve, update, delete)
"""

from rest_framework.test import APITestCase
from django.urls import reverse
from tasks.models import Task


class TaskAPITests(APITestCase):
    """
    Тесты API для модели Task.
    """

    def test_list_returns_tasks_ordered_by_created_at_desc(self):
        """
        Проверяем, что эндпоинт /api/tasks/:
          1. Возвращает код 200 (OK)
          2. Отдаёт задачи в порядке убывания created_at (новые первыми)
          3. Содержит ожидаемые поля сериализатора
        """

        # Создаём две задачи с разным временем создания
        first = Task.objects.create(title="older task")
        second = Task.objects.create(title="newer task")

        # Получаем URL для списка задач (task-list — имя, заданное DRF router'ом)
        url = reverse('task-list')

        # Делаем GET-запрос к /api/tasks/
        response = self.client.get(url)

        # Проверяем, что запрос успешен
        self.assertEqual(response.status_code, 200, "Ожидался статус 200 OK")

        # Ответ должен быть в JSON-формате: список словарей
        data = response.json()

        # Убеждаемся, что вернулись обе задачи
        self.assertEqual(len(data), 2, "Ожидались две задачи в ответе")

        # Проверяем порядок — сначала должна идти более новая задача
        returned_titles = [item["title"] for item in data]
        self.assertEqual(
            returned_titles,
            ["newer task", "older task"],
            "Список задач должен сортироваться по created_at убыванию",
        )

        # Проверяем, что сериализатор возвращает нужные поля
        expected_fields = {"id", "title", "description", "completed", "created_at"}
        self.assertTrue(
            expected_fields.issubset(data[0].keys()),
            f"Ожидались поля {expected_fields} в ответе",
        )

    def test_create_task_via_post(self):
        """
        Проверяем, что POST-запрос на /api/tasks/ создаёт новую задачу.

        Ожидаем:
          - статус 201 Created
          - данные новой задачи в ответе
          - запись реально создаётся в базе
        """

        url = reverse('task-list')

        # JSON-данные для создания задачи
        payload = {
            "title": "Do homework",
            "description": "math + english"
        }

        # Выполняем POST-запрос
        response = self.client.post(url, payload, format='json')

        # Проверяем, что API ответило 201 (Created)
        self.assertEqual(
            response.status_code, 201,
            f"Ожидался статус 201, получено {response.status_code}"
        )

        # Проверяем, что задача реально добавлена в БД
        self.assertEqual(Task.objects.count(), 1, "Ожидалась одна созданная задача")

        task = Task.objects.first()
        self.assertEqual(task.title, payload["title"])
        self.assertEqual(task.description, payload["description"])
        self.assertFalse(task.completed, "completed должен быть False по умолчанию")

        # Проверяем содержимое JSON-ответа
        body = response.json()
        self.assertEqual(body["title"], payload["title"])
        self.assertEqual(body["description"], payload["description"])
        self.assertFalse(body["completed"])
        self.assertIn("id", body)
        self.assertIn("created_at", body)

    def test_retrieve_single_task(self):
        """
        Проверяем, что GET /api/tasks/<id>/ возвращает конкретную задачу.
        """

        task = Task.objects.create(title="Check details", description="verify GET detail")

        # Формируем URL вида /api/tasks/<id>/
        url = reverse('task-detail', args=[task.id])
        response = self.client.get(url)

        # Проверяем статус
        self.assertEqual(response.status_code, 200, "GET detail должен вернуть 200 OK")

        data = response.json()

        # Проверяем корректность данных
        self.assertEqual(data["id"], task.id)
        self.assertEqual(data["title"], task.title)
        self.assertEqual(data["description"], task.description)

    def test_patch_task_completed(self):
        """
        Проверяем частичное обновление (PATCH) задачи:
          - поле completed можно изменить
          - обновление возвращает новые данные
        """

        task = Task.objects.create(title="Mark me done")

        url = reverse('task-detail', args=[task.id])
        response = self.client.patch(url, {"completed": True}, format="json")

        # PATCH должен вернуть 200 OK
        self.assertEqual(response.status_code, 200)

        # Обновляем объект из базы
        task.refresh_from_db()

        # Проверяем, что completed теперь True
        self.assertTrue(task.completed, "Поле completed не обновилось")

        # Проверяем, что API тоже вернул обновлённые данные
        data = response.json()
        self.assertTrue(data["completed"])

    def test_delete_task(self):
        """
        Проверяем удаление задачи через DELETE /api/tasks/<id>/.
        """

        task = Task.objects.create(title="To be deleted")

        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url)

        # Удаление должно вернуть 204 No Content
        self.assertEqual(response.status_code, 204, "DELETE должен вернуть 204")

        # Убеждаемся, что запись удалена
        self.assertEqual(Task.objects.count(), 0, "Задача должна быть удалена из БД")
