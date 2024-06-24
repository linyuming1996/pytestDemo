from common.result_base import ResultBase
from api.webmail_api import Searchmails
from common.logger import logger
from common.read_data import data
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # 基础路径
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")  # 配置文件路径
wps_sid = 'wps_sid='+data.load_ini(data_file_path)["user"]["sid"]  # 基础url基础url


def search_mails(mailbox_ids, start_time, end_time, folders, filters, has_attachment, send, to, subject, body,
                 attachment,
                 keyword, with_body, with_category, page_size, page_token):
    """
    根据用户ID，修改用户信息
    :param mailbox_ids: 用户ID
    :param start_time: 邮件的起始时间戳（单位秒），默认为1
    :param end_time: 邮件的结束时间戳（单位秒），须大于start_time。默认无穷大
    :param folders: 目录ID列表，限制搜索目录范围。默认搜索所有目录，多个账号用,号分割
    :param filter: Items Enum: "unread" "flagged"邮件筛选条件，默认为all
    :param has_attachment: true筛选包含附件，false筛选不包含附件。默认不筛选
    :param send: 发件人搜索,支持邮箱地址、用户名搜索，默认不筛选，多个使用空格分割
    :param to: 收件人搜索，支持邮箱地址、用户名搜索，默认不筛选，这里包含收件人，抄送，密送人搜索，多个使用空格分割
    :param subject: 邮件主题搜索，默认不搜索
    :param body: 邮件正文搜索，支持模糊搜索，默认不搜索
    :param attachment: 邮件附件名称搜索,支持模糊搜索，默认不搜索
    :param keyword: 关键字搜索,支持模糊搜索
    :param with_body: 是否需要邮件体。默认返回的body字段为空串
    :param with_category: 是否需要分类字段。默认不返回categories字段
    :param page_size: 分页大小，默认取10
    :param page_token: 翻页token，首次无需提供
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
    json_data = {
        "mailbox_ids": mailbox_ids,
        "start_time": start_time,
        "end_time": end_time,
        "folders": folders,
        "filter": filters,
        "has_attachment": has_attachment,
        "from": send,
        "to": to,
        "subject": subject,
        "body": body,
        "attachment": attachment,
        "keyword": keyword,
        "with_body": with_body,
        "with_category": with_category,
        "page_size": page_size,
        "page_token": page_token
    }
    res = Searchmails.advance_search_mail_messages(headers=header, params=json_data)
    logger.info("查询邮件==>>请求头==>> {}".format(res.request.headers))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("查询邮件 ==>> 返回结果 ==>> {}".format(result.response.text))
    return result
