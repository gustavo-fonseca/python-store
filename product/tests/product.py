import tempfile

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from product.models import Product, Category, Image

User = get_user_model()


class ProductTests(APITestCase):

    def setUp(self):
        self.valid_payload = {
            "brand": "",
            "categories": [],
            "images": [],
            "name": "Iphone X",
            "is_active": True,
            "short_description": "short desc",
            "full_description": "full desc",
            "color_hex": "#003344",
            "price": 5200.90,
            "old_price": 5600.00,
            "cost_price": 3000,
            "inventory": 30,
            "weight_grams": 400,
            "length_mm": 250,
            "width_mm": 140,
            "thickness_mm": 100
        }

        # create admin user
        self.admin_user = User.objects.create_superuser(
            email="admin@admin.com",
            password="admin"
        )

        # login
        self.client.login(username="admin@admin.com", password="admin")

        # create product's category
        self.category = Category.objects.create(name="Adidas")
        self.valid_payload["categories"].append(self.category.pk)

        # create product's image
        self.image = Image.objects.create(file=tempfile.mkdtemp())
        self.valid_payload["images"].append(self.image.pk)

        # create new product
        response = self.client.post(
            reverse("product-list"), self.valid_payload)
        self.product = Product.objects.get(pk=response.data.get("id"))

    def test_list_product(self):
        """
        Ensure we can list product
        """
        response = self.client.get(reverse("product-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)

    def test_retrieve_product(self):
        """
        Ensure we can retrieve product
        """
        response = self.client.get(
            reverse("product-detail", args=[self.product.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        """
        Ensure we can create product
        """
        response = self.client.post(
            reverse("product-list"), self.valid_payload)
        product = Product.objects.get(pk=response.data.get("id"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(product.name, self.valid_payload.get("name"))
        self.assertEqual(
            product.is_active, self.valid_payload.get("is_active"))

        invalid_payload = self.valid_payload
        invalid_payload["images"] = []
        response = self.client.post(
            reverse("product-list"), invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        """
        Ensure we can update product
        """
        self.valid_payload["name"] = "Ultraboost 20"
        self.valid_payload["is_active"] = False

        response = self.client.put(
            reverse("product-detail", args=[self.product.pk]),
            self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        """
        Ensure we can delete product
        """
        response = self.client.delete(
            reverse("product-detail", args=[self.product.pk]))
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.product.is_active, False)

    def test_product_permissions(self):
        """
        Ensure that only admin can list, create, delete, update, retrieve
        and delete product objects
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
        response = self.client.get(reverse("product-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve test
        response = self.client.get(
            reverse("product-detail", args=[self.product.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # create test
        response = self.client.post(
            reverse("product-list"), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update test
        response = self.client.put(
            reverse("product-detail", args=[self.product.pk]),
            self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete test
        response = self.client.delete(
            reverse("product-detail", args=[self.product.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
