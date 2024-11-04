from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.list_url = reverse('task-list')
        self.task1 = Task.objects.create(title='Tâche 1', description='Description 1')
        self.task2 = Task.objects.create(title='Tâche 2', description='Description 2', is_completed=True)

    def test_create_task(self):
        data = {'title': 'Nouvelle Tâche', 'description': 'Nouvelle Description'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(Task.objects.get(id=response.data['id']).title, 'Nouvelle Tâche')

    def test_get_task_list(self):
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_task(self):
        data = {'title': 'Tâche 1 Modifiée', 'description': 'Description Modifiée', 'is_completed': True}
        response = self.client.put(reverse('task-detail', kwargs={'pk': self.task1.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Tâche 1 Modifiée')
        self.assertTrue(self.task1.is_completed)

    def test_delete_task(self):
        response = self.client.delete(reverse('task-detail', kwargs={'pk': self.task1.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)
