import pytest
import allure
# from operation.user import get_all_user_info, get_one_user_info
from operation.mailboxes import get_mailboxes
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
@allure.feature("邮箱列表")
class TestMailboxes():
    """邮箱列表"""

    @allure.story("用例--获取邮箱列表")
    @allure.title("测试用例：【获取邮箱列表】")
    @pytest.mark.single
    @pytest.mark.parametrize("except_result,except_code,except_msg",
                             api_data["test_MailBoxes"])
    def test_MailBoxes(self,  except_result,except_code, except_msg):
        logger.info("*************** 开始执行用例 ***************")
        result = get_mailboxes()
        assert result.success == except_result, result.error
        assert result.response.status_code == 200
        assert result.success == except_result, result.error
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert except_msg in result.msg
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s"])
