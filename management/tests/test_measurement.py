from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import HydroponicSystem, Measurement
from .utils import generate_jwt_token

class BaseTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')

    def setUp(self):
        self.tokens = generate_jwt_token(self.client, 'test_user', 'test_password')
        self.access_token = self.tokens['access']


class MeasurementCreateTestCase(BaseTestCase):

    def test_create_measurement_authenticated(self):
        # Make an authenticated request to create a measurement
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        system = HydroponicSystem.objects.create(owner=self.user, name='Test System', description='Test Description')
        data = {'system': system.id, 'ph': 6.5, 'temperature': 25.5, 'tds': 800}
        response = self.client.post('/api/measurements/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_measurement_unauthenticated(self):
        # Make an unauthenticated request to create a measurement
        system = HydroponicSystem.objects.create(owner=self.user, name='Test System', description='Test Description')
        data = {'system': system.id, 'ph': 6.5, 'temperature': 25.5, 'tds': 800}
        response = self.client.post('/api/measurements/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_create_measurement_invalid_token(self):
        # Make a request with an invalid token to create a measurement
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        system = HydroponicSystem.objects.create(owner=self.user, name='Test System', description='Test Description')
        data = {'system': system.id, 'ph': 6.5, 'temperature': 25.5, 'tds': 800}
        response = self.client.post('/api/measurements/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Given token not valid for any token type')


class MeasurementDeleteTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a HydroponicSystem instance
        self.system = HydroponicSystem.objects.create(owner=self.user, name='Test System', description='Test Description')
        # Create a Measurement instance associated with the system
        self.measurement = Measurement.objects.create(system=self.system, ph=7.0, temperature=25.0, tds=800)

    def test_delete_measurement_authenticated(self):
        # Make an authenticated request to delete a measurement
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.delete(f'/api/measurements/{self.measurement.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check if the measurement has been deleted from the database
        self.assertFalse(Measurement.objects.filter(id=self.measurement.id).exists())

    def test_delete_measurement_unauthenticated(self):
        # Make an unauthenticated request to delete a measurement
        response = self.client.delete(f'/api/measurements/{self.measurement.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_measurement_invalid_token(self):
        # Make a request with an invalid token to delete a measurement
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        response = self.client.delete(f'/api/measurements/{self.measurement.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class MeasurementUpdateTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Create a HydroponicSystem instance
        self.system = HydroponicSystem.objects.create(owner=self.user, name='Test System', description='Test Description')
        # Create a Measurement instance associated with the system
        self.measurement = Measurement.objects.create(system=self.system, ph=7.0, temperature=25.0, tds=800)

    def test_update_measurement_authenticated(self):
        # Make an authenticated request to update a measurement
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        new_data = {'system': self.system.id, 'ph': 6.8, 'temperature': 26.0, 'tds': 900}
        response = self.client.put(f'/api/measurements/{self.measurement.id}/', new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the measurement has been updated in the database
        updated_measurement = Measurement.objects.get(id=self.measurement.id)
        self.assertEqual(updated_measurement.ph, 6.8)
        self.assertEqual(updated_measurement.temperature, 26.0)
        self.assertEqual(updated_measurement.tds, 900)

    def test_update_measurement_unauthenticated(self):
        # Make an unauthenticated request to update a measurement
        new_data = {'system': self.system.id, 'ph': 6.8, 'temperature': 26.0, 'tds': 900}
        response = self.client.put(f'/api/measurements/{self.measurement.id}/', new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_measurement_invalid_token(self):
        # Make a request with an invalid token to update a measurement
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        new_data = {'system': self.system.id, 'ph': 6.8, 'temperature': 26.0, 'tds': 900}
        response = self.client.put(f'/api/measurements/{self.measurement.id}/', new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MeasurementPartialUpdateTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Create a HydroponicSystem instance
        self.system = HydroponicSystem.objects.create(owner=self.user, name='Test System', description='Test Description')
        # Create a Measurement instance associated with the system
        self.measurement = Measurement.objects.create(system=self.system, ph=7.0, temperature=25.0, tds=800)

    def test_measurement_partial_update_authenticated(self):
        # Make an authenticated request to partially update a measurement
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = f'/api/measurements/{self.measurement.id}/'
        data = {'temperature': 26.0} 
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the measurement has been partially updated
        updated_measurement = Measurement.objects.get(id=self.measurement.id)
        self.assertEqual(updated_measurement.temperature, 26.0)

    def test_measurement_partial_update_unauthenticated(self):
        # Make an unauthenticated request to partially update a measurement
        url = f'/api/measurements/{self.measurement.id}/'
        data = {'temperature': 26.0}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_measurement_partial_update_invalid_token(self):
        # Make a request with an invalid token to partially update a measurement
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        url = f'/api/measurements/{self.measurement.id}/'
        data = {'temperature': 26.0}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MeasurementDisplayTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Create some static hydroponic systems
        systems = [HydroponicSystem.objects.create(owner=self.user, name=f'System {_}', description=f'Description {_}') for _ in range(1, 6)]
        # Create some static measurements associated with each system
        for system in systems:
            measurements_data = [
                {'system': system, 'ph': 6.5, 'temperature': 25.5, 'tds': 800},
                {'system': system, 'ph': 7.0, 'temperature': 26.0, 'tds': 850}
            ]
            for data in measurements_data:
                Measurement.objects.create(**data)


    def test_measurement_list_authenticated(self):
        # Make an authenticated request to get the list of measurements
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get('/api/measurements/')
        
        # Check if the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if the response data contains the expected measurements
        data = response.json()
        self.assertEqual(data['count'], 10)
        self.assertIsNone(data['next'])
        self.assertIsNone(data['previous'])
        
        # Check each measurement in the results array
        for measurement_data in data['results']:
            self.assertIn('id', measurement_data)
            self.assertIn('system', measurement_data)
            self.assertIn('ph', measurement_data)
            self.assertIn('temperature', measurement_data)
            self.assertIn('tds', measurement_data)
            self.assertIn('timestamp', measurement_data)

    def test_measurement_list_unauthenticated(self):
        # Make an unauthenticated request to get the list of measurements
        response = self.client.get('/api/measurements/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_measurement_list_invalid_token(self):
        # Make a request with an invalid token to get the list of measurements
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        response = self.client.get('/api/measurements/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


