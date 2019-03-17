import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

from tornado import gen

def send_mail(dict_body):
    body = (
        'メールフォームから受信しました\n\n'
      + '[Mail]\n'
      + '{}\n'
      + '[Content]\n'
      + '{}'
    ).format(dict_body['mail'], dict_body['content'])

    from_mail = os.environ['MAIL_ADDRESS']
    from_password = os.environ['MAIL_PASSWORD']
    to_mail = os.environ['MAIL_ADDRESS']

    message = MIMEText(body)
    message['Subject'] = '[しずおかごみ出しNavi]メールフォーム'
    message['From'] = from_mail
    message['To'] = to_mail
    message['Date'] = formatdate()

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.starttls()
    gmail.login(from_mail, from_password)
    gmail.sendmail(from_mail, to_mail, message.as_string())
    gmail.close()
