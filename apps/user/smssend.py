from hashlib import md5
import json
import random
import time
import urllib
import urllib.request
import requests


class SmsSendAPIDemo(object):
    """易盾短信发送接口示例代码"""
    API_URL = "https://sms.dun.163.com/v2/sendsms"
    VERSION = "v2"

    def __init__(self, secret_id, secret_key, business_id):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
            business_id (str) 业务ID，易盾根据产品业务特点分配
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.business_id = business_id

    def gen_signature(self, params=None):
        """生成签名信息
        Args:
            params (object) 请求参数
        Returns:
            参数签名md5值
        """
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        return md5(buff.encode("utf-8")).hexdigest()

    def send(self, params):
        """请求易盾接口
        Args:
            params (object) 请求参数
        Returns:
            请求结果，json格式
        """
        params["secretId"] = self.secret_id
        params["businessId"] = self.business_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random() * 100000000)
        params["signature"] = self.gen_signature(params)

        try:
            # params = urllib.parse.urlencode(params)
            # params = params.encode('utf-8')
            # request = urllib.request.Request(self.API_URL, params)
            # content = urllib.request.urlopen(request, timeout=5).read()
            response = requests.post(self.API_URL, data=params)
            return response.json()
        except Exception as ex:
            print("调用API接口失败:", str(ex))


if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "53633b57748f98ad5e645fc3b3db63f7"  # 产品密钥ID，产品标识
    SECRET_KEY = "b02b75ed758849e2c65afdc521f3b6fa"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "9dbcb28d4229401782a556990562b6af"  # 业务ID，易盾根据产品业务特点分配
    api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)

    params = {
        "mobile": "15239330590",
        "templateId": "10084",
        "paramType": "json",
        "params": "json格式字符串"
        # 国际短信对应的国际编码(非国际短信接入请注释掉该行代码)
        # "internationalCode": "对应的国家编码"
    }
    ret = api.send(params)
    print(ret)
    if ret is not None:
        if ret["code"] == 200:
            taskId = ret["data"]["taskId"]
            print("taskId = %s" % taskId)
        else:
            print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))