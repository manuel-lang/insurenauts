from api.models import EmailBody
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
import os


def send_email(body: EmailBody) -> dict[str, str]:
    """Send an email as defined in EmailBody"""
    msg = MIMEText(body.message)
    msg["subject"] = body.subject
    with SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(
            os.environ.get("SMTP_EMAIL_ADDRESS", ""),
            os.environ.get("SMTP_PASSWORD", ""),
        )
        smtp_server.sendmail(
            os.environ.get("SMTP_EMAIL_ADDRESS", ""), [body.to], msg.as_string()
        )
    return {"message": "Email sent successfully"}
