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


class HydroponicSystemListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        
        # Create some hydroponic systems for the user
        HydroponicSystem.objects.create(owner=cls.user, name='System 1', description='Description 1')
        HydroponicSystem.objects.create(owner=cls.user, name='System 2', description='Description 2')

    def setUp(self):
        # Generate JWT token for the user
        self.tokens = generate_jwt_token(self.client, 'test_user', 'test_password')
        self.access_token = self.tokens['access']

    def test_hydroponic_system_list_authenticated(self):
        """Test retrieving hydroponic systems list with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get('/api/hydroponic-systems/')
        self.assertEqual(response.status_code, 200)

        # Verify pagination structure and content
        data = response.json()
        self.assertIn('count', data)
        self.assertIn('results', data)
        self.assertEqual(data['count'], 2)
        systems = data['results']
        self.assertEqual(len(systems), 2)
        self.assertEqual(systems[0]['name'], 'System 1')
        self.assertEqual(systems[1]['name'], 'System 2')

    def test_hydroponic_system_list_unauthenticated(self):
        """Test retrieving hydroponic systems list without authentication."""
        response = self.client.get('/api/hydroponic-systems/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_hydroponic_system_list_invalid_token(self):
        """Test retrieving hydroponic systems list with an invalid token."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        response = self.client.get('/api/hydroponic-systems/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Given token not valid for any token type')

