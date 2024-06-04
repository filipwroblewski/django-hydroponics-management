from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import HydroponicSystem, Measurement
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


class MeasurementCreateTestCase(BaseTestCase):

    def test_create_measurement_authenticated(self):
        # Make an authenticated request to create a measurement
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        system = HydroponicSystem.objects.create(
            owner=self.user, name='Test System',
            description='Test Description')
        data = {
            'system': system.id,
            'ph': 6.5,
            'temperature': 25.5,
            'tds': 800}
        response = self.client.post(
            '/api/measurements/', data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED)

    def test_create_measurement_unauthenticated(self):
        # Make an unauthenticated request to create a measurement
        system = HydroponicSystem.objects.create(
            owner=self.user, name='Test System',
            description='Test Description')
        data = {'system': system.id,
                'ph': 6.5,
                'temperature': 25.5,
                'tds': 800}
        response = self.client.post(
            '/api/measurements/', data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.')

    def test_create_measurement_invalid_token(self):
        # Make a request with an invalid token to create a measurement
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        system = HydroponicSystem.objects.create(
            owner=self.user, name='Test System',
            description='Test Description')
        data = {
            'system': system.id,
            'ph': 6.5,
            'temperature': 25.5,
            'tds': 800}
        response = self.client.post(
            '/api/measurements/', data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data['detail'],
            'Given token not valid for any token type')


class MeasurementDeleteTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a HydroponicSystem instance
        self.system = HydroponicSystem.objects.create(
            owner=self.user, name='Test System',
            description='Test Description')
        # Create a Measurement instance associated with the system
        self.measurement = Measurement.objects.create(
            system=self.system, ph=7.0, temperature=25.0, tds=800)

    def test_delete_measurement_authenticated(self):
        # Make an authenticated request to delete a measurement
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.delete(
            f'/api/measurements/{self.measurement.id}/')
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT)
        # Check if the measurement has been deleted from the database
        self.assertFalse(
            Measurement.objects.filter(
                id=self.measurement.id).exists())

    def test_delete_measurement_unauthenticated(self):
        # Make an unauthenticated request to delete a measurement
        response = self.client.delete(
            f'/api/measurements/{self.measurement.id}/')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_measurement_invalid_token(self):
        # Make a request with an invalid token to delete a measurement
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        response = self.client.delete(
            f'/api/measurements/{self.measurement.id}/')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED)


class MeasurementUpdateTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Create a HydroponicSystem instance
        self.system = HydroponicSystem.objects.create(
            owner=self.user, name='Test System',
            description='Test Description')
        # Create a Measurement instance associated with the system
        self.measurement = Measurement.objects.create(
            system=self.system,
            ph=7.0,
            temperature=25.0,
            tds=800)

    def test_update_measurement_authenticated(self):
        # Make an authenticated request
        # to update a measurement
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        new_data = {
            'system': self.system.id,
            'ph': 6.8,
            'temperature': 26.0,
            'tds': 900}
        response = self.client.put(
            f'/api/measurements/{self.measurement.id}/',
            new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the measurement has been updated in the database
        updated_measurement = Measurement.objects.get(
            id=self.measurement.id)
        self.assertEqual(updated_measurement.ph, 6.8)
        self.assertEqual(updated_measurement.temperature, 26.0)
        self.assertEqual(updated_measurement.tds, 900)

    def test_update_measurement_unauthenticated(self):
        # Make an unauthenticated request to update a measurement
        new_data = {
            'system': self.system.id,
            'ph': 6.8,
            'temperature': 26.0,
            'tds': 900}
        response = self.client.put(
            f'/api/measurements/{self.measurement.id}/',
            new_data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_measurement_invalid_token(self):
        # Make a request with an invalid token
        # to update a measurement
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        new_data = {
            'system': self.system.id,
            'ph': 6.8,
            'temperature': 26.0,
            'tds': 900}
        response = self.client.put(
            f'/api/measurements/{self.measurement.id}/',
            new_data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED)


class MeasurementPartialUpdateTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Create a HydroponicSystem instance
        self.system = HydroponicSystem.objects.create(
            owner=self.user, name='Test System',
            description='Test Description')
        # Create a Measurement instance associated with the system
        self.measurement = Measurement.objects.create(
            system=self.system, ph=7.0, temperature=25.0, tds=800)

    def test_measurement_partial_update_authenticated(self):
        # Make an authenticated request
        # to partially update a measurement
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
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
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_measurement_partial_update_invalid_token(self):
        # Make a request with an invalid token
        # to partially update a measurement
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        url = f'/api/measurements/{self.measurement.id}/'
        data = {'temperature': 26.0}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED)


class MeasurementDisplayTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Create some static hydroponic systems
        systems = [
            HydroponicSystem.objects.create(
                owner=self.user, name=f'System {_}',
                description=f'Description {_}') for _ in range(1, 6)]
        # Create some static measurements associated with each system
        for system in systems:
            measurements_data = [
                {'system': system, 'ph': 6.5, 'temperature': 25.5, 'tds': 800},
                {'system': system, 'ph': 7.0, 'temperature': 26.0, 'tds': 850}
            ]
            for data in measurements_data:
                Measurement.objects.create(**data)

    def test_measurement_list_authenticated(self):
        # Make an authenticated request
        # to get the list of measurements
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
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
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_measurement_list_invalid_token(self):
        # Make a request with an invalid token to get the list of measurements
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        response = self.client.get('/api/measurements/')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED)


class MeasurementPaginationTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.system = HydroponicSystem.objects.create(
            owner=cls.user, name='Sys1', description='System 1')

        # Create multiple measurements to test pagination
        Measurement.objects.bulk_create([
            Measurement(system=cls.system, ph=6.5, temperature=25.5, tds=800),
            Measurement(system=cls.system, ph=7.0, temperature=26.0, tds=850),
            Measurement(system=cls.system, ph=6.8, temperature=25.8, tds=820),
            Measurement(system=cls.system, ph=7.2, temperature=26.2, tds=860),
            Measurement(system=cls.system, ph=6.7, temperature=25.7, tds=810)
        ])

    def test_unauthenticated_request(self):
        # Make an unauthenticated request
        response = self.client.get('/api/measurements/?page_size=2')

        # Check if the request returns unauthorized status
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pagination_with_page_size(self):
        # Make an authenticated request with page_size=2
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            '/api/measurements/?page_size=2')

        # Check if the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify pagination structure and content
        data = response.json()
        self.assertIn('count', data)
        self.assertIn('next', data)
        self.assertIn('previous', data)
        self.assertIn('results', data)

        # Check pagination count and results
        self.assertEqual(data['count'], 5)
        self.assertEqual(len(data['results']), 2)
        self.assertIsNotNone(data['next'])
        self.assertIsNone(data['previous'])

        # Follow the next page link
        next_page_url = data['next']
        response = self.client.get(next_page_url)
        data = response.json()

        # Check the second page of results
        self.assertEqual(len(data['results']), 2)
        self.assertIsNotNone(data['next'])
        self.assertIsNotNone(data['previous'])

        # Follow the next page link again
        next_page_url = data['next']
        response = self.client.get(next_page_url)
        data = response.json()

        # Check the third and last page of results
        self.assertEqual(len(data['results']), 1)
        self.assertIsNone(data['next'])
        self.assertIsNotNone(data['previous'])

    def test_pagination_with_different_page_sizes(self):
        # Test with page_size=3
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            '/api/measurements/?page_size=3')

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 5)
        self.assertEqual(len(data['results']), 3)
        self.assertIsNotNone(data['next'])
        self.assertIsNone(data['previous'])

        # Follow the next page link
        next_page_url = data['next']
        response = self.client.get(next_page_url)
        data = response.json()

        # Check the second page of results
        self.assertEqual(len(data['results']), 2)
        self.assertIsNone(data['next'])
        self.assertIsNotNone(data['previous'])

    def test_pagination_with_page_size_bigger_than_data(self):
        # Test with page_size=10,
        # which is larger than the number of measurements
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            '/api/measurements/?page_size=10')

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 5)
        self.assertEqual(len(data['results']), 5)
        self.assertIsNone(data['next'])
        self.assertIsNone(data['previous'])

    def test_pagination_with_no_additional_pages(self):
        # Test with page_size=5,
        # which exactly matches the number of measurements
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            '/api/measurements/?page_size=5')

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 5)
        self.assertEqual(len(data['results']), 5)
        self.assertIsNone(data['next'])
        self.assertIsNone(data['previous'])

    def test_direct_next_page_access(self):
        # Make an authenticated request with page_size=2
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            '/api/measurements/?page_size=2')

        data = response.json()
        next_page_url = data['next']

        # Directly access the next page
        response = self.client.get(next_page_url)
        data = response.json()

        # Check the results on the second page
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['results']), 2)
        self.assertIsNotNone(data['next'])
        self.assertIsNotNone(data['previous'])


class MeasurementFilterByPHTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.system = HydroponicSystem.objects.create(
            owner=cls.user, name='Sys1', description='System 1')

        # Create multiple measurements to test filtering by pH
        Measurement.objects.bulk_create([
            Measurement(system=cls.system, ph=6.5, temperature=25.5, tds=800),
            Measurement(system=cls.system, ph=7.0, temperature=26.0, tds=850),
            Measurement(system=cls.system, ph=6.8, temperature=25.8, tds=820),
            Measurement(system=cls.system, ph=7.2, temperature=26.2, tds=860),
            Measurement(system=cls.system, ph=6.7, temperature=25.7, tds=810)
        ])

    def test_filter_by_ph_range(self):
        # Test filtering with a valid pH range
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            '/api/measurements/?ph_min=6.7&ph_max=7.0')

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['results']), 3)

        for result in data['results']:
            self.assertGreaterEqual(result['ph'], 6.7)
            self.assertLessEqual(result['ph'], 7.0)

    def test_filter_by_ph_min_out_of_range(self):
        # Test filtering with a pH min value lower than any possible pH
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            '/api/measurements/?ph_min=1.0')

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 5)
        self.assertEqual(len(data['results']), 5)

    def test_filter_by_ph_no_results(self):
        # Test filtering with a pH range that results in no matches
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            '/api/measurements/?ph_min=8.0&ph_max=9.0')

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['results']), 0)


class MeasurementFilterByTemperatureTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.system = HydroponicSystem.objects.create(
            owner=cls.user, name='Sys1', description='System 1')

        # Create multiple measurements to test filtering by temperature
        Measurement.objects.bulk_create([
            Measurement(system=cls.system, ph=6.5, temperature=25.5, tds=800),
            Measurement(system=cls.system, ph=7.0, temperature=26.0, tds=850),
            Measurement(system=cls.system, ph=6.8, temperature=25.8, tds=820),
            Measurement(system=cls.system, ph=7.2, temperature=26.2, tds=860),
            Measurement(system=cls.system, ph=6.7, temperature=25.7, tds=810)
        ])

    def test_filter_by_temperature_range(self):
        # Test filtering with a valid temperature range
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            '/api/measurements/?temperature_min=25.7&temperature_max=26.0')

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['results']), 3)

        for result in data['results']:
            self.assertGreaterEqual(result['temperature'], 25.7)
            self.assertLessEqual(result['temperature'], 26.0)

    def test_filter_by_temperature_no_results(self):
        # Test filtering with a temperature range that results in no matches
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            '/api/measurements/?temperature_min=30.0&temperature_max=35.0')

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['results']), 0)


class MeasurementFilterByTDSTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.system = HydroponicSystem.objects.create(
            owner=cls.user, name='Sys1', description='System 1')

        # Create multiple measurements to test filtering by TDS
        Measurement.objects.bulk_create([
            Measurement(system=cls.system, ph=6.5, temperature=25.5, tds=800),
            Measurement(system=cls.system, ph=7.0, temperature=26.0, tds=850),
            Measurement(system=cls.system, ph=6.8, temperature=25.8, tds=820),
            Measurement(system=cls.system, ph=7.2, temperature=26.2, tds=860),
            Measurement(system=cls.system, ph=6.7, temperature=25.7, tds=810)
        ])

    def test_filter_by_tds_range(self):
        # Test filtering with a valid TDS range
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            '/api/measurements/?tds_min=810&tds_max=850')

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['results']), 3)

        for result in data['results']:
            self.assertGreaterEqual(result['tds'], 810)
            self.assertLessEqual(result['tds'], 850)

    def test_filter_by_tds_min_only(self):
        # Test filtering with only a TDS min value
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get('/api/measurements/?tds_min=820')

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['results']), 3)

        for result in data['results']:
            self.assertGreaterEqual(result['tds'], 820)

    def test_filter_by_tds_max_only(self):
        # Test filtering with only a TDS max value
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get('/api/measurements/?tds_max=810')

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['results']), 2)

        for result in data['results']:
            self.assertLessEqual(result['tds'], 810)

    def test_filter_by_tds_no_results(self):
        # Test filtering with a TDS range that results in no matches
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            '/api/measurements/?tds_min=900&tds_max=1000')

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['results']), 0)


class MeasurementLastMeasurementsTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.system = HydroponicSystem.objects.create(
            owner=cls.user, name='Sys1', description='System 1')

        # Create multiple measurements to test retrieving the last measurements
        Measurement.objects.bulk_create([
            Measurement(system=cls.system, ph=6.5, temperature=25.5, tds=800),
            Measurement(system=cls.system, ph=7.0, temperature=26.0, tds=850),
            Measurement(system=cls.system, ph=6.8, temperature=25.8, tds=820),
            Measurement(system=cls.system, ph=7.2, temperature=26.2, tds=860),
            Measurement(system=cls.system, ph=6.7, temperature=25.7, tds=810),
            Measurement(system=cls.system, ph=7.1, temperature=26.1, tds=830),
            Measurement(system=cls.system, ph=6.9, temperature=25.9, tds=805),
            Measurement(system=cls.system, ph=7.3, temperature=26.3, tds=865),
            Measurement(system=cls.system, ph=6.6, temperature=25.6, tds=815),
            Measurement(system=cls.system, ph=7.4, temperature=26.4, tds=870),
            Measurement(system=cls.system, ph=6.4, temperature=25.4, tds=795),
            Measurement(system=cls.system, ph=7.5, temperature=26.5, tds=875)
        ])

    def test_last_measurements(self):
        # Test retrieving the last 3 measurements
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            ('/api/measurements/last-measurements/'
             '?system_name=Sys1&num_measurements=3'))

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 3)

        # Check that the measurements are the last 3 created
        expected_measurements = [
            {'ph': 7.5, 'temperature': 26.5, 'tds': 875},
            {'ph': 6.4, 'temperature': 25.4, 'tds': 795},
            {'ph': 7.4, 'temperature': 26.4, 'tds': 870}
        ]
        for i, result in enumerate(data):
            self.assertEqual(
                result['ph'],
                expected_measurements[i]['ph'])
            self.assertEqual(
                result['temperature'],
                expected_measurements[i]['temperature'])
            self.assertEqual(
                result['tds'],
                expected_measurements[i]['tds'])

    def test_last_10_measurements(self):
        # Test retrieving the last 10 measurements
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(
            ('/api/measurements/last-measurements/'
             '?system_name=Sys1&num_measurements=10'))

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 10)

        # Check that the measurements are the last 10 created
        expected_measurements = [
            {'ph': 7.5, 'temperature': 26.5, 'tds': 875},
            {'ph': 6.4, 'temperature': 25.4, 'tds': 795},
            {'ph': 7.4, 'temperature': 26.4, 'tds': 870},
            {'ph': 6.6, 'temperature': 25.6, 'tds': 815},
            {'ph': 7.3, 'temperature': 26.3, 'tds': 865},
            {'ph': 6.9, 'temperature': 25.9, 'tds': 805},
            {'ph': 7.1, 'temperature': 26.1, 'tds': 830},
            {'ph': 6.7, 'temperature': 25.7, 'tds': 810},
            {'ph': 7.2, 'temperature': 26.2, 'tds': 860},
            {'ph': 6.8, 'temperature': 25.8, 'tds': 820}
        ]
        for i, result in enumerate(data):
            self.assertEqual(result['ph'], expected_measurements[i]['ph'])
            self.assertEqual(
                result['temperature'],
                expected_measurements[i]['temperature'])
            self.assertEqual(result['tds'], expected_measurements[i]['tds'])
