from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from client.models import ClientAddress

User = get_user_model()


class ClientAddressTests(APITestCase):
    def setUp(self):
        self.valid_client_data = {
            "email": "regular@regular.com",
            "password": "ASD123**",
            "password2": "ASD123**",
            "name": "João Lima",
            "cpf": "929.853.569-46",
            "gender": "M",
            "date_birth": "2000-01-01",
            "cellphone": "(79) 98899-8899",
        }
        self.valid_address_payload = {
            "main": True,
            "name": "Meu apartamento",
            "postal_code": "49070-000",
            "address": "Rua marcos feliciano",
            "district": "Jabotiana",
            "number": "200",
            "city": "São Paulo",
            "state": "SP",
            "complement": "",
            "landmark": "Próximo a academia x"
        }

        # new user
        self.client.post(reverse("signup-list"), self.valid_client_data)

        # login
        self.client.login(
            username=self.valid_client_data["email"],
            password=self.valid_client_data["password"]
        )

        # new address
        response = self.client.post(reverse("clientaddress-list"), self.valid_address_payload)
        self.address = address = ClientAddress.objects.get(pk=response.data.get("id"))

    def test_list_address(self):
        """
        Ensure we can list address' object
        """
        response = self.client.get(reverse("clientaddress-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_address(self):
        """
        Ensure we can retrieve our address' object
        """
        response = self.client.get(reverse("clientaddress-detail", args=[self.address.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_address(self):
        """
        Ensure we can create address' object
        """
        response = self.client.post(reverse("clientaddress-list"), self.valid_address_payload)
        address = ClientAddress.objects.get(pk=response.data.get("id"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(address.main, self.valid_address_payload.get("main"))
        self.assertEqual(address.name, self.valid_address_payload.get("name"))
        self.assertEqual(address.postal_code, self.valid_address_payload.get("postal_code"))
        self.assertEqual(address.address, self.valid_address_payload.get("address"))
        self.assertEqual(address.district, self.valid_address_payload.get("district"))
        self.assertEqual(address.number, self.valid_address_payload.get("number"))
        self.assertEqual(address.city, self.valid_address_payload.get("city"))
        self.assertEqual(address.state, self.valid_address_payload.get("state"))
        self.assertEqual(address.complement, self.valid_address_payload.get("complement"))
        self.assertEqual(address.landmark, self.valid_address_payload.get("landmark"))

    def test_update_address(self):
        """
        Ensure we can update address' object
        """
        update_payload = {
            "main": False,
            "name": "Meu novo apartamento",
            "postal_code": "10070-001",
            "address": "Rua marta feliciana",
            "district": "Morumbi",
            "number": "340",
            "city": "São Paulo",
            "state": "SP",
            "complement": "Blc. 11",
            "landmark": "Próximo a quadra de esporte"
        }

        response = self.client.put(
            reverse("clientaddress-detail", args=[self.address.pk]),
            update_payload
        )
        self.address.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.address.main, update_payload.get("main"))
        self.assertEqual(self.address.name, update_payload.get("name"))
        self.assertEqual(self.address.postal_code, update_payload.get("postal_code"))
        self.assertEqual(self.address.address, update_payload.get("address"))
        self.assertEqual(self.address.district, update_payload.get("district"))
        self.assertEqual(self.address.number, update_payload.get("number"))
        self.assertEqual(self.address.city, update_payload.get("city"))
        self.assertEqual(self.address.state, update_payload.get("state"))
        self.assertEqual(self.address.complement, update_payload.get("complement"))
        self.assertEqual(self.address.landmark, update_payload.get("landmark"))

    def test_soft_delete_address(self):
        """
        Ensure we can soft delete address' object
        """
        response = self.client.delete(
            reverse("clientaddress-detail", args=[self.address.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.address.refresh_from_db()
        self.assertEqual(self.address.is_deleted, True)
        self.assertIsNotNone(self.address.date_deleted)


    def test_address_permissions(self):
        """
        Ensure only the owner can list, retrieve, create, update and delete address
        """
        # new client
        self.valid_client_data["email"] = "new_regular@regular.com"
        self.client.post(reverse("signup-list"), self.valid_client_data)

        self.client.login(
            username=self.valid_client_data["email"],
            password=self.valid_client_data["password"]
        )

        # list test
        response = self.client.get(reverse("clientaddress-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

        # retrieve test
        response = self.client.get(reverse("clientaddress-detail", args=[self.address.pk]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # update test
        response = self.client.put(
            reverse("clientaddress-detail", args=[self.address.pk]),
            self.valid_address_payload
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # delete test
        response = self.client.delete(
            reverse("clientaddress-detail", args=[self.address.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
