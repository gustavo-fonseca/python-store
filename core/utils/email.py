import threading

from typing import Dict, List

from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings


class Email:
    """
    This class provides a solution to send html email inside a thread process
    to avoid blocking the request
    """

    def __init__(self, subject: str, from_name: str, from_email: str, to_name: str,
                 to_email: str, template_path: str, template_context: Dict[str, any]) -> None:
        self.subject = subject
        self.from_name = from_name
        self.from_email = from_email
        self.to_name = to_name
        self.to_email = to_email
        self.template_path = template_path
        self.template_context = template_context

    def send(self):
        from_email = f"{self.from_name} <{self.from_email}>"
        to_email = [self.to_email]

        # update template context with default data
        self.template_context.update(
            {
                "hostname": settings.FRONTEND_URL,
                "to_name": self.to_name,
                "to_email": self.to_email,
            }
        )

        # getting a string from a django-html template
        html_message = get_template(self.template_path).render(self.template_context)

        # calling the thread process
        tread = threading.Thread(
            target=self.send_email_on_thread,
            args=(self.subject, html_message, to_email, from_email),
        )
        tread.start()

    def send_email_on_thread(
        self, subject: str, message: str, to: List[str], from_email: str) -> None:
        """
        Sending email
        """
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = "html"
        msg.send()
