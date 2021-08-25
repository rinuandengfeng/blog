import os.path
from pathlib import Path

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, g

# 蓝图中有url_prefix这个参数，运行的时候需要在路由上添加user/  才能运行
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from apps import app
from apps.article.models import Article_type, Article
from apps.user.models import User, Photo, AboutMe, MessageBoard
from apps.user.smssend import SmsSendAPIDemo
from apps.utils.utils import upload_qiniu, del_qiniu, user_type
from exts import db
from settings import Config

user_bp1 = Blueprint('user', __name__, url_prefix='/user')

# 将需要的路由加入到这个钩子函数中，然后就走这个def before_request1():函数，所以里面的g.user就可以使用
required_login_list = ['/user/center',
                       '/user/change',
                       '/article/publish',
                       '/user/upload_photo',
                       '/user/photo_del',
                       '/article/add_comment',
                       '/user/aboutme',
                       '/user/showabout']


@user_bp1.before_app_first_request
def first_request():
    # print('before_app_first_request')
    return '1'


#  重点
@user_bp1.before_app_request
def before_request1():
    # print('before_app_request', request.path)
    if request.path in required_login_list:
        id = session.get('uid')
        if not id:
            return render_template('user/login.html')
        else:
            user = User.query.get(id)
            # g对象，本次请求的对象
            g.user = user


@user_bp1.after_app_request
def after_request_test(response):
    response.set_cookie('a', 'bbbb', max_age=19)
    return response


@user_bp1.teardown_app_request
def teardown_request_test(response):
    return response


# 自定义过滤器  将二进制文件转化为utf-8
@user_bp1.app_template_filter('cdecode')
def content_decode(content):
    content = content.decode(encoding='utf-8')
    return content[:100]


@user_bp1.app_template_filter('cdecode2')
def content_decode(content):
    content = content.decode(encoding='utf-8')
    return content


# 首页
@user_bp1.route('/')
def index():
    # 1.cookie获取方式
    # uid = request.cookies.get('uid', None)
    # 2.session的获取,session底层默认获取
    uid = session.get('uid')
    # 获取文章列表,按照文章的发表时间进行排序
    # 接收页码数

    page = request.args.get('page', 1)
    page = int(page)
    pagination = Article.query.order_by(-Article.padatetime).paginate(page=page, per_page=3)

    # 获取分类列表
    types = Article_type.query.all()
    # 判断用户是否登录
    if uid:
        user = User.query.get(uid)
        return render_template('user/index.html', user=user, pagination=pagination, types=types)
    else:
        return render_template('user/index.html', pagination=pagination, types=types)


# 注册用户路由
@user_bp1.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        email = request.form.get('email')

        if password == repassword:
            # 注册用户
            user = User()
            user.username = username
            # 使用flask自带的函数实现密码加密：generater_password_hash()
            user.password = generate_password_hash(password)
            user.phone = phone
            user.email = email
            # 添加并提交
            db.session.add(user)
            db.session.commit()
            # return redirect(url_for('user/user_conter.html'))
            return redirect(url_for('user.login'))
    return render_template('user/register.html')


# 手机号码验证
@user_bp1.route('/checkphone', methods=['GET', 'POST'])
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).all()
    # ajax的返回值必须是json格式
    # code:400  不能用  200  可以用
    if len(user) > 0:
        return jsonify(code=400, msg='此号码已被注册')
    else:
        return jsonify(code=200, msg='此号码可以用')


# 用户登录
@user_bp1.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        f = request.args.get('f')
        # 用户名或者密码
        if f == '1':
            username = request.form.get('username')
            password = request.form.get('password')
            users = User.query.filter(User.username == username).all()
            for user in users:
                # 如果flag=Ture表示匹配，否则密码不匹配
                flag = check_password_hash(user.password, password)
                if flag:
                    # 1.cookie实现机制
                    # respone = redirect(url_for('user.index'))
                    # respone.set_cookie('uid', str(user.id), max_age=1800)
                    # return respone
                    # 2.session机制 , session当成字典使用
                    session['uid'] = user.id
                    return redirect(url_for('user.index'))
                else:
                    return render_template('user/login.html', msg="用户名或者密码错误！")
        # 手机号码与验证码
        elif f == '2':
            phone = request.form.get('phone')
            code = request.form.get('code')
            # 先验证验证码
            valide_code = session.get(phone)
            if code == valide_code:
                # 查询数据库
                user = User.query.filter(User.phone == phone).all()
                if user:
                    # 登录成功
                    session['uid'] = user.id
                    return redirect(url_for('user.index'))
                else:
                    return render_template('user.login', msg='此号码未注册！')
            else:
                return render_template('user/login.html', msg='验证码有误!')
    return render_template('user/login.html')


# 发送短信息
@user_bp1.route('/sendMsg')
def send_message():
    phone = request.args.get('phone')
    # 验证手机号码是否注册，去数据库查询
    ret, code = send_message(phone)
    if ret is not None:
        if ret["code"] == 200:
            taskId = ret["data"]["taskId"]
            print("taskId = %s" % taskId)
            session[phone] = '189075'  # 不局限在send_message这个函数使用
            return jsonify(code=200, msg='短信发送成功！')
        else:
            print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))
            return jsonify(code=400, msg='短信发送失败！')

    else:
        return jsonify(code=400, msg='手机号码没有注册!')


