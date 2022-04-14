from django.test import TestCase
from django.contrib.auth.models import User
from faker import Faker


class CreateUserTestCase(TestCase):
    """
    This class is going to create new user for testing
    """
    def setUp(self) -> None:
        faker = Faker()
        self.username = faker.user_name()
        self.email = faker.email()
        self.password = faker.password()
        self.first_name = faker.first_name
        self.last_name = faker.last_name

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name
        )

    def tearDown(self) -> None:
        self.user.delete()
