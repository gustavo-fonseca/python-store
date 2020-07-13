from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from client.models import ClientAddress

User = get_user_model()


class SignUpTests(APITestCase):
    def test_client_signup(self):
        """
        Make sure that the client can create a new account object.
        """

        valid_data = {
            "email": "regular@regular.com",
            "password": "ASD123**",
            "password2": "ASD123**",
            "name": "João Lima",
            "cpf": "929.853.569-46",
            "gender": "M",
            "date_birth": "2000-01-01",
            "cellphone": "(79) 98899-8899",
        }

        response = self.client.post("/signup", valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "regular@regular.com")

        # Ensure the email is unique
        response = self.client.post("/signup", valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

        # login test
        payload = {"email": "regular@regular.com", "password": "ASD123**"}
        response = self.client.post("/login", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
            "date_birth": "2010-00-00",
            "cellphone": "(79) 9899-8899",
        }

        response = self.client.post("/signup", invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)
        self.assertIn("name", response.data)
        self.assertIn("cpf", response.data)
        self.assertIn("gender", response.data)
        self.assertIn("date_birth", response.data)
        self.assertIn("cellphone", response.data)

    def test_client_address(self):
        """
        """

        # create new regular user
        valid_data = {
            "email": "regular2@regular.com",
            "password": "ASD123**",
            "password2": "ASD123**",
            "name": "João Lima",
            "cpf": "929.853.569-46",
            "gender": "M",
            "date_birth": "2000-01-01",
            "cellphone": "(79) 98899-8899",
        }

        response = self.client.post("/signup", valid_data, format="json")

        # login
        self.client.login(username="regular2@regular.com", password="ASD123**")

        # list test
        response = self.client.get("/client-address", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

        # create test
        payload = {
            "main": True,
            "name": "Meu apartamento",
            "postal_code": "49070-000",
            "address": "Rua marcos feliciano",
            "district": "Jabotiana",
            "number": "200",
            "city": "São Paulo",
            "state": "SP",
            "complement": "",
            "landmark": "",
        }
        response = self.client.post("/client-address", payload, format="json")
        address = ClientAddress.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(address.postal_code, "49070-000")

        # list test
        response = self.client.get("/client-address", format="json")
        self.assertEqual(len(response.data), 1)

        # read test
        response = self.client.get(f"/client-address/{address.pk}", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # update test
        payload["postal_code"] = "49070-001"
        response = self.client.put(
            f"/client-address/{address.pk}", payload, format="json"
        )
        address.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(address.postal_code, "49070-001")

        # ==================================
        # create new regular user permissions
        # ==================================
        valid_data = {
            "email": "regular3@regular.com",
            "password": "ASD123**",
            "password2": "ASD123**",
            "name": "João Lima",
            "cpf": "929.853.569-46",
            "gender": "M",
            "date_birth": "2000-01-01",
            "cellphone": "(79) 98899-8899",
        }

        response = self.client.post("/signup", valid_data, format="json")

        # login
        self.client.login(username="regular3@regular.com", password="ASD123**")

        # list test on new regular user
        response = self.client.get("/client-address", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

        # read test on new regular user
        response = self.client.get(f"/client-address/{address.pk}", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # update test on new regular user
        response = self.client.put(
            f"/client-address/{address.pk}", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # create test on new regular user
        response = self.client.post("/client-address", payload, format="json")
        new_address_id = response.data.get("id")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # list test on new regular user
        response = self.client.get("/client-address", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # delete test
        response = self.client.delete(
            f"/client-address/{new_address_id}", format="json"
        )
        address = ClientAddress.objects.get(pk=new_address_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(address.is_deleted, True)
        self.assertEqual(address.date_deleted is not None, True)