# 用户退出
@user_bp1.route('/logout')
def logout():
    # 1. cookie的方式
    # response = redirect(url_for('user.index'))
    # 删除cookie     通过response对象delete_cookie(key),key就是要删除的cookie的key
    # response.delete_cookie('uid')
    # 2.session的方式
    # del session['uid']        这种方式只删除session中的这个键值对，不会删除session空间和cookie
    session.clear()  # 删除session的内存空间和删除cookie
    return redirect(url_for('user.index'))


# 用户中心
@user_bp1.route('/center')
def user_center():
    types = Article_type.query.all()
    photos = Photo.query.filter(Photo.user_id == g.user.id).all()

    return render_template('user/center.html', user=g.user, types=types, photos=photos)


# 图片的扩展名
ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif', 'bmp']


# 用户信息修改
@user_bp1.route('/change', methods=['GET', 'POST'])
def user_change():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        # 只要有文件（图片），获取方式必须使用request.files.get(name)
        icon = request.files.get('icon')
        # 属性： filename 用户获取文件的名字
        # 方法： save(保存路径)
        icon_name = icon.filename  # 获取文件的名字

        suffix = icon_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            # icon_name = secure_filename('/' + icon_name)  # secure_filename()保证文件名是符合python的命名规则
            file_path = os.path.join(Config.UPLOAD_ICON_DIR, icon_name)
            icon.save(file_path)
            # 文件保存成功
            user = g.user
            user.username = username
            user.phone = phone
            user.email = email
            path = 'upload/icon'
            # 使用Path(path_icon).as_posix()这个方法将‘\’转化为'/'
            path_icon = os.path.join(path, icon_name)
            user.icon = Path(path_icon).as_posix()
            db.session.commit()
            return redirect(url_for('user.user_center'))
        else:
            return render_template('user/center.html', user=g.user, msg='必须是扩展名为jpg,png,gif,bmpS格式')

        # 查询一下手机号码
        users = User.query.all()
        for user in users:
            if user.phone == phone:
                # 说明数据库中已经有人注册此号码
                return render_template('user/center.html', user=g.user, msg='此号码已被注册')
        # user = g.user
        # user.username = username
        # user.phone = phone
        # user.email = email
        # db.session.commit()
    return render_template('user/center.html', user=g.user)


# 上传照片
@user_bp1.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    # 获取上传的照片
    photo = request.files.get('photo')  # FileStorage
    # 把照片上传到七牛云云存储
    # 在工具模块封装好的
    info, ret = upload_qiniu(photo)
    if info.status_code == 200:
        photo = Photo()
        # 取出文件名
        photo.photo_name = ret
        photo.user_id = g.user.id
        db.session.add(photo)
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:
        return '上传失败'


# 删除相册图片
@user_bp1.route('/photo_del')
def photo_del():
    pid = request.args.get('pid')
    photo = Photo.query.get(pid)
    filename = photo.photo_name
    # 封装号的一个删除七牛云存储的函数
    info = del_qiniu(filename)
    if info.status_code == 200:
        # 删除数据库的内容
        db.session.delete(photo)
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:

        return render_template('500.html', err_msg='删除相册图片失败!')


# 我的相册
@user_bp1.route('/myphoto')
def myphoto():
    # 默认第一页  如果不转成整型，默认是str类型
    page = int(request.args.get('page', 1))
    # 分页操作 ，返回的是paginate对象  photos是一个paginate类型
    photos = Photo.query.paginate(page=page, per_page=3)
    user, types = user_type
    return render_template('user/myphoto.html', photos=photos, user=user, types=types)


# 关于用户介绍添加
@user_bp1.route('/aboutme', methods=['GET', 'POST'])
def about_me():
    content = request.form.get('about')
    # 添加信息
    # 异常处理
    try:
        aboutme = AboutMe()
        aboutme.content = content.encode('utf-8')
        aboutme.user_id = g.user.id
        db.session.add(aboutme)
        db.session.commit()
    # 有错进入except
    except Exception as err:
        return redirect(url_for('user.user_center'))
    # 没有错进入else
    else:
        return render_template('user/aboutme.html', user=g.user)


# 展示关于我
@user_bp1.route('/showabout')
def show_about():
    user, types = user_type()
    return render_template('user/aboutme.html', user=g.user, types=types)


# 留言板
@user_bp1.route('/board', methods=['GET', 'POST'])
def show_board():
    # 获取登录用户信息
    uid = session.get('uid', None)
    user = None
    if uid:
        user = User.query.get(uid)
        # 查询所有的留言内容,并进行分页处理
        page = request.args.get('page', 1)
        page = int(page)
        boards = MessageBoard.query.order_by(-MessageBoard.mdatetime).paginate(page=page, per_page=3)

    # 判断当前的请求方式
    if request.method == 'POST':
        content = request.form.get('board')
        # 添加留言内容
        msg_board = MessageBoard()
        msg_board.content = content
        if uid:
            msg_board.user_id = uid
        db.session.add(msg_board)
        db.session.commit()
        return redirect(url_for('user.show_board'))
    user, types = user_type()
    return render_template('user/board.html', user=user, boards=boards, types=types)


# 留言删除
@user_bp1.route('/board_del')
def delete_board():
    bid = request.args.get('bid')
    if bid:
        msgboard = MessageBoard.query.get(bid)
        db.session.delete(msgboard)
        db.session.commit()
        return redirect(url_for('user.user_center'))


# 错误的路由
@user_bp1.route('/error')
def test_error():
    referer = request.headers.get('Referer', None)
    return render_template('500.html', err_msg="有误", referer=referer)
