
# -*- coding: utf-8 -*-
# flake8: noqa
import os

from qiniu import Auth, put_file, etag
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
from settings import Config

access_key = 'MnbL-ZEB56Qfd6zYieG1rWZmfyTNPOGtOCNMkWbA'
secret_key = 'LYuWGlJq8_FxKH-d_BNiwKsdhQ8rNm-THfUyP6yr'

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'myblog20'

#上传后保存的文件名
key = 'my-python-logo.png'

#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

#要上传文件的本地路径
localfile = os.path.join(Config.UPLOAD_ICON_DIR,'海贼王.jpg')

ret, info = put_file(token, key, localfile, version='v2')
print(info)
print(ret)
# assert ret['key'] == key
# assert ret['hash'] == etag(localfile)


