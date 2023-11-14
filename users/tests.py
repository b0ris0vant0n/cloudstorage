from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
import json

from users.models import UserProfile


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True)

    def test_register_user(self):
        data = {
            'user': {
                'username': 'newuser',
                'password': 'newpassword',
                'email': 'newuser@example.com'
            },
            'full_name': 'New User',
            'is_admin': False,
            'storage_path': '/new/path/',
            "email": "a@gmail.com"
        }
        url = reverse('register_user')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_user_list(self):
        url = reverse('get_user_list')
        self.client.force_login(self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        user_to_delete = User.objects.create_user(username='todelete', password='todeletepassword')
        user_profile_to_delete = UserProfile.objects.create(user=user_to_delete, full_name='Full Name',
                                                            email='email@example.com', is_admin=False,
                                                            storage_path='/path/to/storage')

        url = reverse('delete_user', args=[user_profile_to_delete.id])
        self.client.force_login(self.admin_user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'User deleted successfully')

    def test_user_login(self):
        url = reverse('user_login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Login successful')

    def test_user_logout(self):
        url = reverse('user_logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Logout successful')
