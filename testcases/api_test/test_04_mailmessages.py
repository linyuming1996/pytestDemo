import pytest
import allure
from operation.mailmessages import create_mail_draft, send_mail_message, list_mail_messages_in_folder, get_mail_message, \
    search_mail_messages, create_mail_attachment
from testcases.conftest import api_data
from common.logger import logger
import os
from common.read_data import BASE_PATH


@allure.step("前置步骤1 ==>> 创建草稿")
def step_1(mailbox_id, attachment_urls, bcc, body, cc, subject, to):
    logger.info("前置步骤1 ==>> 创建草稿")
    return create_mail_draft(mailbox_id, attachment_urls, bcc, body, cc, subject, to)


# @allure.step("步骤1 ==>> 查询邮件")
# def step_2(username):
#     logger.info("步骤1 ==>> 获取某个用户信息：{}".format(username))


@allure.severity(allure.severity_level.TRIVIAL)
@allure.epic("针对单个接口的测试")
@allure.feature("邮箱邮件")
class TestMailMessages():
    """邮箱邮件"""

    @allure.story("用例--上传附件")
    @allure.title("测试用例：【上传附件】")
    @pytest.mark.single
    @pytest.mark.parametrize(
        "mailbox_id, file_name, except_result, except_code, except_msg",
        api_data["test_CreateMailAttachment"])
    def test_CreateMailAttachment(self, mailbox_id, file_name, except_result, except_code, except_msg):
        logger.info("*************** 开始执行用例 ***************")
        file_name = os.path.join(BASE_PATH, "data", file_name)  # 配置文件路径
        with open(file_name, 'rb') as file:
            # binary_content = file.read()
            binary_content = (file_name, open(file_name, 'rb'), 'text/plain')
            logger.info('file1={}'.format(binary_content))
            # 获取文件大小
            file_size = os.path.getsize(file_name)
            logger.info("上传附件 ==>> {},附件大小{}".format(file_name, file_size))
        result = create_mail_attachment(mailbox_id, binary_content, file_size)
        assert result.success == except_result, result.error
        assert result.response.status_code == 200
        assert result.success == except_result, result.error
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert except_msg in result.msg
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--创建邮件草稿")
    @allure.title("测试用例：【创建邮件草稿】")
    @pytest.mark.single
    @pytest.mark.parametrize("mailbox_id, attachment_urls, bcc, body, cc, subject, to,except_result,except_code,"
                             "except_msg",
                             api_data["test_CreateMailDraft"])
    def test_CreateMailDraft(self, mailbox_id, attachment_urls, bcc, body, cc, subject, to, except_result, except_code,
                             except_msg):
        logger.info("*************** 开始执行用例 ***************")
        result = create_mail_draft(mailbox_id, attachment_urls, bcc, body, cc, subject, to)
        assert result.success == except_result, result.error
        assert result.response.status_code == 200
        assert result.success == except_result, result.error
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert except_msg in result.msg
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--发送邮件")
    @allure.title("测试用例：【发送邮件】")
    @pytest.mark.single
    @pytest.mark.parametrize("mailbox_id, attachment_urls, bcc, body, cc, subject, to, except_result, except_code,"
                             "except_msg",
                             api_data["test_SendMailMessage"])
    def test_SendMailMessage(self, mailbox_id, attachment_urls, bcc, body, cc, subject, to, except_result, except_code,
                             except_msg):
        logger.info("*************** 开始执行用例 ***************")
        result = step_1(mailbox_id, attachment_urls, bcc, body, cc, subject, to)
        result = send_mail_message(mailbox_id, result.message_id)
        assert result.success == except_result, result.error
        assert result.response.status_code == 200
        assert result.success == except_result, result.error
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert except_msg in result.msg
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--查看邮件")
    @allure.title("测试用例：【查看邮件】")
    @pytest.mark.single
    @pytest.mark.parametrize(
        "mailbox_id, folder_id, attachment_urls, bcc, body, cc, subject, to, except_result, except_code,except_msg",
        api_data["test_GetMailMessage"])
    def test_GetMailMessage(self, mailbox_id, folder_id, attachment_urls, bcc, body, cc, subject, to, except_result,
                            except_code,
                            except_msg):
        logger.info("*************** 开始执行用例 ***************")
        result = step_1(mailbox_id, attachment_urls, bcc, body, cc, subject, to)
        result = get_mail_message(mailbox_id, folder_id, result.message_id)
        assert result.success == except_result, result.error
        assert result.response.status_code == 200
        assert result.success == except_result, result.error
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert except_msg in result.msg
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--获取特定目录下的邮件列表")
    @allure.title("测试用例：【获取特定目录下的邮件列表】")
    @pytest.mark.single
    @pytest.mark.parametrize("mailbox_id, folder_id, start_time, end_time, filters, with_attachment, with_body,"
                             "page_size, page_token, except_result, except_code,except_msg",
                             api_data["test_ListMailMessagesInFolder"])
    def test_ListMailMessagesInFolder(self, mailbox_id, folder_id, start_time, end_time, filters, with_attachment,
                                      with_body, page_size, page_token, except_result, except_code, except_msg):
        logger.info("*************** 开始执行用例 ***************")
        result = list_mail_messages_in_folder(mailbox_id, folder_id, start_time, end_time, filters, with_attachment,
                                              with_body,
                                              page_size, page_token)
        assert result.success == except_result, result.error
        assert result.response.status_code == 200
        assert result.success == except_result, result.error
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert except_msg in result.msg
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--搜索邮件")
    @allure.title("测试用例：【搜索邮件】")
    @pytest.mark.single
    @pytest.mark.parametrize(
        "mailbox_id, start_time, end_time, folder_id, filters, keyword, types, with_body, with_attachment,"
        "page_size, page_token, except_result, except_code,except_msg",
        api_data["test_SearchMailMessages"])
    def test_SearchMailMessages(self, mailbox_id, start_time, end_time, folder_id, filters, keyword, types, with_body,
                                with_attachment, page_size, page_token, except_result, except_code, except_msg):
        logger.info("*************** 开始执行用例 ***************")
        result = search_mail_messages(mailbox_id, start_time, end_time, folder_id, filters, keyword, types, with_body,
                                      with_attachment, page_size, page_token)
        assert result.success == except_result, result.error
        assert result.response.status_code == 200
        assert result.success == except_result, result.error
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert except_msg in result.msg
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s"])
