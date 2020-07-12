import uuid, datetime

from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from core.utils.email import Email


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

    def forget_password(self, email):
        """
        Send an email with a link to resent password
        """
        user = self.filter(email=email).first()

        if user:
            user.password_reset_token = uuid.uuid4()
            user.password_reset_token_expiration_datetime = timezone.now() + datetime.timedelta(
                hours=3
            )
            user.save()

            email = Email(
                subject="Home Store - Forgotten Password?",
                from_name="Home Store",
                from_email="contato@gustavofonseca.com.br",
                to_name="",
                to_email=email,
                template_path="email/forget-password.html",
                template_context={"token": user.password_reset_token},
            )

            email.send()

    def reset_password(self, password_reset_token, new_raw_password):
        """
        TODO:
        """
        user = self.filter(password_reset_token=password_reset_token).first()
        now = timezone.now()

        if user and now < user.password_reset_token_expiration_datetime:
            user.password_reset_token = None
            user.password_reset_token_expiration_datetime = None
            user.set_password(new_raw_password)
            user.save()
            return True

        return False
