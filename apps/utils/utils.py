import os
import random

from flask import session
from qiniu import Auth, put_file, etag, put_data, BucketManager
import qiniu.config

from apps.article.models import Article, Article_type
from apps.user.models import User
from apps.user.smssend import SmsSendAPIDemo
from settings import Config


def upload_qiniu(filestorage):
    # 需要填写你的 Access Key 和 Secret Key

    access_key = 'MnbL-ZEB56Qfd6zYieG1rWZmfyTNPOGtOCNMkWbA'
    secret_key = 'LYuWGlJq8_FxKH-d_BNiwKsdhQ8rNm-THfUyP6yr'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'myblog20'

    # 上传后保存的文件名
    filenames = filestorage.filename

    # 生成随机数
    rran = random.randint(1, 1000)
    # 取出后缀名
    suffix = filenames.rsplit('.')[-1]
    # 取出文件的名字
    key = filenames.rsplit('.')[0] + '_' + str(rran) + '.' + suffix
    # key = 'my-python-logo.png'

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = os.path.join(Config.UPLOAD_ICON_DIR, '海贼王.jpg')
    #
    # ret, info = put_file(token, key, localfile, version='v2')
    ret, info = put_data(token, key, filestorage.read())  # filesstorage.read()是读取这些文件的二进制流
    return info, key


def del_qiniu(filename):
    access_key = 'MnbL-ZEB56Qfd6zYieG1rWZmfyTNPOGtOCNMkWbA'
    secret_key = 'LYuWGlJq8_FxKH-d_BNiwKsdhQ8rNm-THfUyP6yr'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'myblog20'
    # 初始化BucketManager
    bucket = BucketManager(q)
    # 文件的名字 key是要删除的文件的名字
    key = filename
    ret, info = bucket.delete(bucket_name, key)
    return info


def user_type():
    # 获取文章分类
    types = Article_type.query.all()
    # 登录用户
    user = None
    user_id = session.get('uid', None)
    if user_id:
        user = User.query.get(user_id)
    return user, types


# 发送短信
def send_messages(phone):
    """示例代码入口"""
    SECRET_ID = "b8bd68caf02d1ea89941382347d354fd"  # 产品密钥ID，产品标识
    SECRET_KEY = "41992a16b5bed476fab972118b23f319"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "ef52f46eb8d64cb980a9e441f392e600"  # 业务ID，易盾根据产品业务特点分配
    api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)

    code = ""
    for i in range(6):
        ran = random.randint(0, 9)
        code += str(ran)
    params = {
        "mobile": phone,
        "templateId": "15022",
        "paramType": "json",
        "params": {"code": code}
        # 国际短信对应的国际编码(非国际短信接入请注释掉该行代码)
        # "internationalCode": "对应的国家编码"
    }
    ret = api.send(params)
    return ret, code
