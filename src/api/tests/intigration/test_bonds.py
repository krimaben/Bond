from django.urls import reverse
from rest_framework.test import APIClient

from api.tests import CreateUserTestCase

from api.models import Bond


class BondTestCase(CreateUserTestCase):
    """
    Test case for create and list bond
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

        return response

    def test_create_bond_api(self):
        response = self.bond
        self.assertEquals(response.status_code, 201)
        self.assertTrue('Bond Published Successfully by user' in response.json()['success'])

    def test_list_bond_api(self):
        _ = self.create_bond()
        response = self.client.get(
            reverse('list_create_bonds'),
            format='json'
        )

        self.assertEquals(response.status_code, 200)
        self.assertTrue(len(response.json()) >= 1)

    def test_update_bond_api(self):
        bond = self.bond.json()
        payload = {
            "bond_name": "Test New Name",
            "number_of_bonds": 1001,
            "sp_of_bonds": 560.0001

        }
        response = self.client.put(
            reverse('update_bond', kwargs={
                'publication_id': bond.get('publication_id', None)
            }),
            payload,
            format='json'
        )

        self.assertEquals(response.status_code, 200)
        self.assertTrue('Test New Name' in response.json()['bond_name'])
        self.assertEquals(response.json()['number_of_bonds'], 1001)
        self.assertTrue('560.0001' in response.json()['sp_of_bonds'])

    def test_delete_bond_api(self):
        bond = self.bond.json()

        response = self.client.delete(
            reverse('delete_bond', kwargs={
                'publication_id': bond.get('publication_id', None)
            }),
            format='json'
        )

        self.assertEquals(response.status_code, 200)
        self.assertTrue('Bond Item is deleted successfully!' in response.json()['message'])

    def tearDown(self) -> None:
        self.client.logout()
        Bond.objects.filter().delete()
        super().tearDown()
