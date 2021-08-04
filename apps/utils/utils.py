import os
import random

from qiniu import Auth, put_file, etag, put_data, BucketManager
import qiniu.config
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
    #文件的名字 key是要删除的文件的名字
    key = filename
    ret, info = bucket.delete(bucket_name, key)
    return info