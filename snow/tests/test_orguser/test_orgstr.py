import allure
import pytest
import random
import time
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import click_element, driver, login

@pytest.fixture(scope="function")
def department_name():
    """生成随机部门名称，格式为 '测试部门-XX'"""
    random_number = random.randint(10, 99)  # 生成10到99之间的随机数
    return f"测试部门-{random_number}"

@allure.step("点击组织架构菜单")
def click_organization_menu(driver):
    click_element(driver, "//*[@id='root']/section/section/aside/div[1]/div[2]/div/div[1]", "点击组织架构菜单")

@allure.step("点击加号按钮新建部门")
def click_add_department_button(driver):
    click_element(driver, "//*[@id='root']/section/section/section/main/div/div/div[1]/aside/div[1]/div[2]/div/div[1]/div[2]", "点击添加部门按钮")

@allure.step("输入部门名称：{department_name}")
def input_department_name(driver, department_name):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='name_input']"))
    )
    element.send_keys(department_name)

@allure.step("点击确定按钮保存部门")
def click_confirm_button(driver):
    click_element(driver, "/html/body/div[3]/div[2]/div/div[3]/button[2]", "点击确定按钮")

@allure.step("定位到xpath判断添加失败")
def find_xpath(driver, department_name):
    try:
        # 尝试定位元素，设置最长等待时间为3秒
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div/div[3]/button[2]"))
        )
        # 如果找到了元素，说明步骤失败
        return False, f"步骤失败：部门存在，添加失败。"
    except (TimeoutException, NoSuchElementException):
        # 如果没有找到元素，说明步骤成功
        return True, "步骤成功：部门不存在，添加成功。"

@allure.story("添加部门")
@allure.title("测试添加部门功能流程")
@allure.description("测试添加部门功能流程")
def test_orgstr(login, department_name):
    driver = login

    with allure.step("步骤1：进入组织架构菜单"):
        click_organization_menu(driver)

    with allure.step("步骤2：点击添加部门按钮"):
        click_add_department_button(driver)

    with allure.step(f"步骤3：输入部门名称：{department_name}"):
        input_department_name(driver, department_name)  # 确保传递 department_name 参数

    with allure.step("步骤4：点击确定按钮"):
        click_confirm_button(driver)
        time.sleep(2)

    with allure.step("步骤5：检查部门添加结果"):
        success, message = find_xpath(driver, department_name)  # 确保传递 department_name 参数
        allure.attach(driver.get_screenshot_as_png(), name="部门添加结果截图", attachment_type=allure.attachment_type.PNG)

        if success:
            assert True, message
        else:
            assert False, message