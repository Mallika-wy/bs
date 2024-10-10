from flask import make_response, jsonify
import smtplib
from email.message import EmailMessage
import ssl


class ApiResult:
    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data

    def make_response(self):
        response = make_response(jsonify(self.to_dict()), self.code)
        response.headers['Content-Type'] = 'application/json'
        return response

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
            'data': self.data
        }


my_config = {
            'interval': 10,
            'pages': 3,
            'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:2004wangyang@localhost/bs',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }


def send_email(data):
    mail_host = "smtp.163.com"           # 设置服务器
    mail_post = 465
    mail_user = "18205098642@163.com"     # 用户名
    mail_pass = "ZWqHSNX6XvtBiXXb"      # 口令

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
