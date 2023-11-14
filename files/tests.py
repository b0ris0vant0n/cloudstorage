from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import File, UserProfile
from unittest.mock import patch
from .serializers import FileSerializer
from unittest.mock import patch

class FileAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_user_files(self):
        url = reverse('get_user_files')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_file(self):
        url = reverse('upload_file')
        data = {
            'name': 'testfile.txt',
            'size': 1024,
            'mime_type': 'text/plain',
            'path': '/upload/testfile.txt',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.json())
        self.assertIn('file_id', response.json())


    def test_rename_file(self):
        file = File.objects.create(
            user_profile=self.user_profile,
            name='testfile.txt',
            size=1024,
            mime_type='text/plain',
            storage_path='/upload/testfile.txt',
        )
        url = reverse('rename_file', args=[file.id])
        new_name = 'renamed_file.txt'
        data = {'new_name': new_name}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.json())
        file.refresh_from_db()
        self.assertEqual(file.name, new_name)

    def test_update_comment_file(self):
        file = File.objects.create(
            user_profile=self.user_profile,
            name='testfile.txt',
            size=1024,
            mime_type='text/plain',
            storage_path='/upload/testfile.txt',
            comment='some comments'
        )
        url = reverse('update_comment', args=[file.id])
        new_comment = 'new comment'
        data = {'new_comment': new_comment}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.json())
        file.refresh_from_db()
        self.assertEqual(file.comment, new_comment)

    def test_delete_file(self):
        file = File.objects.create(
            user_profile=self.user_profile,
            name='testfile.txt',
            size=1024,
            mime_type='text/plain',
            storage_path='/upload/testfile.txt',
        )
        url = reverse('delete_file', args=[file.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.json())
        with self.assertRaises(File.DoesNotExist):
            file.refresh_from_db()
