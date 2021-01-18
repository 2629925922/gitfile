from flask import Flask,render_template,session,request,abort,make_response
# from werkzeug.routing import BaseConverter
from create_sql import db,user
import os
import random
from flask_wtf import CSRFProtect
# from flask_uploads import *

app = Flask(__name__)
app.secret_key='sf131sad31f'
CSRFProtect(app)
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





@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html',name=session['username'])
    return render_template('from.html')
@app.route('/index',methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template('from.html')
    else:
    #name = request.values.get("username")
    #passwd = request.values.get("password")
        name = request.form.get("username")
        passwd = request.form.get("password")
        #if name == "admin" and passwd == "123456":
        if(name == "" or passwd == ""):
            return "<script>alert('账户或密码为空！！');location.href='http://127.0.0.1:5000'</script>"
        user_data = user.query.all()
        for i in user_data:
            if(i.name == name and i.password == passwd):
                session['username'] = name
                rep = make_response("success")
                rep.set_cookie(name,max_age=60)
                print(rep)
                return render_template('index.html', name=name)
        #if name == "admin" and passwd == "123456":
            #else:
                #error = "你的用户名跟密码错误"
                #abort(404)
                #return "你的账户跟密码错误！！"
        return "<script>alert('账户或密码错误！！');location.href='http://127.0.0.1:5000'</script>"


@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("from.html")
    else:
        name = request.form.get("username")
        email = request.form.get("email")
        passwd = request.form.get("password")
        if (name == "" or passwd == "" or email == ""):
            return "<script>alert('账户或密码或邮箱为空！！');location.href='http://127.0.0.1:5000'</script>"
        user_data = user.query.all()
        for i in user_data:
            if(i.name == name):
                return "<script>alert('用户名已存在！！');location.href='http://127.0.0.1:5000'</script>"
        data = user(name=name,email=email,password=passwd)
        db.session.add(data)
        db.session.commit()
        return "<script>alert('注册成功，请登录');location.href='http://127.0.0.1:5000'</script>"
@app.route('/logout')
def logout():
    #return render_template('from.html')
    print(session.pop('username'))
    return render_template("from.html")
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
    return render_template('xx.html',name=name)
@app.route('/zygh')
def zygh():
    name = session['username']
    return render_template('zygh.html',name=name)
@app.route('/lyb',methods=['GET','POST'])
def lyb():
    name = session['username']
    messageuser = []
    message = []
    object = user.query.all()
    # for i in messaeuser:
    #     messageuser.append(i.name)
    #     message.append(i.message)
    if request.method == 'GET':
        return render_template('lyb.html',name=name,object=object)
    message = request.form.get("message")
    data = user.query.filter(user.name==name).all()
    for i in data:
        i.message = message
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
    new_pass = request.form.get("newpass")
    passwd_data = user.query.filter(user.name == name).all()
    for i in passwd_data:
        if(old_pass == i.password):
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
            return "<script>alert('上传文件不符合');window.history.go(-1)</script>"
@app.errorhandler(404)
def error(e):
    print(e)
    return render_template("404.html")
# @app.errorhandler(500)
# def error(e):
#     print(e)
#     return render_template("500.html")
if __name__ == '__main__':
    app.run(debug=True)
