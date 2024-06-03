from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import HydroponicSystem

def generate_jwt_token(client, username, password):
    url = '/api/token/'
    response = client.post(url, {'username': username, 'password': password}, format='json')
    if response.status_code == 200:
        return response.json()
    return None

class GenerateJWTTokenTestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(username='test_user', password='test_password')

    def test_generate_jwt_token_success(self):
        """Test generating JWT token with valid credentials."""
        tokens = generate_jwt_token(self.client, 'test_user', 'test_password')
        self.assertIsNotNone(tokens)
        self.assertIn('refresh', tokens)
        self.assertIn('access', tokens)

    def test_generate_jwt_token_invalid_credentials(self):
        """Test generating JWT token with invalid credentials."""
        tokens = generate_jwt_token(self.client, 'invalid_user', 'invalid_password')
        self.assertIsNone(tokens)

    def test_generate_jwt_token_no_credentials(self):
        """Test generating JWT token with no credentials."""
        tokens = generate_jwt_token(self.client, '', '')
        self.assertIsNone(tokens)

    def test_generate_jwt_token_wrong_password(self):
        """Test generating JWT token with correct username but wrong password."""
        tokens = generate_jwt_token(self.client, 'test_user', 'wrong_password')
        self.assertIsNone(tokens)

