from rest_framework.test import APIClient


def generate_jwt_token(
        client: APIClient,
        username: str,
        password: str) -> dict:
    url = '/api/token/'
    response = client.post(
        url,
        {'username': username, 'password': password},
        format='json')
    if response.status_code == 200:
        return response.json()
    return None
