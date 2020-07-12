from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class SignUpTests(APITestCase):
    def test_client_signup_sucess(self):
        """
        Ensure that the client can create a new account object.
        """

        valid_data = {
            "email": "contact@mail.com",
            "password": "ASD123**",
            "password2": "ASD123**",
            "name": "Gustavo Fonseca",
            "cpf": "929.853.569-46",
            "gender": "M",
            "dt_birth": "2000-01-01",
            "cellphone": "(79) 98899-8899",
        }

        response = self.client.post("/signup", valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().email, "contact@mail.com")

        # Ensure the email is unique
        response = self.client.post("/signup", valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_client_signup_validation(self):
        """
        Ensure that the client can create a new account object.
        """

        invalid_data = {
            "email": "invalidmail",
            "password": "123",
            "name": "",
            "cpf": "000.111.222-33",
            "gender": "X",
            "dt_birth": "2010-00-00",
            "cellphone": "(79) 9899-8899",
        }

        response = self.client.post("/signup", invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)
        self.assertIn("name", response.data)
        self.assertIn("cpf", response.data)
        self.assertIn("gender", response.data)
        self.assertIn("dt_birth", response.data)
        self.assertIn("cellphone", response.data)

