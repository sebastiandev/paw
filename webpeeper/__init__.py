import os


URL = "https://promociones-aereas.com.ar"
KEYWORDS = ['costa rica', 'panama', 'caribe']
SMTP_AWS_USER = 'AKIAIG5B2URLQZ4UUKPQ'
SMTP_AWS_SERVER = 'email-smtp.us-west-2.amazonaws.com'
SMTP_GMAIL_SERVER = 'smtp.gmail.com'
SMTP_GMAIL_USER = 'devsebas@gmail.com'


def email_credentials():
    if os.getenv('SMTP_AWS_PASS'):
        return SMTP_AWS_SERVER, SMTP_AWS_USER, os.getenv('SMTP_AWS_PASS')

    elif os.getenv('GMAIL_PASS'):
        return SMTP_GMAIL_SERVER, SMTP_GMAIL_USER, os.getenv('GMAIL_PASS')

    else:
        raise Exception("Couldn't find any email credentials on the environment")
