import pytest
import allure
# from operation.user import get_all_user_info, get_one_user_info
from operation.search import search_mails
from testcases.conftest import api_data
from common.logger import logger


@allure.step("步骤1 ==>> 登录邮箱")
def step_1():
    logger.info("步骤1 ==>> 登录邮箱")


# @allure.step("步骤1 ==>> 查询邮件")
# def step_2(username):
#     logger.info("步骤1 ==>> 获取某个用户信息：{}".format(username))


@allure.severity(allure.severity_level.TRIVIAL)
@allure.epic("针对单个接口的测试")
@allure.feature("查询用户邮件")
class TestSearchMails():
    """查询成员邮件"""

    @allure.story("用例--查询成员邮件")
    # @allure.description("该用例是针对查询成员邮件接口的测试")
    # @allure.issue("https://www.email.wps.cn", name="点击，跳转到对应BUG的链接地址")
    # @allure.testcase("https://www.cnblogs.com/wintest", name="点击，跳转到对应用例的链接地址")
    @allure.title("测试用例：【查询成员邮件】")
    @pytest.mark.single
    @pytest.mark.parametrize("mailbox_ids, start_time, end_time, folders, filters,has_attachment,send,to,subject,"
                             "body, attachment, keyword, with_body, with_category, page_size, page_token, "
                             "except_result,except_code,except_msg",
                             api_data["test_SearchMails"])
    # @pytest.mark.usefixtures("update_user_telephone")
    def test_SearchMails(self, mailbox_ids, start_time, end_time, folders, filters, has_attachment, send, to, subject,
                         body, attachment, keyword, with_body, with_category, page_size, page_token, except_result,
                         except_code, except_msg):
        logger.info("*************** 开始执行用例 ***************")
        result = search_mails(mailbox_ids, start_time, end_time, folders, filters, has_attachment, send, to, subject,
                              body, attachment, keyword, with_body, with_category, page_size, page_token)
        assert result.success == except_result, result.error
        assert result.response.status_code == 200
        assert result.success == except_result, result.error
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert except_msg in result.msg
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s"])
