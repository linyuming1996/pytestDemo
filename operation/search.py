from core.result_base import ResultBase
from api.search import search
from common.logger import logger


def search():
    result = ResultBase()
    res = search.search()
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    return result
