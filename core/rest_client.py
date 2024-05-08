import requests
import json as complexjson
from common.logger import logger


class RestClient():
    """"request请求方式封装"""

    def __init__(self, api_root_url):
        self.api_root_url = api_root_url
        self.session = requests.session()

    def get(self, url, **kwargs):
        return self.request(url, "GET", **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request(url, "POST", data, json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request(url, "PUT", data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url, "DELETE", **kwargs)

    # def patch(self, url, data=None, **kwargs):
    #     return self.request(url, "PATCH", data, **kwargs)

    def request(self, url, method, data=None, json=None, **kwargs):
        url = self.api_root_url + url
        headers = dict(**kwargs).get("headers")
        params = dict(**kwargs).get("params")
        # files = dict(**kwargs).get("files")
        # cookies = dict(**kwargs).get("cookies")
        files = dict(**kwargs).get("files")
        cookies = dict(**kwargs).get("cookies")
        self.request_log(url, method, data, json, params, headers, files, cookies)
        if method == "GET":
            json = complexjson.dumps(json)
            return self.session.get(url, **kwargs)
        # if method == "POST":
        #     return requests.post(url, data, json, **kwargs)
        # if method == "PUT":
        #     if json:
        #         # PUT 和 PATCH 中没有提供直接使用json参数的方法，因此需要用data来传入
        #         data = complexjson.dumps(json)
        #     return self.session.put(url, data, **kwargs)
        # if method == "DELETE":
        #     return self.session.delete(url, **kwargs)
        # if method == "PATCH":
        #     if json:
        #         data = complexjson.dumps(json)
        #     return self.session.patch(url, data, **kwargs)

    def request_log(self, url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None,
                    **kwargs):
        logger.info("接口请求地址 ==>> {}".format(url))
        logger.info("接口请求方式 ==>> {}".format(method))
        # Python3中，json在做dumps操作时，会将中文转换成unicode编码，因此设置 ensure_ascii=False
        logger.info("接口请求头 ==>> {}".format(complexjson.dumps(headers, indent=4, ensure_ascii=False)))
        logger.info("接口请求 params 参数 ==>> {}".format(complexjson.dumps(params, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 data 参数 ==>> {}".format(complexjson.dumps(data, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 json1 参数 ==>> {}".format(json))
        logger.info("接口请求体 json 参数 ==>> {}".format(complexjson.dumps(json, indent=4, ensure_ascii=False)))
        # - `dumps()` 是该库中的一个方法，用于将 Python 对象编码成 JSON 字符串；
        # - `json` 是要转换的 Python 对象；
        # - `indent=4` 表示使用四个空格来缩进生成的 JSON 字符串，使其更具可读性；
        # - `ensure_ascii=False` 表示不要将非 ASCII 字符转义为 Unicode 转义序列，这样可以保留原始字符
        # logger.info("接口请求体 json 参数 ==>> {}".format(complexjson.dumps(self.session.get(url, **kwargs).request.body), indent=4, ensure_ascii=False))
        logger.info("接口上传附件 files 参数 ==>> {}".format(files))
        logger.info("接口 cookies 参数 ==>> {}".format(complexjson.dumps(cookies, indent=4, ensure_ascii=False)))
