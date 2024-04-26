from core.result_base import ResultBase
from api.search import search
from common.logger import logger


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
    :param to: 发件人搜索,支持邮箱地址、用户名搜索，默认不筛选，多个使用空格分割
    :param subject: 发件人搜索,支持邮箱地址、用户名搜索，默认不筛选，多个使用空格分割
    :param body: 发件人搜索,支持邮箱地址、用户名搜索，默认不筛选，多个使用空格分割
    :param attachment: 发件人搜索,支持邮箱地址、用户名搜索，默认不筛选，多个使用空格分割
    :param keyword: 发件人搜索,支持邮箱地址、用户名搜索，默认不筛选，多个使用空格分割
    :param with_body: 发件人搜索,支持邮箱地址、用户名搜索，默认不筛选，多个使用空格分割
    :param with_category: 发件人搜索,支持邮箱地址、用户名搜索，默认不筛选，多个使用空格分割
    :param page_size: 发件人搜索,支持邮箱地址、用户名搜索，默认不筛选，多个使用空格分割
    :param page_token: 发件人搜索,支持邮箱地址、用户名搜索，默认不筛选，多个使用空格分割
    :param token: 用户token
    :return: 自定义的关键字返回结果 result
    """
    result = ResultBase()
    header = {
        "Content-Type": "application/json"
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
        "page_token":page_token

    }
    res = search.search(mailbox_ids, json=json_data, headers=header, )
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("查询邮件 ==>> 返回结果 ==>> {}".format(result.response.text))
    return result



