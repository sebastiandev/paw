import smtplib
from io import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email import charset
from email.generator import Generator


class Emailer(object):

    def __init__(self, server, user, password, port=587):
        self._smtp = smtplib.SMTP(server, port)
        self._smtp.ehlo()
        self._smtp.starttls()
        self._smtp.ehlo()
        self._smtp.login(user, password)

        # Default encoding mode set to Quoted Printable. Acts globally!
        charset.add_charset('utf-8', charset.QP, charset.QP, 'utf-8')

    def send(self, from_address, to_address, subject, msg):
        if type(to_address) is str:
            to_address = to_address.split(',')

        # 'alternative’ MIME type – HTML and plain text bundled in one e-mail message
        mime_msg = MIMEMultipart('alternative')
        mime_msg['Subject'] = "{}".format(Header(subject, 'utf-8'))

        # Only descriptive part of recipient and sender shall be encoded, not the email address
        mime_msg['From'] = "<{}>".format((Header(from_address, 'utf-8')))
        mime_msg['To'] = ','.join(["<{}>".format(Header(recip, 'utf-8'))  for recip in to_address])

        textpart = MIMEText(msg, 'plain', 'UTF-8')
        mime_msg.attach(textpart)

        # Create a generator and flatten message object to 'file’
        str_io = StringIO()
        Generator(str_io, False).flatten(mime_msg)

        self._smtp.sendmail(from_address, to_address, str_io.getvalue())

