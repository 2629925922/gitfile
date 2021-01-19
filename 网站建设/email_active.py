from flask import Flask
from flask_mail import Mail,Message

app = Flask(__name__)
mail = Mail(app)

MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = "587"
MAIL_USE_TLS = True
MAIL_USERNAME = "2629925922@qq.com"
MAIL_PASSWORD = "mhp2629925922."
MAIL_DEFAULT_SENDER = "2629925922@qq.com"
