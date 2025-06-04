import time
import allure
import pytest
import faker
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import click_element, driver, login

fake =  faker.Faker(locale='zh_CN')

@pytest.fixture(scope="module")
def zh():
    """生成随机的账号，使用faker生成不同账号"""
    return faker.Faker().unique.user_name()
@pytest.fixture(scope="module")
def name():
    """生成随机的姓名，使用faker生成不同姓名（3字中文名字）"""
    first_name = fake.first_name()
    second_name = fake.last_name()
    third_name = fake.last_name()
    return f"{first_name}{second_name}{third_name}"



@allure.step("找到web测试部门并点击")
def find_web_dept(driver):
    click_element(driver,
                  xpath='//*[@id="root"]/section/section/section/main/div/div/div[1]/aside/div[1]/div[2]/div/div[2]/div/div[1]/span[3]/span',
                  step_name="点击的一个部门")
@allure.step("添加用户")
def click_add_user(driver):
    click_element(driver,
                  xpath="//*[@id='root']/section/section/section/main/div/div/div[2]/div[1]/div[2]/div[1]/div/button",
                  step_name="点击添加用户按钮")
@allure.step("输入账号: faker随机账号")
def input_account(driver,zh):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='username_input']"))
    )
    element.send_keys(zh)


@allure.step("输入姓名: faker随机姓名")
def input_name(driver,name):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='fullname_input']"))
    )
    element.send_keys(name)

@pytest.fixture(scope="module")
def phone():
    """使用faker生成中国地区11位手机号，确保以133开头"""
    suffix = fake.random_int(min=0, max=99999999)  # 生成 0 ~ 99999999 之间的整数
    return f"133{suffix:08d}"  # 格式化为 8 位，不足补零
def input_phone(driver,phone):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='mobile']/div/div/div[2]/span/span/input"))
    )
    element.send_keys(phone)

@pytest.fixture(scope="module")
def email():
    return faker.Faker().unique.email()
@allure.step("输入邮箱: faker随机email")
def input_email(driver, email="web@test.com"):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='email_input']"))
    )
    element.send_keys(email)


@allure.step("双击密码框")
def double_click_password(driver):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//*[@id='password']/div/div/div[1]/div/div/div/div/div/div/div/span/span/input"))
    )
    element.click()
    element.click()


@allure.step("清空密码框")
def clear_password(driver):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//*[@id='password']/div/div/div[1]/div/div/div/div/div/div/div/span/span/input"))
    )
    element.clear()


@allure.step("输入密码: {password}")
def input_password(driver, password="Hou800828"):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//*[@id='password']/div/div/div[1]/div/div/div/div/div/div/div/span/span/input"))
    )
    element.send_keys(password)


@allure.step("点击保存按钮")
def click_save(driver):
    click_element(driver,
                  xpath="/html/body/div[3]/div[2]/div/div/div[3]/button[2]",
                  step_name="点击保存按钮")


@allure.step("验证用户是否添加成功")
def verify_user_addition(driver):
    try:
        # 定位账号已存在的错误提示元素
        error_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '账号已存在')]"))
        )
        time.sleep(2)
        return False, "错误：账号已经存在"
    except TimeoutException:
        # 如果3秒内未找到错误提示，认为用户添加成功
        return True, "用户添加成功"
@allure.story("用户管理 - 用户添加")
@allure.title("测试用户添加流程")
@allure.description("测试用户添加功能")
def test_user(login,zh,name,email,phone):
    driver = login

    with allure.step("步骤1：进入web测试部门"):
        find_web_dept(driver)

    with allure.step("步骤2：点击添加用户按钮"):
        click_add_user(driver)

    with allure.step("步骤3：输入账号信息"):
        input_account(driver,zh)

    with allure.step("步骤4：输入用户姓名"):
        input_name(driver,name)

    with allure.step("步骤5：输入手机号码"):
        input_phone(driver,phone)

    with allure.step("步骤6：输入邮箱地址"):
        input_email(driver,email)

    with allure.step("步骤7：双击密码框"):
        double_click_password(driver)

    with allure.step("步骤8：清空默认密码"):
        clear_password(driver)

    with allure.step("步骤9：设置新密码"):
        input_password(driver)

    with allure.step("步骤10：点击保存按钮"):
        click_save(driver)
    with allure.step("步骤11：验证添加结果"):
        success, message = verify_user_addition(driver)
        if success:
            assert True, message
        else:
            assert False, message
        allure.attach(driver.get_screenshot_as_png(), name="用户添加结果截图",
                      attachment_type=allure.attachment_type.PNG)
        time.sleep(10)