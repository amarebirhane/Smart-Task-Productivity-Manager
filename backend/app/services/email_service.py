import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings

logger = logging.getLogger("app.email")

class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, body: str):
        """
        Sends an email using the configured SMTP server.
        This should be run as a BackgroundTask.
        """
        if not all([settings.SMTP_HOST, settings.SMTP_PORT, settings.SMTP_USER, settings.SMTP_PASSWORD]):
            logger.warning(f"SMTP not configured. Email to {to_email} was not sent. Subject: {subject}")
            return

        try:
            message = MIMEMultipart()
            message["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "html"))

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(message)
            
            logger.info(f"Email sent successfully to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")

    @staticmethod
    def send_simulated_email(to_email: str, subject: str, body: str):
        # Keep for backward compatibility or testing if needed, but mark as deprecated
        logger.info(f"SIMULATED EMAIL: To: {to_email}, Subject: {subject}")

email_service = EmailService()
