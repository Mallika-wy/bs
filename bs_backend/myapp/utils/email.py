from flask import current_app
import smtplib
from email.message import EmailMessage
import ssl


def send_email(data):
    app_config = current_app.config
    mail_host = app_config['mail_host']         # 设置服务器
    mail_post = app_config['mail_post']
    mail_user = app_config['mail_user']     # 用户名
    mail_pass = app_config['mail_pass']      # 口令

    receiver = data['email']
    content = data['content']

    msg = EmailMessage()
    msg['subject'] = 'B/S 商品比价网站信息降价提示'
    msg['From'] = mail_user
    msg['To'] = receiver
    msg.set_content(content)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(mail_host, mail_post, context=context) as smtp:
        smtp.login(mail_user, mail_pass)
        smtp.send_message(msg)