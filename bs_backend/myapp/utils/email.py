from flask import current_app
import smtplib
from email.message import EmailMessage
import ssl


def send_email(data):
    app_config = current_app.config
    mail_host = app_config['MAIL_HOST']         # 设置服务器
    mail_port = app_config['MAIL_PORT']
    mail_user = app_config['MAIL_USER']     # 用户名
    mail_pass = app_config['MAIL_PASS']      # 口令

    receiver = data['email']
    content = data['content']

    msg = EmailMessage()
    msg['subject'] = 'B/S 商品比价网站信息降价提示'
    msg['From'] = mail_user
    msg['To'] = receiver
    msg.set_content(content)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(mail_host, mail_port, context=context) as smtp:
        smtp.login(mail_user, mail_pass)
        smtp.send_message(msg)