import os
from common.rest_client import RestClient
from common.read_data import data

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # 基础路径
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")  # 配置文件路径
api_root_url = data.load_ini(data_file_path)["host"]["api_root_url"]  # 基础url


class Search_mails(RestClient):

    def __init__(self, api_root_url, **kwargs):
        super(Search_mails, self).__init__(api_root_url)

    def search(self, **kwargs):
        return self.get("/v7/mail_messages/search", **kwargs)


Searchmails = Search_mails(api_root_url)
