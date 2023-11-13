from django.test import TestCase
from rest_framework.test import APIClient
from users.models import UserProfile
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfileAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.admin_user)

    def test_get_user_profile_list(self):
        response = self.client.get('/api/users/userprofiles/')
        self.assertEqual(response.status_code, 200)

    def test_create_user_profile(self):
        user = User.objects.create_user(username='testuser', password='testpassword')

        data = {
            'user': user.pk,
            'full_name': 'Test User',
            'email': 'test@example.com',
            'storage_path': '/path/to/storage',
        }
        response = self.client.post('/api/users/userprofiles/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.last().userprofile.full_name, 'Test User')


class UserProfileModelTestCase(TestCase):
    def test_user_profile_creation(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        user_profile = UserProfile.objects.register_user(user=user, full_name='Test User', email='test@example.com')
        self.assertEqual(user_profile.full_name, 'Test User')
        self.assertEqual(user_profile.email, 'test@example.com')