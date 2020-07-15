from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class SignUpTests(APITestCase):

    def setUp(self):
        self.valid_data = {
            "email": "regular@regular.com",
            "password": "ASD123**",
            "password2": "ASD123**",
            "name": "João Lima",
            "cpf": "929.853.569-46",
            "gender": "M",
            "date_birth": "2000-01-01",
            "cellphone": "(11) 98899-8899"
        }
        self.invalid_data = {
            "email": "invalidmail",
            "password": "123",
            "name": "",
            "cpf": "000.111.222-33",
            "gender": "X",
            "date_birth": "200-00-00",
            "cellphone": "(79) 9899-889",
        }


    def test_client_signup(self):
        """
        Ensure we can create a new client's profile object.
        """

        # create test
        response = self.client.post(reverse("signup-list"), self.valid_data)
        new_user = User.objects.get(email=self.valid_data.get("email"))
        client_profile = new_user.client_profile

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_user.email, self.valid_data.get("email"))
        self.assertEqual(client_profile.name, self.valid_data.get("name"))
        self.assertEqual(client_profile.cpf, self.valid_data.get("cpf"))
        self.assertEqual(client_profile.gender, self.valid_data.get("gender"))
        self.assertEqual(
            client_profile.cellphone, self.valid_data.get("cellphone"))

        # Ensure the email is unique
        response = self.client.post(reverse("signup-list"), self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

        # login test
        payload = {"email": "regular@regular.com", "password": "ASD123**"}
        response = self.client.post(reverse("login"), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_signup_validation(self):
        """
        Ensure all client's info are valid
        """

        response = self.client.post(reverse("signup-list"), self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)
        self.assertIn("name", response.data)
        self.assertIn("cpf", response.data)
        self.assertIn("gender", response.data)
        self.assertIn("date_birth", response.data)
        self.assertIn("cellphone", response.data)
