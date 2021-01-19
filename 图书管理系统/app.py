from flask import Flask,render_template,request,session,redirect,url_for
from flask_script import Manager
# from flask_login import LoginManager
from flask_mail import Mail,Message
from create_sql import db,user
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from flask_wtf import FlaskForm
# ,CSRFProtect
from wtforms import StringField,PasswordField,HiddenField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError

# import config
app = Flask(__name__)
manger = Manager(app)
# dl = LoginManager()
# dl.init__app(app)
class config():
    app.config["SECRET_KEY"] = "FJDOAJ548FADSF1A"
    app.config['MAIL_SERVER'] = 'smtp.qq.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True  # 这里要使用ssl
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_DEBUG'] = True  # 开启debug 查看报错信息
    app.config['MAIL_USERNAME'] = "2629925922@qq.com"  # 这里填发送方的邮箱
    app.config['MAIL_PASSWORD'] = "zqwaipprwasaeaae"  # 授权码不能用空格
    app.config['MAIL_DEFAULT_SENDER'] = "2629925922@qq.com"
    # WTF_CSRF_ENABLED = False
app.config.from_object('config')
# CSRFProtect(app)
mail = Mail(app)

class regfrom(FlaskForm):
    # render_kw = {'class': 'name', 'placeholder': '请输入用户名'}
    # render_kw = {'class': 'password', 'placeholder': '请输入密码'}
    # , render_kw = {'class': 'password', 'placeholder': '请输入邮箱'}
    # , render_kw = {'class': 'active', 'placeholder': '请输入激活码'}
    username = StringField('用户名',validators=[DataRequired('用户名必须输入')])
    password = PasswordField('密码',validators=[DataRequired("密码必须输入")])
    email = StringField('邮箱',validators=[DataRequired("邮箱必须输入")])
    active = StringField('激活码',validators=[DataRequired("激活码必须输入")])
# CSRFProtect(app)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        name = session['username']
        username = request.form.get('name')
        passwd = request.form.get('password')
        data = user.query.filter(user.name==username).all()
        for i in data:
            if check_password_hash(i.password,passwd) == True:
                return "登录成功"
            # return render_template("login.html")
        return "<script>alert('登录失败，请返回!!');window.history.go(-1)</script>"
@app.route('/register',methods=['GET','POST'])
def register():
    form = regfrom()
    # if form.validate_on_submit():                 #from.validate_on_submit()等价于   request.method==' post '  and  from.validate() ，validate是验证，验证表单信息
    if request.method == 'GET':
        return render_template("register.html", form=form)
    else:
        # # name = request.form.get("name")
        # # email = request.form.get("email")
        name = form.username.data
        email = form.email.data
        # return name + email
        if user.query.filter(user.name == name).first():
            # for i in users:
            #     if(i.name == name):
            return "<script>alert('用户名已存在');window.history.go(-1)</script>"
        if len(name) > 1 and len(email) > 1:
            code = str(uuid.uuid1())[:6]
            codes = "欢迎注册制梦空间，你的激活码是:  " + code
            message = Message(subject="制梦空间验证码", recipients=[email], body=codes)
            try:
                mail.send(message)
            except:
                return "<script>alert('发送失败!');window.history.go(-1)</script>"
            session['username'] = name
            data = user(name=name, email=email, active=code)
            db.session.add(data)
            db.session.commit()
            # return render_template("register1.html", name=name)
            return redirect(url_for("register1"))
        return "<script>alert('用户名或邮箱为空');window.history.go(-1)</script>"

@app.route('/register1',methods=['GET','POST'])
def register1():
    form = regfrom()
    # if form.validate_on_submit():
    if request.method == 'GET':
        return render_template('register1.html', form=form)
    else:
        name = session['username']
        # name = request.form.get("name")
        # passwd = request.form.get("password")
        # active = request.form.get("active")
        # name = form.username.data
        passwd = form.password.data
        active = form.active.data
        if len(name) > 1 and len(passwd) > 1 and len(active) > 1:
            passwd = generate_password_hash(passwd)
            data = user.query.filter(user.name == name).all()
            for i in data:
                if (i.active == active):
                    i.password = passwd
                    db.session.add(i)
                    db.session.commit()
                    return redirect(url_for("login"))
                else:
                    return "<script>alert('激活码错误!!');window.history.go(-1)</script>"
        return "<script>alert('密码或激活码为空');window.history.go(-1)</script>"
@app.errorhandler(404)
def error(e):
    print(e)
    return render_template("404.html")
@app.errorhandler(500)
def errors(a):
    print(a)
    return render_template("500.html")
if __name__ == '__main__':
    manger.run()
