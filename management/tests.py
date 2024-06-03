from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class GenerateJWTTokenTestCase(APITestCase):
    
    def generate_jwt_token(self, username, password):
        url = '/api/token/'
        response = self.client.post(url, {'username': username, 'password': password}, format='json')
        if response.status_code == 200:
            return response.json()
        return None
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_generate_jwt_token_success(self):
        # Test with valid credentials
        tokens = self.generate_jwt_token('test_user', 'test_password')
        self.assertIsNotNone(tokens)
        self.assertIn('refresh', tokens)
        self.assertIn('access', tokens)

    def test_generate_jwt_token_invalid_credentials(self):
        # Test with invalid credentials
        tokens = self.generate_jwt_token('invalid_user', 'invalid_password')
        self.assertIsNone(tokens)

    def test_generate_jwt_token_no_credentials(self):
        # Test with no credentials
        tokens = self.generate_jwt_token('', '')
        self.assertIsNone(tokens)

    def test_generate_jwt_token_wrong_password(self):
        # Test with correct username but wrong password
        tokens = self.generate_jwt_token('test_user', 'wrong_password')
        self.assertIsNone(tokens)
