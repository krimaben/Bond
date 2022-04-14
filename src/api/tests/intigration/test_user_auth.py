from django.urls import reverse
from rest_framework.test import APIClient

from api.tests import CreateUserTestCase


class UserLoginTestCase(CreateUserTestCase):
    """
    This is used for testing user login through JWT Simple token
    """

    def setUp(self) -> None:
        super().setUp()

    def test_login_user(self):
        self.client = APIClient()
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(reverse("user_login"), payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.json())
        self.assertTrue('refresh' in response.json())

    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()


class UserTokenVerify(CreateUserTestCase):
    """
    This is used for user token verify
    """

    def setUp(self) -> None:
        super().setUp()

    def test_verify_token(self):
        self.client = APIClient()
        login_payload = {
            "username": self.username,
            "password": self.password
        }
        login_response = self.client.post(
            reverse("user_login"),
            login_payload,
            format='json'
        )

        token_verify_payload = {
            "token": login_response.json().get('access', None)
        }
        token_verify_response = self.client.post(
            reverse("token_varify"),
            token_verify_payload,
            format='json'
        )
        self.assertEqual(token_verify_response.status_code, 200)

    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()
