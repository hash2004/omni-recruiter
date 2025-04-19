import os
import smtplib
from email.message import EmailMessage

def send_email(to_email: str, body: str, subject: str = ""):
    """
    Send an email using SMTP and an app password.

    Args:
        to_email:   Recipient's email address.
        body:       The plaintext (or HTML) content of your email.
        subject:    Subject line for the email (optional).
    """
    # Load configuration from environment (or replace with string literals)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "nadeemhashim7@gmail.com"      # e.g. yourname@gmail.com
    app_password = "wzqu uttr svgy adwp" # your Gmail app password

    # Build the email
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # Send it
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

"""
# Example usage:
if __name__ == "__main__":
    # ensure these are set in your environment:
    # export SENDER_EMAIL="you@gmail.com"
    # export EMAIL_APP_PASSWORD="abcd efgh ijkl mnop"
    send_email(
        to_email="aaqibanazir@gmail.com",
        subject="Hello from Python!",
        body="This is a test sent via SMTP with an app password."
    )
"""