from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.session import sessionmaker


app = Flask(__name__)

app.secret_key = "dfasfasf32121sdaf"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:3306/mhp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class user(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(24))
    email = db.Column(db.String(24))
    password = db.Column(db.String(24))
    image = db.Column(db.String(80))
    age = db.Column(db.Integer)
    national = db.Column(db.String(20))
    place = db.Column(db.String(20))
    phnoe = db.Column(db.String(11))
    message = db.Column(db.String(200))
    city = db.Column(db.String(30))
    genter = db.Column(db.String(10))
    active = db.Column(db.String(50))
    # quote = db.Column(db.String(200))



