from flask import Flask,render_template,session,request,abort,make_response,redirect,url_for,flash
# from werkzeug.routing import BaseConverter
from create_sql import db,user,messages
import os
import random
from flask_wtf import CSRFProtect
# import email_active
import uuid
from flask_mail import Mail,Message
# from flask_uploads import *
# import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from flask_wtf import FlaskForm,CSRFProtect
from flask_wtf.file import FileAllowed,FileField,FileRequired
# ,CSRFProtect
from wtforms import StringField,PasswordField,HiddenField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError
import datetime
import time
# from modles import current_user


app = Flask(__name__)
# app.secret_key='sf131sad31f'
CSRFProtect(app)



# MAIL_SERVER = "smtp.qq.com"
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USERNAME = "2629925922@qq.com"
# MAIL_PASSWORD = "zqwaipprwasaeaae"
# MAIL_DEFAULT_SENDER = "2629925922@qq.com"
app.config["SECRET_KEY"] = "FJDOAJ548FADSF1A"
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True  # 这里要使用ssl
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_DEBUG'] = True  # 开启debug 查看报错信息
app.config['MAIL_USERNAME'] = "2629925922@qq.com"  # 这里填发送方的邮箱
app.config['MAIL_PASSWORD'] = "zqwaipprwasaeaae"  # 授权码不能用空格
app.config['MAIL_DEFAULT_SENDER'] = "2629925922@qq.com"

mail = Mail(app)

# def follow(username):
#     User = user.query.filter_by(name=username).first()
#     if not User:
#         return "用户不存在"
#     if current_user.is_following(user):
#         return "取消关注"
#     else:
#         return "关注"
    # current_user.follow(user)
    # return "已关注"

# #文件上传设置
# app.config['UPLOAD_PHOTOS_DEST'] = "./static/img"
# app.config['UPLOAD_PHOTOS_URL'] = "/static/img"
# # app.config['UPLOADED_PHOTOS_ALLOW'] = IMAGES
# photos = UploadSet('photo',IMAGES)
# configure_uploads(app,photos)
# patch_request_class(app,2 * 1024 * 1024)

#    # 正则匹配路由
# class MybaseConverter(BaseConverter):
#     def __init__(self,url_map,regx):
#         super(MybaseConverter,self).__init__(url_map)
#         self.regex = regx
#
# app.url_map.converters['re'] = MybaseConverter
# #@app.route("/user/<re('[0-9]{3}'):num>")
# @app.route('/user/<re("\d{3}"):num>')
# def user(num):
#     return "the number is {}".format


# class error(BaseConverter):
#     def __init__(self,url_map,regx):
#         super(error,self)__init__(url_map)
#         self.regx = regx
# app.url_map.converters['re'] = error
# @app.route("/<re('[a-z]{10}'):num>")
# def errors(num):
#     abort(404)
#     return "小子想渗透"
class regfrom(FlaskForm):
    # render_kw = {'class': 'name', 'placeholder': '请输入用户名'}
    # render_kw = {'class': 'password', 'placeholder': '请输入密码'}
    # , render_kw = {'class': 'password', 'placeholder': '请输入邮箱'}              #添加cssgenjs样式
    # , render_kw = {'class': 'active', 'placeholder': '请输入激活码'}
    username = StringField('用户名',validators=[DataRequired('用户名必须输入')])
    password = PasswordField('密码',validators=[DataRequired("密码必须输入")])
    email = StringField('邮箱',validators=[DataRequired("邮箱必须输入")])
    active = StringField('激活码',validators=[DataRequired("激活码必须输入")])
    file = FileField('upload image',validators=[FileRequired(),FileAllowed(['jpg','jpeg','gif','png','bmp'])])









#  在请求进入视图函数之前 做出响应，只执行一次
# @app.before_first_request
# def bfe():
#     return flash("欢迎来到制梦空间")

#  在请求进入视图函数之前 做出响应
@app.before_request
def be1():
    if request.path == "/login" or "/register" or "/register1":
        return None
    if not session.get("username"):
        return redirect("/login")
    return None

@app.route("/sy")
def sy():
    return render_template("sy.html")
@app.route("/pl")
def pl():
    name = session['username']
    object = user.query.all()
    return render_template("pl.html",object=object,name=name)
