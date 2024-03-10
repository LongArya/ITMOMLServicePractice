import requests
from http import HTTPStatus
from pprint import pprint
from requests import Response
from backend.core.config import settings

BACKEND_API = "http://127.0.0.1:8000"
REGISTER_ENDPOINT = f"{BACKEND_API}{settings.API_V1_STR}/auth/register"
LOGIN_ENDPOINT = f"{BACKEND_API}{settings.API_V1_STR}/auth/login"
CURRENT_USER_ENDPOINT = f"{BACKEND_API}{settings.API_V1_STR}/users/me"


def register_user_via_api(username: str, email: str, password: str) -> Response:
    user_data = {
        "name": username,
        "email": email,
        "is_active": True,
        "is_superuser": False,
        "password": password,
    }
    response = requests.post(REGISTER_ENDPOINT, json=user_data)
    return response


def login_via_api(email: str, password: str) -> Response:
    auth_data = {"username": email, "password": password}
    response = requests.post(LOGIN_ENDPOINT, data=auth_data)
    return response


def get_current_user_data_via_api(access_token: str) -> Response:
    headers = {"Authorization": f"Bearer {access_token}"}
    response: Response = requests.get(CURRENT_USER_ENDPOINT, headers=headers)
    return response
