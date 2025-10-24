# tasks/tests/test_integration_api.py
from rest_framework.test import APITestCase
from django.db import connection
from tasks.models import Task

class IntegrationTaskAPITests(APITestCase):
    def test_create_and_retrieve_task(self):
        # 1. Создаём задачу через API (эмулируем реальный HTTP-запрос)
        response = self.client.post("/api/tasks/", {"title": "Integration check"}, format="json")
        self.assertEqual(response.status_code, 201)

        # 2. Проверяем, что она реально попала в базу данных
        self.assertTrue(Task.objects.filter(title="Integration check").exists())

        # 3. Проверяем, что её можно получить обратно через API
        get_response = self.client.get("/api/tasks/")
        data = get_response.json()
        titles = [item["title"] for item in data]
        self.assertIn("Integration check", titles)

        # 4. Проверяем, что соединение с базой активно
        self.assertTrue(connection.ensure_connection)
