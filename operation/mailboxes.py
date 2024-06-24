from common.result_base import ResultBase
from api.webmail_api import Mailboxes
from common.logger import logger
from common.read_data import data, data_file_path


wps_sid = 'wps_sid=' + data.load_ini(data_file_path)["user"]["sid"]  # 基础url基础url


def get_mailboxes():
    """
    获取邮箱列表
    :return: 自定义的关键字返回结果 result
    """
    result = ResultBase()
    header = {
        "Content-Type": "application/json",
        "cookie": wps_sid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36 "
    }
    res = Mailboxes.get_mailboxes(headers=header)
    logger.info("获取邮箱列表==>>请求头==>> {}".format(res.request.headers))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("获取邮箱列表 ==>> 返回结果 ==>> {}".format(result.response.text))
    return result
