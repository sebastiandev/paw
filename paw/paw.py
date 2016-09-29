import requests
import smtplib
import re
import os
from lxml import html
from io import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email import charset
from email.generator import Generator

URL = "https://promociones-aereas.com.ar"
KEYWORDS = ['costa rica', 'panama', 'caribe']


SMTP_AWS_USER = 'AKIAIG5B2URLQZ4UUKPQ'
SMTP_AWS_SERVER = 'email-smtp.us-west-2.amazonaws.com'


def send_email(msg):
    from_address = 'devsebas@gmail.com'
    recipient = ["superpacko@gmail.com", "grillo.svy@gmail.com"]
    subject = 'Promociones Aereas'

    # Default encoding mode set to Quoted Printable. Acts globally!
    charset.add_charset('utf-8', charset.QP, charset.QP, 'utf-8')

    # 'alternative’ MIME type – HTML and plain text bundled in one e-mail message
    mime_msg = MIMEMultipart('alternative')
    mime_msg['Subject'] = "%s" % Header(subject, 'utf-8')
    # Only descriptive part of recipient and sender shall be encoded, not the email address
    mime_msg['From'] = "<%s>" % (Header(from_address, 'utf-8'))
    mime_msg['To'] = ','.join(["<{}>".format(Header(recip, 'utf-8'))  for recip in recipient])

    textpart = MIMEText(msg, 'plain', 'UTF-8')
    mime_msg.attach(textpart)

    # Create a generator and flatten message object to 'file’
    str_io = StringIO()
    g = Generator(str_io, False)
    g.flatten(mime_msg)

    #s = smtplib.SMTP('smtp.gmail.com', 587)
    s = smtplib.SMTP(SMTP_AWS_SERVER, 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    #s.login("devsebas@gmail.com", os.getenv('GMAIL_PASS'))
    s.login(SMTP_AWS_USER, os.getenv('SMTP_AWS_PASS'))
    s.sendmail("", recipient, str_io.getvalue())


def check():
    req = requests.get(URL)
    tree = html.fromstring(req.content)
    mensaje = "Promociones con alguno de los keywords {}:".format(','.join(KEYWORDS))
    promociones = []

    for article in tree.xpath('//article'):
        title = article.xpath('.//header/h2/a/text()')
        if type(title) is list:
            title = ''.join(title)

        content = article.xpath('.//div/p/text()')
        if type(content) is list:
            content = ''.join(content)

        link = article.xpath('.//header/h2/a/@href')
        if type(link) is list:
            link = ''.join(link)

        post_date = article.xpath('.//header/h6/text()')
        if type(post_date) is list:
            post_date = ''.join(post_date)

        re_match = re.search(r"\d{2}/\d{2}/\d{4}", post_date)
        article_date = re_match.group() if re_match else ''

        # print("Checking article {} {} - {} ...".format(article_date, title, link))
        if any(k in content.lower() for k in KEYWORDS) or any(k in title.lower() for k in KEYWORDS):
            print("Found interesting post, sending email...")
            msg = "\r\n  - Link: {}\r\n    Date: {}\r\n    Title: {}\r\n    Post: {}\r\n"""\
                .format(link, article_date, title, content)
            promociones.append(msg)

    for promo in promociones:
        mensaje += "\r\n\r\n" + promo

    send_email(mensaje)
