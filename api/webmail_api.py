import os
from common.rest_client import RestClient
from common.read_data import data

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # 基础路径
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")  # 配置文件路径
api_root_url = data.load_ini(data_file_path)["host"]["api_root_url"]  # 基础url


class Search_mails(RestClient):

    def __init__(self, api_root_url, **kwargs):
        super(Search_mails, self).__init__(api_root_url)

    def advance_search_mail_messages(self, **kwargs):
        return self.get("/v7/mail_messages/search", **kwargs)

    def search_mail_messages(self, mailbox_id, **kwargs):
        return self.get("/v7/mailboxes/{}/messages".format(mailbox_id), **kwargs)


Searchmails = Search_mails(api_root_url)


class Mail_boxes(RestClient):
    def __init__(self, api_root_url, **kwargs):
        super(Mail_boxes, self).__init__(api_root_url)

    def get_mailboxes(self, **kwargs):
        """获取邮箱列表"""
        return self.get("/v7/mailboxes", **kwargs)


Mailboxes = Mail_boxes(api_root_url)


class Mail_folders(RestClient):
    def __init__(self, api_root_url, **kwargs):
        super(Mail_folders, self).__init__(api_root_url)

    def list_mail_folders(self, mailbox_id, **kwargs):
        """获取目录列表"""
        return self.get("/v7/mailboxes/{}/folders".format(mailbox_id), **kwargs)

    def get_mail_folder(self, mailbox_id, folder_id, **kwargs):
        """获取指定目录"""
        return self.get("/v7/mailboxes/{}/folders/{}".format(mailbox_id, folder_id), **kwargs)

    def list_mail_folder_children(self, mailbox_id, folder_id, **kwargs):
        """获取子目录"""
        return self.get("/v7/mailboxes/{}/folders/{}/children".format(mailbox_id, folder_id), **kwargs)


Mailfolders = Mail_folders(api_root_url)


class Mail_messages(RestClient):
    def __init__(self, api_root_url, **kwargs):
        super(Mail_messages, self).__init__(api_root_url)

    def create_mail_draft(self, mailbox_id, **kwargs):
        """创建草稿"""
        return self.post("/v7/mailboxes/{}/messages/create".format(mailbox_id), **kwargs)

    def send_mail_message(self, mailbox_id,message_id, **kwargs):
        """发送邮件"""
        return self.post("/v7/mailboxes/{}/messages/{}/send".format(mailbox_id,message_id), **kwargs)

    def get_mail_message(self, mailbox_id, folder_id, message_id, **kwargs):
        """获取指定邮件"""
        return self.get("/v7/mailboxes/{}/folders/{}/messages/{}".format(mailbox_id, folder_id, message_id), **kwargs)

    def list_mail_messages_in_folder(self, mailbox_id, folder_id, **kwargs):
        """获取特定目录下的邮件列表"""
        return self.get("/v7/mailboxes/{}/folders/{}/messages".format(mailbox_id, folder_id), **kwargs)

    def create_mail_attachment(self, mailbox_id, **kwargs):
        """上传附件"""
        return self.post("/v7/mailboxes/{}/attachments/create".format(mailbox_id), **kwargs)

    def search_mail_messages(self, mailbox_id, **kwargs):
        return self.get("/v7/mailboxes/{}/messages".format(mailbox_id), **kwargs)


Mailmessages = Mail_messages(api_root_url)
