import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.credentials import FROM_EMAIL, PASSWORD


def send_email(to_email: str):
    msg = MIMEMultipart()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "simple email in python"
    message = (
        """Activation email\nConfirms that you have registered in Password Manager"""
    )
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP("smtp.gmail.com", 587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login(FROM_EMAIL, PASSWORD)

    mailserver.sendmail(FROM_EMAIL, to_email, msg.as_string())

    mailserver.quit()
