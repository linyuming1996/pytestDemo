from common.result_base import ResultBase
from api.webmail_api import Mailfolders
from common.logger import logger
from common.read_data import data, data_file_path

wps_sid = 'wps_sid=' + data.load_ini(data_file_path)["user"]["sid"]  # 基础url基础url


def get_mailfolders(mailbox_ids):
    """
    根据用户ID，获取邮箱的所有目录信息
    :param mailbox_ids: 用户ID
    :param sid: 用户token
    :return: 自定义的关键字返回结果 result
    """
    result = ResultBase()
    header = {
        "Content-Type": "application/json",
        "cookie": wps_sid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36 "
    }
    res = Mailfolders.list_mail_folders(mailbox_ids, headers=header)
    logger.info("获取邮箱目录==>>请求头==>> {}".format(res.request.headers))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("获取邮箱目录 ==>> 返回结果 ==>> {}".format(result.response.text))
    return result


def get_mail_folder(mailbox_id, folder_id):
    """
    根据用户ID，获取指定目录
PATH PARAMETERS
mailbox_id
required
string <= 1024 characters
folder_id
required
string <= 1024 characters
    """
    result = ResultBase()
    header = {
        "Content-Type": "application/json",
        "cookie": wps_sid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36 "
    }
    res = Mailfolders.get_mail_folder(mailbox_id, folder_id, headers=header)
    logger.info("获取指定目录信息==>>请求头==>> {}".format(res.request.headers))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("获取指定目录信息 ==>> 返回结果 ==>> {}".format(result.response.text))
    return result


def list_mail_folder_children(mailbox_id, folder_id):
    """
    获取指定目录下的所有子目录信息
PATH PARAMETERS
mailbox_id
required
string <= 1024 characters
parent_id
required
string <= 1024 characters
    """
    result = ResultBase()
    header = {
        "Content-Type": "application/json",
        "cookie": wps_sid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36 "
    }
    res = Mailfolders.list_mail_folder_children(mailbox_id, folder_id, headers=header)
    logger.info("获取子目录==>>请求头==>> {}".format(res.request.headers))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("获取子目录 ==>> 返回结果 ==>> {}".format(result.response.text))
    return result