@app.route("/gr",methods=['GET','POST'])
def gr():
    if request.method == 'GET':
        return redirect(url_for("pl"))
    else:
        name = request.form.get("name")
        data = user.query.filter(user.name==name).all()
        for i in data:
            return render_template("gr.html",image=i.image,name=i.name)

# user = user()
@app.route("/gz",methods=['GET','POST'])
def gz():

    name = request.form.get("name")
    fun = request.form.get("follow")
    User = user.query.filter_by(name=name).first()

    if fun == "follow":
        if not User:
            flash("用户不存在")
        if user.is_following(User):
            flash("用户已关注")
        user.follow(User)
        flash("已关注")
    elif fun == "unfollow":
        if not User:
            flash("用户不存在")
        if not user.is_following(User):
            flash("你未关注该用户")
        user.unfollow(User)
        flash("已取消关注")


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html',name=session['username'])
    return redirect(url_for("login"))

# @app.route('/index',methods=["GET","POST"])
# def login():
#     form = regfrom()
#     if request.method == 'GET':
#         return render_template('from.html')
#     else:
#     #name = request.values.get("username")
#     #passwd = request.values.get("password")
#         # name = request.form.get("username")
#         # passwd = request.form.get("password")
#         name = form.username.data
#         passwd = form.password.data
#         #if name == "admin" and passwd == "123456":
#         if(name == "" or passwd == ""):
#             return "<script>alert('账户或密码为空！！');location.href='http://127.0.0.1:5000'</script>"
#         user_data = user.query.all()
#         for i in user_data:
#             if(i.name == name and i.password == passwd):
#                 session['username'] = name
#                 rep = make_response("success")
#                 rep.set_cookie(name,max_age=60)
#                 print(rep)
#                 return render_template('index.html', name=name)
#         #if name == "admin" and passwd == "123456":
#             #else:
#                 #error = "你的用户名跟密码错误"
#                 #abort(404)
#                 #return "你的账户跟密码错误！！"
#         return "<script>alert('账户或密码错误！！');location.href='http://127.0.0.1:5000'</script>"
#
#             return "<script>alert('用户名或密码为空，请返回!!');window.history.go(-1)</script>"
@app.route('/login',methods=["GET","POST"])
def login():
    form = regfrom()
    if request.method == 'GET':
        return render_template("login.html",form=form)
    else:
        username = form.username.data
        passwd = form.password.data
        # username = request.form.get('name')
        # passwd = request.form.get('password')
        if len(username)>1 and len(passwd)>1:
            data = user.query.filter(user.name==username).all()
            for i in data:
                if check_password_hash(i.password,passwd) == True:
                    data = user.query.filter(user.name==username).all()
                    for i in data:
                        session['id'] = i.id
                        session['username'] = username
                        return render_template("index.html",name=username)
                # return render_template("login.html")
                else:
                    return "<script>alert('登录失败，请返回!!');window.history.go(-1)</script>"
        else:
            return "<script>alert('用户名或密码为空，请返回!!');window.history.go(-1)</script>"
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



# @app.route("/email",methods=['GET','POST'])
# def email_active_code():
#     if request.method == 'GET':
#         return render_template("from.html")
#     else:
#         name = request.form.get("username")
#         email = request.form.get("email")
#         user_data = user.query.all()
#         for i in user_data:
#             if (i.name == name):
#                 return "<script>alert('用户名已存在！！');location.href='http://127.0.0.1:5000'</script>"
#         code = str(uuid.uuid1())[:6]
#         active_code = "flask active code is  " + code
#         # return "name: "+ name + ",email: " + email + ",code: " + active_code
#         message = Message(subject="hello flask email active code",recipients=[email],body=active_code)
#         # message = Message(subject='邮箱标题’, recipients=['接收方的邮箱'], body='发送的邮箱内容')
#         try:
#             mail.send(message)
#             data = user(name=name,email=email,active=code)
#             db.session.add(data)
#             db.session.commit()
#             # return "<script>alert('激活邮件已发送，请查收！');location.href='http://127.0.0.1:5000/register'</script>"
#
#         except:
#             return "<script>alert('邮件发送失败');window.history.go(-1)</script>"
#         return render_template("email1.html", name=name)
# @app.route("/register",methods=['GET','POST'])
# def register():
#     if request.method == 'GET':
#         return render_template("email1.html")
#     else:
#         name = request.form.get("username")
#         # email = request.form.get("email")
#         passwd = request.form.get("password")
#         active = request.form.get("active")
#         if (name == "" or passwd == "" or active == ''):
#             return "<script>alert('账户或密码或邮箱或激活码为空！！');location.href='http://127.0.0.1:5000'</script>"
#         # return "name: "+name+",password: "+passwd+",active: "+active
#         data_active = user.query.filter(user.name == name).all()
#         for i in data_active:
#             if(i.active != active):
#                 return "<script>alert('邮箱验证码输入有误!!');window.history.go(-1)</script>"
#         data = user.query.filter(user.name == name).all()
#         for i in data:
#             i.password = passwd
#             i.active = active
#             db.session.add(i)
#             db.session.commit()
#         # data = user(name=name,email=email,password=passwd)
#         # db.session.add(data)
#         # db.session.commit()
#         return "<script>alert('注册成功，请登录');location.href='http://127.0.0.1:5000'</script>"

