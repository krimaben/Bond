from api.tests import CreateUserTestCase
from django.urls import reverse
from rest_framework.test import APIClient

from api.models import Bond


class USDRateTestCase(CreateUserTestCase):
    """
    Test case for update USD Rate
    """

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(reverse("user_login"), payload, format='json')
        self.access_token = response.json().get('access', None)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.bonds_list = self.create_list_bonds()

    def create_list_bonds(self):
        bond_list = []
        payloads = [
            {
                "bond_name": "Test1 Name",
                "number_of_bonds": 999,
                "sp_of_bonds": 56001.0001

            },
            {
                "bond_name": "Test2 Name",
                "number_of_bonds": 10000,
                "sp_of_bonds": 57000.0001
            }
        ]
        for payload in payloads:
            response = self.client.post(
                reverse('list_create_bonds'),
                payload,
                format='json'
            )
            bond_list.append(response.json())

        return bond_list

    def test_usd_rate(self):
        response = self.client.put(
            reverse('update_usd_rate'),
            format='json'
        )

        self.assertEquals(response.status_code, 200)
        self.assertTrue(1 <= len(response.json()))

    def tearDown(self) -> None:
        self.client.logout()
        Bond.objects.filter().delete()
        super().tearDown()
