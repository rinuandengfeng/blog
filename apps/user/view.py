import hashlib
from hashlib import md5

from flask import Blueprint, render_template, request

from apps.user.models import User
from exts import db

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        if password == repassword:
            passw = hashlib.md5(password.encode('UTF_8')).hexdigest()
            #与模型结合
            #1.找到模型类并创建对象
            user = User()
            #2.给对象的属性赋值
            user.username = username
            user.password = passw
            user.phone = phone
            #添加
            #3.将user对象添加到session中（类似于缓存）
            db.session.add(user)
            #4.将缓存提交到数据库
            db.session.commit()
            return render_template('user/conter')
        else:
            return '两次密码不一致'

    return render_template('user/register.html')