@app.route('/logout')
def logout():
    #return render_template('from.html')
    print(session.pop('username'))
    return redirect(url_for('login'))
@app.route('/grjs')
def grjs():
    name = session['username']
    data = user.query.filter(user.name==name).all()
    for i in data:
        return render_template('grjs.html',name=name,age=i.age,national=i.national,place=i.place,phone=i.phnoe,email=i.email,image=i.image,genter=i.genter,city=i.city)
@app.route('/kysh')
def kysh():
    name = session['username']
    return render_template('kysh.html',name=name)
@app.route('/xx')
def xx():
    name = session['username']
    data = user.query.filter(user.id==session['id']).first()
    data = data.messages
    return render_template("xx.html",name=name,data=data)
@app.route('/zygh')
def zygh():
    name = session['username']
    return render_template('zygh.html',name=name)

_now = time.time()
@app.template_filter("time_filter")
def time_filter(time):
    # if not isinstance(time, datetime.datetime):
    #     return time
    # t1 = datetime.datetime.strptime(str(_now), "%Y-%m-%d %H:%M:%S.%f")
    # t2 = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    try :
        _period = float(_now) - float(time)
        _period = int(_period)
        if _period < 60:
            return "刚刚"
        elif 60 <= _period < 3600:
            return "%s分钟前" % int(_period / 60)
        elif 3600 <= _period < 86400:
            return "%s小时前" % int(_period / 3600)
        elif 86400 <= _period < 2592000:
            return "%s天前" % int(_period / 86400)
        else:
            return time.strftime('%Y-%m-%d %H:%M')
    except:
        return flash("请先登录")
@app.route('/lyb',methods=['GET','POST'])
def lyb():
    name = session['username']
    messageuser = []
    message = []
    # for i in messaeuser:
    #     messageuser.append(i.name)
    #     message.append(i.message)
    if request.method == 'GET':
        return render_template('lyb.html',name=name,object=object)
    message = request.form.get("message")
    data = user.query.filter(user.name==name).all()
    for i in data:
        # now = datetime.strptime(str(now),"%Y-%m-%d %H:%M:%S.%f")
        i.message = message
        i.message_time = _now
        db.session.add(i)
        db.session.commit()
        return "<script>alert('留言信息完成');window.history.go(-1)</script>"
@app.route("/htgl")
def htgl():
    name = session['username']
    data = user.query.filter(user.name==name).all()
    for i in data:
        # if(i.name == name):
        return render_template("htgl.html",image=i.image)
@app.route("/info",methods=['GET','POST'])
def info():
    name = session['username']
    if request.method == 'GET':
        return render_template("info.html")
    else:
        age = request.form.get("age")
        national = request.form.get("national")
        place = request.form.get("place")
        phone = request.form.get("phone")
        city = request.values.get("city")
        genter = request.form.get("genter")
        if(age == '' or national == '' or place == '' or phone == '' or city == '' or genter == ''):
            return "<script>alert('网站信息未填写完');window.history.go(-1)</script>"
        data = user.query.filter(user.name==name).all()
        for i in data:
            i.age = age
            i.national = national
            i.place = place
            i.phnoe = phone
            i.genter = genter
            i.city = city
            db.session.add(i)
            db.session.commit()
            return "<script>alert('网站信息设置成功');window.history.go(-1)</script>"

@app.route("/pass")
def passs():
    name = session['username']
    return render_template("pass.html",name=name)
