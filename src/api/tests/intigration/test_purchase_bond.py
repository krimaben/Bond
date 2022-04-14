from api.tests import CreateUserTestCase
from django.urls import reverse
from rest_framework.test import APIClient

from api.models import Bond


class PurchaseBondTestCase(CreateUserTestCase):
    """
    Test case for Purchase Bond
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
        self.bond = self.create_bond()

    def create_bond(self):
        payload = {
            "bond_name": "Test Name",
            "number_of_bonds": 10000,
            "sp_of_bonds": 56000.0001

        }
        response = self.client.post(
            reverse('list_create_bonds'),
            payload,
            format='json'
        )

        return response.json()

    def test_purchase_bond(self):
        response = self.client.put(
            reverse('purchase_bond', kwargs={
                'publication_id': self.bond.get('publication_id', None)
            }),
            format='json'
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['publication_id'], self.bond.get('publication_id', None))
        self.assertTrue('purchased' in response.json()['status_of_bond'])

    def tearDown(self) -> None:
        self.client.logout()
        Bond.objects.filter().delete()
        super().tearDown()
