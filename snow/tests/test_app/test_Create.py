import random
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure
from allure_commons.types import AttachmentType
from conftest import click_element

@pytest.fixture(scope="function")
def app_name():
    """生成随机应用名称，格式为'应用-xx'"""
    random_string = random.randint(10, 99)  # 生成10到99之间的随机数
    return f"应用-{random_string}"
@pytest.fixture(scope="function")
def app_ip():
    """生成随机id地址，格式为***.qq.com"""
    random_string = random.randint(10, 99)
    return f"web{random.randint(1000, 9999)}.qq.com"
@pytest.fixture(scope="function")
def app_ip2():
    """生成随机关联id地址，格式为ab**.qq.com"""
    random_string = random.randint(10, 99)
    return f"*{random.randint(1000, 9999)}.qq.com"
@allure.step("点击菜单中的应用")
def click_app_menu(driver):
    return click_element(driver, "//*[@id='root']/section/section/aside/div[1]/div[2]/div/div[2]", "点击菜单中的应用")


@allure.step("点击创建按钮")
def click_create_button(driver):
    return click_element(driver, "//*[@id='root']/section/section/section/main/div/div/div[2]/div[1]/div[1]/button", "点击创建按钮")


@allure.step("输入应用名称")
def input_app_name(driver,  app_name):
    input_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='name_input']"))
    )
    input_box.send_keys(app_name)


@allure.step("设置地址类型 https://")
def set_address_type_https(driver,  app_ip):
    # 定位 HTTPS 下拉图标并点击
    if not click_element(driver, "//*[@id='website']/div/div/div[1]/div/span/span", "展开HTTPS下拉框"):
        return False
    time.sleep(5)

    # 显式选择 HTTPS 协议项（例如第一个选项），如果点击失败则重试一次
    if not click_element(driver, "//*[@id='arco-select-popup-6']//li[contains(text(), 'https://')]", "选择HTTPS协议") and not click_element(driver, "//*[@id='arco-select-popup-6']//li[contains(text(), 'https://')]", "选择HTTPS协议（重试）"):       return False
    # 输入域名
    input_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='website']/div/div/input"))
    )
    input_box.send_keys(app_ip)
    return True


@allure.step("输入关联 IP")
def input_associated_ip(driver,  app_ip2):
    input_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='relationAddress_input']"))
    )
    input_box.send_keys(app_ip2)


@allure.step("选择连接器组")
def select_connector_group(driver):
    # 定位下拉框并点击打开选项列表
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
        # 等待最多 10 秒，查找“创建成功”提示
        success_text = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '创建成功')]"))
        )
        assert success_text.is_displayed(), "未显示创建成功提示"

        # 添加 Allure 日志与截图
        with allure.step("✅ 创建成功"):
            allure.attach(driver.get_screenshot_as_png(), name="创建成功截图", attachment_type=AttachmentType.PNG)

        return True

    except (TimeoutException, NoSuchElementException, AssertionError):
        # 捕获所有可能的异常类型
        with allure.step("❌ 创建失败"):
            allure.attach(driver.get_screenshot_as_png(), name="创建失败截图", attachment_type=AttachmentType.PNG)
        raise AssertionError("创建失败：应用重复了")


@allure.step("测试流程：创建应用")
@allure.story("创建应用")
@allure.title("创建应用")
def test_Create(login,app_name,app_ip,app_ip2):
    driver = login

    with allure.step("步骤1：点击菜单中的应用"):
        assert click_app_menu(driver), "点击菜单中的应用失败"
    with allure.step("步骤2：点击创建按钮"):
        assert click_create_button(driver), "点击创建按钮失败"
    with allure.step("步骤3：输入应用名称"):
        input_app_name(driver,app_name)
    with allure.step("步骤4：设置地址类型 HTTPS"):
        assert set_address_type_https(driver, app_ip), "设置地址类型HTTPS失败"
    with allure.step("步骤5：输入关联 IP 地址"):
        input_associated_ip(driver, app_ip2)
    with allure.step("步骤6：选择连接器组"):
        assert select_connector_group(driver), "选择连接器组失败"
    with allure.step("步骤7：选择 test 选项"):
        assert select_test(driver), "选择test选项失败"
    with allure.step("步骤8：提交创建"):
        assert submit_create_application(driver), "提交创建失败"
    with allure.step("步骤9：检查创建结果"):
        assert check_create_result(driver), "创建结果验证失败"