@app.route("/passd",methods=["GET","POST"])
def passd():
    name = session['username']
    # if request.method == 'GET':
    #     return render_template("pass.html", name=name)
    # else:
    old_pass = request.form.get("oldpass")
    # old_pass = generate_password_hash(old_pass)
    new_pass = request.form.get("newpass")
    new_pass = generate_password_hash(new_pass)
    passwd_data = user.query.filter(user.name == name).all()
    for i in passwd_data:
        # if(old_pass == i.password):
        if check_password_hash(i.password, old_pass) == True:
            #new_passwd = user.query.filter(user.password == passwd_data).update({"password": new_pass})
            #print(new_passwd)
            i.password = new_pass
            db.session.add(i)
            db.session.commit()
            return "<script>alert('新密码设置成功');window.history.go(-1)</script>"
        else:
            return "<script>alert('旧密码输入有误!!');window.history.go(-1)</script>"
    return render_template("pass.html",name=name)

@app.route("/information")
def information():
    user_data = user.query.all()
    for i in user_data:
        if(session['username'] == i.name):
            name = i.name
            email = i.email
            passwd = i.password
            return render_template("information.html",name=name,email=email,passwd=passwd)
@app.route("/file",methods=['GET','POST'])
def txfile():
    name = session['username']
    image_type = ['.jpg','.png','.jpeg','.gif','.bmp']
    file_url = r"C:\Users\Think\Desktop\gitfile\网站建设\static\img"
    a = ''
    for i in range(1, 20):
        b = random.choice("asdfafoppmp1564132123")
        a += b
    if request.method == 'GET':
        data_image = user.query.filter(user.name == name).all()
        for i in data_image:
            return render_template("txfile.html", file=i.image)
        # return render_template("txfile.html",file="y.jpg")
    else:
        #file = request.files.get('image')
        file = request.files.get("image")
        filename = os.path.splitext(file.filename)
        if filename[1] in image_type:
             # return "<script>alert('上传文件不能为空');window.history.go(-1)</script>"
            filename = a + filename[1]
            file.save(os.path.join(file_url,filename))
            print("<script>window.history.go(-1)</script>")
            #print(render_template("htgl.html",file=file=file.filename))
            data = user.query.filter(user.name == name).all()
            for i in data:
                i.image = filename
                db.session.add(i)
                db.session.commit()
            # data = user(image=file.filename)
            # db.session.add(data)
            # db.session.commit()
            data_image = user.query.filter(user.name==name).all()
            for i in data_image:
                return render_template("txfile.html",file=i.image)
        else:
            return "<script>alert('上传文件不符合');window.history.go(-1)</script>"\

@app.route('/mfile',methods=['GET','POST'])
def mfile():
    if request.method == 'GET':
        render_template("message_file.html")
    else:
        file_url = r"C:\Users\Think\Desktop\gitfile\网站建设\static\img"
        image_type = ['.jpg', '.png', '.jpeg', '.gif', '.bmp']
        a = ''
        for i in range(1,20):
            b = random.choice("abcdefghijklmnoqprstuvwsvz12234567890")
            a += b
        title = request.form.get('title')
        data = messages.query.filter(messages.title==title).all()
        file = request.files.get("image")
        for i in image_type:
            filename = os.path.splitext(file.filename)
            filename = a + filename[1]
            file.save(os.path.join(file_url,filename))
            for i in data:
                i.image = filename
                db.session.add(i)
                db.session.commit()
                flash("上传完成")
                return redirect(url_for('xx'))
        else:
            return "<script>alert('文件上传失败');window.history.go(-1)</script>"

@app.route('/message',methods=['GET','POST'])
def message():
    name = session['username']
    if request.method == 'GET':
        return render_template("message.html")
    else:
        # dataname = user.query.filter(user.name==session['id']).all()
        title = request.form.get('title')
        message = request.form.get('message')
        # for i in dataname:
        data = messages(title=title,message=message,name_id=session['id'])
        db.session.add(data)
        db.session.commit()
        return render_template("message_file.html",title=title)

@app.route('/kjwz')
def kjwz():
    data = messages.query.all()
    return render_template("kjwz.html",data=data,name=session['username'])

@app.route('/wz/<title>',methods=['GET'])
def wz(title):
    data = messages.query.filter(messages.title==title).all()
    return render_template("wz.html",name=session['username'],data=data)


@app.errorhandler(404)
def error(e):
    print(e)
    return render_template("404.html")
# @app.errorhandler(500)
# def error(e):
#     print(e)
#     return render_template("500.html")
if __name__ == '__main__':
    # send_mail()
    app.run(debug=True)
