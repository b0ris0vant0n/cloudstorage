from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from users.models import UserProfile
from rest_framework.test import APIClient
from .models import File


class FileAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, full_name='Test User', email='test@example.com')
        self.client.force_authenticate(user=self.user)

    def test_upload_file(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('upload_file')
        data = {'name': 'testfile.txt', 'path': '/upload/testfile.txt', 'size': 1024, 'mime_type': 'text/plain'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        file = File.objects.get(name='testfile.txt', path='/upload/testfile.txt', size=1024, mime_type='text/plain')
        self.assertEqual(response.json()['file_id'], file.id)

    def test_get_file_list(self):
        self.test_upload_file()
        url = reverse('get_file_list')
        response = self.client.get(url)
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_download_file(self):
        self.test_upload_file()
        file_id = File.objects.get(name='testfile.txt').id
        url = reverse('download_file', args=[file_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rename_file(self):
        self.test_upload_file()
        file_id = File.objects.get(name='testfile.txt').id
        self.client.login(username='testuser', password='testpassword')
        url = reverse('rename_file', args=[file_id])
        data = {'new_name': 'new_testfile.txt'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'File renamed successfully'})

    def test_delete_file(self):
        self.test_upload_file()
        file_id = File.objects.get(name='testfile.txt').id
        self.client.login(username='testuser', password='testpassword')
        url = reverse('delete_file', args=[file_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'File deleted successfully'})
