from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAPITests(APITestCase):

    def setUp(self):
        self.valid_payload = {
            "email": "new_admin@admin.com",
            "password": "admin",
            "is_superuser": True,
            "is_active": True
        }
        self.invalid_payload = {
            "email2": "new_admin@admin.com",
            "password": "admin",
            "is_superuser": True,
            "is_active": True
        }
        self.admin_user = User.objects.create_superuser(
            email="admin@admin.com", password="admin"
        )
        self.regular_user = User.objects.create_user(
            email="regular@regular.com", password="regular"
        )

    def test_create_user(self):
        """
        Ensure only admin users can create a new user object.
        """

        # Regular user
        self.client.login(username="regular@regular.com", password="regular")

        response = self.client.post(reverse("user-list"), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user
        self.client.login(username="admin@admin.com", password="admin")

        response = self.client.post(reverse("user-list"), self.valid_payload)
        new_admin_user = User.objects.get(email="new_admin@admin.com")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_admin_user.is_superuser, True)
        self.assertEqual(new_admin_user.is_active, True)

    def test_list_user(self):
        """
        Ensure only admin users can list users object.
        """

        # Regular user
        self.client.login(username="regular@regular.com", password="regular")
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user
        self.client.login(username="admin@admin.com", password="admin")
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user(self):
        """
        Ensure only admin users can retrieve users object.
        """

        # Regular user
        self.client.login(username="regular@regular.com", password="regular")
        response = self.client.get(
            reverse("user-detail", args=[self.admin_user.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user
        self.client.login(username="admin@admin.com", password="admin")
        response = self.client.get(
            reverse("user-detail", args=[self.admin_user.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        """
        Ensure only admin users can update users object.
        """

        # Regular user
        self.client.login(username="regular@regular.com", password="regular")
        response = self.client.put(
            reverse("user-detail", args=[self.admin_user.pk]),
            self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user
        self.client.login(username="admin@admin.com", password="admin")
        response = self.client.put(
            reverse("user-detail", args=[self.admin_user.pk]),
            self.valid_payload
        )
        self.admin_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.admin_user.email, self.valid_payload.get("email"))

    def test_soft_delete_user(self):
        """
        Ensure only admin users can soft delete users object.
        """

        # Regular user
        self.client.login(username="regular@regular.com", password="regular")
        response = self.client.delete(
            reverse("user-detail", args=[self.admin_user.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user
        self.client.login(username="admin@admin.com", password="admin")
        response = self.client.delete(
            reverse("user-detail", args=[self.admin_user.pk]))

        self.admin_user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.admin_user.is_active, False)

    def test_forget_reset_password_action(self):
        """
        Ensure we can use forget and reset password action
        """

        # forget action
        payload = {"email": "regular@regular.com"}
        response = self.client.post(reverse("user-forget-password"), payload)
        self.regular_user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(self.regular_user.password_reset_token)
        self.assertIsNotNone(
            self.regular_user.password_reset_token_expiration_datetime)

        # reset action
        payload = {
            "password": "AER123$123",
            "token": self.regular_user.password_reset_token
        }
        response = self.client.post(reverse("user-reset-password"), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.regular_user.refresh_from_db()
        self.assertIsNone(self.regular_user.password_reset_token)
        self.assertIsNone(
            self.regular_user.password_reset_token_expiration_datetime)
