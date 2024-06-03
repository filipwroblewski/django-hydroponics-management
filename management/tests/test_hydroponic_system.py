from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import HydroponicSystem
from .utils import generate_jwt_token


class BaseTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test_user', password='test_password')

    def setUp(self):
        self.tokens = generate_jwt_token(
            self.client, 'test_user', 'test_password')
        self.access_token = self.tokens['access']


class HydroponicSystemCreateTestCase(BaseTestCase):

    def test_create_hydroponic_system_authenticated(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(
            '/api/hydroponic-systems/',
            {
                'name': 'New System',
                'description': 'Description of the new system'},
            format='json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['name'], 'New System')
        self.assertEqual(
            data['description'],
            'Description of the new system')
        self.assertEqual(data['owner'], self.user.username)

    def test_create_hydroponic_system_unauthenticated(self):
        response = self.client.post(
            '/api/hydroponic-systems/',
            {
                'name': 'New System',
                'description': 'Description of the new system'},
            format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.')

    def test_create_hydroponic_system_invalid_data(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(
            '/api/hydroponic-systems/',
            {
                'name': '',
                'description': 'Description of the new system'},
            format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.data)
        self.assertEqual(
            response.data['name'][0],
            'This field may not be blank.')


class HydroponicSystemDeleteTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.other_user = User.objects.create_user(
            username='other_user', password='other_password')

        self.system1 = HydroponicSystem.objects.create(
            owner=self.user, name='System 1',
            description='Description 1')
        self.system2 = HydroponicSystem.objects.create(
            owner=self.other_user, name='System 2',
            description='Description 2')

    def test_delete_hydroponic_system_authenticated(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.delete(
            f'/api/hydroponic-systems/{self.system1.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(HydroponicSystem.objects.filter(
            id=self.system1.id).exists())

    def test_delete_hydroponic_system_unauthenticated(self):
        response = self.client.delete(
            f'/api/hydroponic-systems/{self.system1.id}/')
        self.assertEqual(response.status_code, 401)
        self.assertTrue(
            HydroponicSystem.objects.filter(id=self.system1.id).exists())

    def test_delete_hydroponic_system_not_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.delete(
            f'/api/hydroponic-systems/{self.system2.id}/')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            HydroponicSystem.objects.filter(id=self.system2.id).exists())


class HydroponicSystemUpdateTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.system = HydroponicSystem.objects.create(
            owner=self.user, name='Test System',
            description='Test Description')

    def test_hydroponic_system_update_authenticated(self):
        # Make an authenticated request to update the hydroponic system
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = f'/api/hydroponic-systems/{self.system.id}/'
        data = {
            'name': 'Test System - Update',
            'description': 'Updated description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        # Check if the system was updated
        updated_system = HydroponicSystem.objects.get(id=self.system.id)
        self.assertEqual(updated_system.name, 'Test System - Update')
        self.assertEqual(updated_system.description, 'Updated description')

    def test_hydroponic_system_update_unauthenticated(self):
        # Make an unauthenticated request to update the hydroponic system
        url = f'/api/hydroponic-systems/{self.system.id}/'
        data = {
            'name': 'Test System - Update',
            'description': 'Updated description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.')

    def test_hydroponic_system_update_invalid_token(self):
        # Make a request with an invalid token to update the hydroponic system
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        url = f'/api/hydroponic-systems/{self.system.id}/'
        data = {
            'name': 'Test System - Update',
            'description': 'Updated description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'],
            'Given token not valid for any token type')


class HydroponicSystemPartialUpdateTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.system = HydroponicSystem.objects.create(
            owner=self.user, name='Test System',
            description='Test Description')

    def test_hydroponic_system_partial_update_name_authenticated(self):
        # Make an authenticated request
        # to update just the name of the hydroponic system
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = f'/api/hydroponic-systems/{self.system.id}/'
        data = {'name': 'Test System - Name Update'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        # Check if the name was updated
        updated_system = HydroponicSystem.objects.get(id=self.system.id)
        self.assertEqual(updated_system.name, 'Test System - Name Update')
        self.assertEqual(updated_system.description, 'Test Description')

    def test_hydroponic_system_partial_update_description_authenticated(self):
        # Make an authenticated request
        # to update just the description of the hydroponic system
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = f'/api/hydroponic-systems/{self.system.id}/'
        data = {'description': 'Updated description'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        # Check if the description was updated
        updated_system = HydroponicSystem.objects.get(id=self.system.id)
        self.assertEqual(updated_system.name, 'Test System')
        self.assertEqual(updated_system.description, 'Updated description')

    def test_hydroponic_system_partial_update_unauthenticated(self):
        # Make an unauthenticated request
        # to update just the name of the hydroponic system
        url = f'/api/hydroponic-systems/{self.system.id}/'
        data = {'name': 'Test System - Name Update'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.')

    def test_hydroponic_system_partial_update_invalid_token(self):
        # Make a request with an invalid token
        # to update just the name of the hydroponic system
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        url = f'/api/hydroponic-systems/{self.system.id}/'
        data = {'name': 'Test System - Name Update'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'],
            'Given token not valid for any token type')


class HydroponicSystemListDisplayTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Create some static hydroponic systems
        [HydroponicSystem.objects.create(
            owner=self.user, name=f'System {_}',
            description=f'Description {_}') for _ in range(1, 6)]

    def test_hydroponic_system_list_authenticated(self):
        # Make an authenticated request to get the hydroponic systems list
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get('/api/hydroponic-systems/')
        self.assertEqual(response.status_code, 200)

        # Verify pagination structure and content
        data = response.json()
        self.assertIn('count', data)
        self.assertIn('results', data)
        self.assertEqual(data['count'], 5)
        systems = data['results']
        self.assertEqual(len(systems), 5)
        for i, system in enumerate(systems, start=1):
            self.assertEqual(system['name'], f'System {i}')
            self.assertEqual(system['description'], f'Description {i}')
            self.assertEqual(system['owner'], 'test_user')

            # Check if created_at and updated_at exist (auto-added fields)
            self.assertIn('created_at', system)
            self.assertIn('updated_at', system)

    def test_hydroponic_system_list_unauthenticated(self):
        # Make an unauthenticated request to get the hydroponic systems list
        response = self.client.get('/api/hydroponic-systems/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.')

    def test_hydroponic_system_list_invalid_token(self):
        # Make a request with an invalid token
        # to get the hydroponic systems list
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        response = self.client.get('/api/hydroponic-systems/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'],
            'Given token not valid for any token type')
