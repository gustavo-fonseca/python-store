import io
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from PIL import Image as ImagePillow

from product.models import Image

User = get_user_model()


class ImageTests(APITestCase):

    def generate_photo_file(self):
        file = io.BytesIO()
        image = ImagePillow.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = "test.png"
        file.seek(0)
        return file

    def setUp(self):
        self.valid_payload = {
            "file": self.generate_photo_file(),
            "is_active": True
        }
        self.invalid_payload = {
            "idade": "Celulares",
            "is_active": True
        }

        # create admin user
        self.admin_user = User.objects.create_superuser(
            email="admin@admin.com",
            password="admin"
        )

        # login
        self.client.login(username="admin@admin.com", password="admin")

        # create new image
        response = self.client.post(
            reverse("image-list"), self.valid_payload, format="multipart")
        self.image = Image.objects.get(pk=response.data.get("id"))

    def test_list_image(self):
        """
        Ensure we can list image
        """
        response = self.client.get(reverse("image-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_image(self):
        """
        Ensure we can retrieve image
        """
        response = self.client.get(
            reverse("image-detail", args=[self.image.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_image(self):
        """
        Ensure we can create image
        """
        self.valid_payload["file"] = self.generate_photo_file()
        response = self.client.post(
            reverse("image-list"), self.valid_payload, format="multipart")
        image = Image.objects.get(pk=response.data.get("id"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(image.is_active, self.valid_payload.get("is_active"))

        response = self.client.post(reverse("image-list"), self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_image(self):
        """
        Ensure we can update image
        """
        self.valid_payload["file"] = self.generate_photo_file()
        self.valid_payload["is_active"] = False

        response = self.client.put(
            reverse("image-detail", args=[self.image.pk]),
            self.valid_payload,
            format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_image(self):
        """
        Ensure we can delete image
        """
        response = self.client.delete(
            reverse("image-detail", args=[self.image.pk]))
        self.image.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.image.is_active, False)

    def test_image_permissions(self):
        """
        Ensure that only admin can list, create, delete, update, retrieve
        and delete image objects
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
        response = self.client.get(reverse("image-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve test
        response = self.client.get(
            reverse("image-detail", args=[self.image.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # create test
        response = self.client.post(reverse("image-list"), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update test
        response = self.client.put(
            reverse("image-detail", args=[self.image.pk]), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete test
        response = self.client.delete(
            reverse("image-detail", args=[self.image.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
