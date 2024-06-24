from common.result_base import ResultBase
from api.webmail_api import Mailmessages
from common.logger import logger
from common.read_data import data, data_file_path

wps_sid = data.load_ini(data_file_path)["user"]["sid"]  # 基础url基础url
csrf = data.load_ini(data_file_path)["user"]["csrf"]


def create_mail_draft(mailbox_id, attachment_urls, bcc, body, cc, subject, to):
    """
创建一封新的草稿并将其存于用户草稿箱中。

PATH PARAMETERS
mailbox_id
required
string <= 1024 characters
REQUEST BODY SCHEMA: application/json
attachment_urls
Array of strings <= 1024 items [ items <= 1024 characters ]
邮件的普通附件url集合。内嵌附件可以直接在body中引用，无需额外提交

bcc_recipients
Array of objects (mail_recipient) <= 1024 items
邮件的Bcc，密送人集合

body
string <= 1024 characters
邮件体

cc_recipients
Array of objects (mail_recipient) <= 1024 items
邮件的Cc，抄送人集合

subject
string <= 1024 characters
邮件标题

to_recipients
Array of objects (mail_recipient) <= 1024 items
邮件的To，收件人集合
    """
    result = ResultBase()
    header = {
        "Content-Type": "application/json",
        "cookie": "wps_sid={};csrf={}".format(wps_sid, csrf),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36 ",
        "X-Csrftoken": csrf,
    }
    json_data = {
        "attachment_urls": [
            attachment_urls
        ],
        "bcc_recipients": [
            {
                "avatar": "",
                "email_address": bcc,
                "label": {},
                "name": "bcc"
            }
        ],
        "body": body,
        "cc_recipients": [
            {
                "avatar": "",
                "email_address": cc,
                "label": {},
                "name": "cc"
            }
        ],
        "subject": subject,
        "to_recipients": [
            {
                "avatar": "",
                "email_address": to,
                "label": {},
                "name": "to"
            }
        ]
    }
    res = Mailmessages.create_mail_draft(mailbox_id, headers=header, json=json_data)
    logger.info("创建草稿==>>请求头==>> {}".format(res.request.headers))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    result.message_id = res.json()["data"]["id"]
    logger.info("创建草稿 ==>> 返回结果 ==>> {}".format(result.response.text))
    logger.info("创建草稿 ==>> 草稿ID ==>> {}".format(result.message_id))
    return result


def send_mail_message(mailbox_id, message_id):
    """
    将草稿箱中的指定邮件投递出去。

PATH PARAMETERS
mailbox_id
required
string <= 1024 characters
message_id
required
string <= 1024 characters
    """
    result = ResultBase()
    header = {
        "Content-Type": "application/json",
        "cookie": "wps_sid={};csrf={}".format(wps_sid, csrf),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36 ",
        "X-Csrftoken": csrf,
    }
    res = Mailmessages.send_mail_message(mailbox_id, message_id, headers=header)
    logger.info("发送邮件==>>请求头==>> {}".format(res.request.headers))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("发送邮件 ==>> 返回结果 ==>> {}".format(result.response.text))
    return result


def get_mail_message(mailbox_id, folder_id, message_id):
    """
从用户特定邮箱提取一封邮件。

PATH PARAMETERS
mailbox_id
required
string <= 1024 characters
folder_id
required
string <= 1024 characters
message_id
required
string <= 1024 characters
    """
    result = ResultBase()
    header = {
        "Content-Type": "application/json",
        "cookie": "wps_sid={};csrf={}".format(wps_sid, csrf),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36 ",
        "X-Csrftoken": csrf,
    }
    res = Mailmessages.get_mail_message(mailbox_id, folder_id, message_id, headers=header)
    logger.info("查看邮件==>>请求头==>> {}".format(res.request.headers))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("查看邮件 ==>> 返回结果 ==>> {}".format(result.response.text))
    return result


