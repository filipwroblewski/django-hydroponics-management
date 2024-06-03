from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import HydroponicSystem
from .utils import generate_jwt_token

class HydroponicSystemCreateTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')

    def setUp(self):
        self.tokens = generate_jwt_token(self.client, 'test_user', 'test_password')
        self.access_token = self.tokens['access']

    def test_create_hydroponic_system_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post('/api/hydroponic-systems/', 
                                    {'name': 'New System', 'description': 'Description of the new system'}, 
                                    format='json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['name'], 'New System')
        self.assertEqual(data['description'], 'Description of the new system')
        self.assertEqual(data['owner'], self.user.username)

    def test_create_hydroponic_system_unauthenticated(self):
        response = self.client.post('/api/hydroponic-systems/', 
                                    {'name': 'New System', 'description': 'Description of the new system'}, 
                                    format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_create_hydroponic_system_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post('/api/hydroponic-systems/', 
                                    {'name': '', 'description': 'Description of the new system'}, 
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'][0], 'This field may not be blank.')


class HydroponicSystemDeleteTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.other_user = User.objects.create_user(username='other_user', password='other_password')

    def setUp(self):
        self.tokens = generate_jwt_token(self.client, 'test_user', 'test_password')
        self.access_token = self.tokens['access']
        self.system1 = HydroponicSystem.objects.create(owner=self.user, name='System 1', description='Description 1')
        self.system2 = HydroponicSystem.objects.create(owner=self.other_user, name='System 2', description='Description 2')

    def test_delete_hydroponic_system_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.delete(f'/api/hydroponic-systems/{self.system1.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(HydroponicSystem.objects.filter(id=self.system1.id).exists())

    def test_delete_hydroponic_system_unauthenticated(self):
        response = self.client.delete(f'/api/hydroponic-systems/{self.system1.id}/')
        self.assertEqual(response.status_code, 401)
        self.assertTrue(HydroponicSystem.objects.filter(id=self.system1.id).exists())

    def test_delete_hydroponic_system_not_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.delete(f'/api/hydroponic-systems/{self.system2.id}/')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(HydroponicSystem.objects.filter(id=self.system2.id).exists())