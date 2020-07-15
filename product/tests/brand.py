from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from product.models import Brand

User = get_user_model()


class BrandTests(APITestCase):

    def setUp(self):
        self.valid_payload = {
            "name": "Adidas",
            "is_active": True
        }
        self.invalid_payload = {
            "idade": "Puma",
            "is_active": True
        }

        # create admin user
        self.admin_user = User.objects.create_superuser(
            email="admin@admin.com",
            password="admin"
        )

        # login
        self.client.login(username="admin@admin.com", password="admin")

        # create new brand
        response = self.client.post(reverse("brand-list"), self.valid_payload)
        self.brand = Brand.objects.get(pk=response.data.get("id"))

    def test_list_brand(self):
        """
        Ensure we can list brand
        """
        response = self.client.get(reverse("brand-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_brand(self):
        """
        Ensure we can retrieve brand
        """
        response = self.client.get(
            reverse("brand-detail", args=[self.brand.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_brand(self):
        """
        Ensure we can create brand
        """
        response = self.client.post(reverse("brand-list"), self.valid_payload)
        brand = Brand.objects.get(pk=response.data.get("id"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(brand.name, self.valid_payload.get("name"))
        self.assertEqual(brand.is_active, self.valid_payload.get("is_active"))

        response = self.client.post(reverse("brand-list"), self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_brand(self):
        """
        Ensure we can update brand
        """
        self.valid_payload["name"] = "Nike"
        self.valid_payload["is_active"] = False

        response = self.client.put(
            reverse("brand-detail", args=[self.brand.pk]),
            self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_brand(self):
        """
        Ensure we can delete brand
        """
        response = self.client.delete(
            reverse("brand-detail", args=[self.brand.pk]))
        self.brand.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.brand.is_active, False)

    def test_brand_permissions(self):
        """
        Ensure that only admin can list, create, delete, update, retrieve
        and delete brand objects
        """
        regular_user_payload = {
            "email": "regular@regular.com",
            "password": "ASD123**",
            "password2": "ASD123**",
            "name": "João Lima",
            "cpf": "929.853.569-46",
            "gender": "M",
            "date_birth": "2000-01-01",
            "cellphone": "(11) 98899-8899"
        }
        self.client.post(reverse("signup-list"), regular_user_payload)
        self.client.login(username="regular@regular.com", password="ASD123**")

        # list test
        response = self.client.get(reverse("brand-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve test
        response = self.client.get(
            reverse("brand-detail", args=[self.brand.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # create test
        response = self.client.post(reverse("brand-list"), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update test
        response = self.client.put(
            reverse("brand-detail", args=[self.brand.pk]), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete test
        response = self.client.delete(
            reverse("brand-detail", args=[self.brand.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
