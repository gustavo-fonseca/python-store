from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAPITests(APITestCase):
    def test_admin_permissions(self):
        """
        Make sure that only admin has permissions on userviewset
        """

        # create new admin user
        admin_user = User.objects.create_superuser(
            email="admin@admin.com", password="admin"
        )

        # login
        self.client.login(username="admin@admin.com", password="admin")

        # list test
        response = self.client.get("/users", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # read test
        response = self.client.get(f"/users/{admin_user.pk}", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # create test
        payload = {
            "email": "admin2@admin.com",
            "password": "admin",
            "is_superuser": True,
            "is_active": True,
        }
        response = self.client.post("/users", payload, format="json")
        admin2_user = User.objects.filter(email="admin2@admin.com").first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(admin2_user)
        self.assertEqual(admin2_user.is_superuser, True)
        self.assertEqual(admin2_user.is_active, True)

        # update test
        payload = {
            "email": "admin3@admin.com",
            "is_superuser": False,
            "is_active": True,
        }
        response = self.client.put(
            f"/users/{admin2_user.pk}", payload, format="json"
        )
        admin2_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin2_user.is_superuser, False)
        self.assertEqual(admin2_user.is_active, True)

        # delete test
        response = self.client.delete(
            f"/users/{admin2_user.pk}", payload, format="json"
        )
        admin2_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(admin2_user.is_active, False)

    def test_non_admin_permissions(self):
        """
        Make sure that regular user has not permissions on userviewset
        """

        # create new regular user
        regular_user = User.objects.create_user(
            email="regular@regular.com", password="regular"
        )

        # login
        self.client.login(username="regular@regular.com", password="regular")

        # list test
        response = self.client.get("/users", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # read test
        response = self.client.get(f"/users/{regular_user.pk}", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # create test
        response = self.client.post("/users", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update test
        response = self.client.put(f"/users/{regular_user.pk}", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete test
        response = self.client.delete(f"/users/{regular_user.pk}", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_forget_password(self):
        """
        Make sure forget password actions is working
        """
        regular_user = User.objects.create_user(
            email="recoveremail@recoveremail123.com", password="recoveremail"
        )

        # forget password test
        payload = {"email": "recoveremail@recoveremail123.com"}
        response = self.client.post("/forget-password", payload, format="json")
        regular_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(regular_user.password_reset_token is None)
        self.assertFalse(regular_user.password_reset_token_expiration_datetime is None)

        # reset password test
        payload = {
            "password": "week",
            "token": regular_user.password_reset_token,
        }
        response = self.client.post("/reset-password", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "password": "AER123$123",
            "token": regular_user.password_reset_token,
        }
        response = self.client.post("/reset-password", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        regular_user.refresh_from_db()
        self.assertIsNone(regular_user.password_reset_token)
        self.assertIsNone(regular_user.password_reset_token_expiration_datetime)