def list_mail_messages_in_folder(mailbox_id, folder_id, start_time, end_time, filters, with_attachment, with_body,
                                 page_size, page_token):
    """
取已登录用户的，特定邮箱中的邮件列表。目前仅支持用户登录后，访问自己的邮箱数据。

PATH PARAMETERS
mailbox_id
required
string <= 1024 characters
folder_id
required
string <= 1024 characters
QUERY PARAMETERS
start_time
integer <int64> >= 1
邮件的起始时间戳（单位秒），默认为1

end_time
integer <int64> >= 2
邮件的结束时间戳（单位秒），须大于start_time。默认无穷大

filter
Array of strings (search_filter) <= 1024 items
Items Enum: "unread" "flagged"
邮件筛选条件，默认为all

with_body
boolean
是否需要邮件体。默认返回的body字段为空串

with_attachment
boolean
是否需要附件。默认不返回attachments字段

page_size
required
integer <int64> [ 1 .. 50 ]
分页大小，默认取10

page_token
string <= 1024 characters
翻页token，首次无需提供
    """
    result = ResultBase()
    header = {
        "Content-Type": "application/json",
        "cookie": "wps_sid={};".format(wps_sid),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36 ",
    }
    json_data = {
        "start_time": start_time,
        "end_time": end_time,
        "filter": filters,
        "with_attachment": with_attachment,
        "with_body": with_body,
        "page_size": page_size,
        "page_token": page_token
    }
    res = Mailmessages.list_mail_messages_in_folder(mailbox_id, folder_id, headers=header, data=json_data)
    logger.info("获取目录邮件列表==>>请求头==>> {}".format(res.request.headers))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("获取目录邮件列表 ==>> 返回结果 ==>> {}".format(result.response.text))
    return result


def create_mail_attachment(mailbox_id, files, size):
    """
上传附件到服务器，之后可在草稿中引用该附件。

PATH PARAMETERS
mailbox_id
required
string <= 1024 characters
REQUEST BODY SCHEMA: multipart/form-data
content
required
object <binary>
二进制的文件内容

size
required
integer <int64> >= 1
附件的实际大小，若长度不一致则会上传失败
    """
    result = ResultBase()
    header = {
        # "Content-Type": "multipart/form-data",
        "cookie": "wps_sid={};csrf={}".format(wps_sid, csrf),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36 ",
        "X-Csrftoken": csrf,
    }
    form_data = {
        "content": files,
        "size": size
    }
    logger.info("上传邮件附件==>>请求体==>> {}".format(form_data))
    res = Mailmessages.create_mail_attachment(mailbox_id, files=form_data, headers=header
                                              )
    logger.info("上传邮件附件==>>请求头==>> {}".format(res.request.headers))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    # result.attachment_url = res.json()["data"]["url"]
    logger.info("上传邮件附件 ==>> 返回结果 ==>> {}".format(result.response.text))
    return result


def search_mail_messages(mailbox_id, start_time, end_time, folder_id, filters, keyword, types, with_body,
                         with_attachment,
                         page_size, page_token):
    """
取已登录用户的，符合特定条件（支持：发件人、收件人、主题、邮件体）的邮件列表，按发信日期从新到老。目前仅支持用户登录后，访问自己的邮箱数据。

PATH PARAMETERS
mailbox_id
required
string <= 1024 characters
QUERY PARAMETERS
start_time
integer <int64> >= 1
邮件的起始时间戳（单位秒），默认为1

end_time
integer <int64> >= 2
邮件的结束时间戳（单位秒），须大于start_time。默认无穷大

folders
Array of strings <= 1024 items [ items <= 1024 characters ]
目录ID列表，限制搜索目录范围。默认搜索所有目录

filter
Array of strings (search_filter) <= 1024 items
Items Enum: "unread" "flagged"
邮件筛选条件，默认为all

keyword
required
string <= 1024 characters
关键字，搜索范围由关键字类型指定

type
required
string (search_scope)
Enum: "sender" "receiver" "subject" "body" "all"
关键字类型

with_body
boolean
是否需要邮件体。默认返回的body字段为空串

with_attachment
boolean
是否需要附件。默认不返回attachments字段

page_size
integer <int64> [ 1 .. 50 ]
分页大小，默认取10

page_token
string <= 1024 characters
翻页token，首次无需提供
    """
    result = ResultBase()
    header = {
        "Content-Type": "application/json",
        "cookie": "wps_sid={};csrf={}".format(wps_sid, csrf),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36 ",
        "X-Csrftoken": csrf,
    }
    query_data = {
        "start_time": start_time,
        "end_time": end_time,
        "folders": folder_id,
        "filter": filters,
        "keyword": keyword,
        "type": types,
        "with_body": with_body,
        "with_attachment": with_attachment,
        "page_size": page_size,
        "page_token": page_token
    }
    res = Mailmessages.search_mail_messages(mailbox_id, headers=header, params=query_data)
    logger.info("搜索邮件==>>请求头==>> {}".format(res.request.headers))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("搜索邮件 ==>> 返回结果 ==>> {}".format(result.response.text))
    return result
