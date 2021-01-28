from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.session import sessionmaker
from datetime import datetime

app = Flask(__name__)

app.secret_key = "dfasfasf32121sdaf"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:3306/mhp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# class Follow(db.Model):
#     __tablename__='follows'
#     follower_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
#     followed_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
#     timestamp = db.Column(db.DateTime,default=datetime.now())


followers = db.Table("followers",
    db.Column('follower_id',db.Integer,db.ForeignKey('users.id')),
    db.Column('followed_id',db.Integer,db.ForeignKey('users.id'))
)

class messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200))
    message = db.Column(db.String(1000))
    image = db.Column(db.String(90))
    name_id = db.Column(db.Integer,db.ForeignKey('users.id'))

class user(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(150))
    image = db.Column(db.String(80))
    age = db.Column(db.Integer)
    national = db.Column(db.String(20))
    place = db.Column(db.String(20))
    phnoe = db.Column(db.String(11))
    message = db.Column(db.String(200))
    city = db.Column(db.String(30))
    genter = db.Column(db.String(10))
    active = db.Column(db.String(50))
    message_time = db.Column(db.String(80))
    messages = db.relationship('messages',backref='users')
    # followerd = db.relationship(
    #     'user',secondary=followers,
    #     primaryjoin=(followers.c.follower_id == id),
    #     secondaryjoin=(followers.c.followed_id == id),
    #     backref=db.backref('followers',lazy=True),lazy=True
    # )

    followed = db.relationship('user',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    # def __init__(self,User):
    #     self.User = User
    # def follow(self,User):
    #     if not self.is_following(self.User):
    #         self.followerd.append(self.User)
    # def unfollow(self,User):
    #     if self.is_following(self.User):
    #         self.followerd.remove(self.User)
    # def is_following(self,User):
    #     return self.followerd.filter(followers.c.followed_id == User.id).count() > 0

    def follow(self, User):
        if not self.is_following(User):
            self.followed.append(User)
            return self

    def unfollow(self, User):
        if self.is_following(User):
            self.followed.remove(User)
            return self

    def is_following(self, User):
        return self.followed.filter(followers.c.followed_id == User.id).count()


