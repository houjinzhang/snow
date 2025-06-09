# test_Create.py

import random
import time
import allure
import pytest
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from conftest import click_element


# =================== Fixtures ===================
@pytest.fixture(scope="function")
def app_name():
    """生成随机应用名称，格式为'应用-时间戳+随机数'"""
    return f"应用-{int(time.time())}-{random.randint(1000, 9999)}"


@pytest.fixture(scope="function")
def app_ip():
    """生成随机IP地址，格式为webxxxx.qq.com"""
    return f"web{random.randint(1000, 9999)}.qq.com"


@pytest.fixture(scope="function")
def app_ip2():
    """生成随机关联IP地址，格式为*xxxx.qq.com"""
    return f"*{random.randint(1000, 9999)}.qq.com"


# =================== 工具函数 ===================
@allure.step("点击菜单中的应用")
def click_app_menu(driver):
    return click_element(driver, "//*[@id='root']/section/section/aside/div[1]/div[2]/div/div[2]", "点击菜单中的应用")


@allure.step("点击创建按钮")
def click_create_button(driver):
    return click_element(driver, "//*[@id='root']/section/section/section/main/div/div/div[2]/div[1]/div[1]/button", "点击创建按钮")


@allure.step("输入应用名称")
def input_app_name(driver, app_name):
    input_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='name_input']"))
    )
    input_box.clear()
    input_box.send_keys(app_name)
    allure.attach(driver.get_screenshot_as_png(), name="输入应用名称后截图", attachment_type=AttachmentType.PNG)
    return True


@allure.step("设置地址类型 HTTPS")
def set_address_type_https(driver, app_ip):
    # 展开下拉框
    assert click_element(driver, '//*[@id="website"]/div/div/div[1]', "设置地址类型 HTTPS"), "展开HTTPS下拉框失败"

    # 选择 HTTPS 协议项
    assert click_element(driver, '//li[@class="arco-select-option"]', "选择https：//"), "选择HTTPS协议失败"
    time.sleep(1)

    # 定位网址输入框并设置值
    input_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='website']/div/div/input"))
    )

    # 强制聚焦 + 清空原有内容
    driver.execute_script("arguments[0].focus();", input_box)
    input_box.clear()

    # 使用 JS 设置值并触发事件
    driver.execute_script("""
        arguments[0].value = arguments[1];
        var event = new Event('input', { bubbles: true });
        arguments[0].dispatchEvent(event);
    """, input_box, app_ip)

    allure.attach(driver.get_screenshot_as_png(), name="设置HTTPS地址后截图", attachment_type=AttachmentType.PNG)
    return True


@allure.step("输入关联 IP 地址")
def input_associated_ip(driver, app_ip2):
    input_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='relationAddress_input']"))
    )
    input_box.clear()

    driver.execute_script("""
        arguments[0].value = arguments[1];
        var event = new Event('input', { bubbles: true });
        arguments[0].dispatchEvent(event);
    """, input_box, app_ip2)

    allure.attach(driver.get_screenshot_as_png(), name="输入关联IP后截图", attachment_type=AttachmentType.PNG)
    return True


@allure.step("选择连接器组")
def select_connector_group(driver):
    return click_element(driver, "//*[@id='networkId']/div/div/div[1]/div/div", "打开连接器组下拉框")


@allure.step("选择 test 选项")
def select_test(driver):
    return click_element(driver, "/html/body/div[3]/span/div", "选择test选项")


@allure.step("提交创建")
def submit_create_application(driver):
    return click_element(driver, "//*[@id='root']/section/section/section/main/div/div[2]/div/div[1]/button", "提交创建")


@allure.step("检查创建结果")
def check_create_result(driver):
    try:
        success_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(., '创建成功')]"))
        )
        assert success_text.is_displayed(), "未显示创建成功提示"
        allure.attach(driver.get_screenshot_as_png(), name="创建成功截图", attachment_type=AttachmentType.PNG)
        return True

    except (TimeoutException, NoSuchElementException, AssertionError):
        allure.attach(driver.get_screenshot_as_png(), name="创建失败截图", attachment_type=AttachmentType.PNG)
        raise AssertionError("创建失败：应用重复或未正确显示成功提示")


# =================== 测试用例 ===================
@allure.feature("应用管理")
@allure.story("创建应用")
@allure.title("测试流程：创建应用")
def test_Create(login, app_name, app_ip, app_ip2):
    driver = login

    with allure.step("步骤1：点击菜单中的应用"):
        assert click_app_menu(driver), "点击菜单中的应用失败"

    with allure.step("步骤2：点击创建按钮"):
        assert click_create_button(driver), "点击创建按钮失败"

    with allure.step("步骤3：输入应用名称"):
        assert input_app_name(driver, app_name), "输入应用名称失败"

    with allure.step("步骤4：设置地址类型 HTTPS"):
        assert set_address_type_https(driver, app_ip), "设置地址类型HTTPS失败"

    with allure.step("步骤5：输入关联 IP 地址"):
        assert input_associated_ip(driver, app_ip2), "输入关联IP失败"

    with allure.step("步骤6：选择连接器组"):
        assert select_connector_group(driver), "选择连接器组失败"

    with allure.step("步骤7：选择 test 选项"):
        assert select_test(driver), "选择test选项失败"

    with allure.step("步骤8：提交创建"):
        assert submit_create_application(driver), "提交创建失败"

    with allure.step("步骤9：检查创建结果"):
        assert check_create_result(driver), "创建结果验证失败"

    time.sleep(2)  # 可视化观察等待
