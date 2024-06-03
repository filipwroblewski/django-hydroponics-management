from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .utils import generate_jwt_token

class GenerateJWTTokenTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')

    def test_generate_jwt_token_success(self):
        tokens = generate_jwt_token(self.client, 'test_user', 'test_password')
        self.assertIsNotNone(tokens)
        self.assertIn('refresh', tokens)
        self.assertIn('access', tokens)

    def test_generate_jwt_token_invalid_credentials(self):
        tokens = generate_jwt_token(self.client, 'invalid_user', 'invalid_password')
        self.assertIsNone(tokens)

    def test_generate_jwt_token_no_credentials(self):
        tokens = generate_jwt_token(self.client, '', '')
        self.assertIsNone(tokens)

    def test_generate_jwt_token_wrong_password(self):
        tokens = generate_jwt_token(self.client, 'test_user', 'wrong_password')
        self.assertIsNone(tokens)
