from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from users.models import EmailVerification

User = get_user_model()

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register-list')
        self.user_data = {
            "username":"randomusername",
            "email":"managadzeandria06@gmail.com",
            "password":"strongpassword123",
            "password2":"strongpassword123",
            "first_name":"nika",
            "last_name":"nika",
            "phone_number":"588588588"
        }

    def test_user_registration_sucess(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())
        user = User.objects.get(email=self.user_data['email'])
        self.assertFalse(user.is_active)
        self.assertTrue(EmailVerification.objects.filter(user=user).exists())

    def test_password_mismatch(self):
        self.user_data['password2'] = 'newrandompassword123'
        response = self.client.post(self.register_url,self.user_data,format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertFalse(User.objects.filter(email=self.user_data['email']).exists())

    def test_user_registration_duplicate_email(self):
        User.objects.create(
            username = 'randomusername123',
            email = self.user_data['email'],
            password = 'randompassword123',
        )
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)