import time
import random
import string
import allure
import faker
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

fake =  faker.Faker(locale='zh_CN')


def pytest_collection_modifyitems(config, items):
    """控制测试用例执行顺序"""
    order = [

    ]

    # 构建一个字典用于快速查找优先级
    name_to_order = {name: index for index, name in enumerate(order)}

    # 按照指定顺序排序
    items.sort(key=lambda x: name_to_order.get(x.name, float('inf')))

    # 打印排序后的测试用例名称，用于调试
    print("排序后的测试用例：")
    for item in items:
        print(item.name)

@pytest.fixture(scope="function")
def driver():
    service = Service(executable_path='C:/Users/Administrator/Desktop/chromedriver-win64/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def login(driver):
    driver.get("https://10.2.0.252/")

    # 点击证书警告页按钮
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "details-button"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "proceed-link"))
    ).click()

    # 输入账号密码并登录
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="请输入手机号"]'))
    )

    driver.find_element(By.XPATH, '//input[@placeholder="请输入手机号"]').send_keys("13332386332")
    driver.find_element(By.XPATH, '//input[@placeholder="请输入密码"]').send_keys("PxCeadN5ac")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    return driver

def click_element(driver, xpath, step_name):
    """通用点击操作封装"""
    with allure.step(step_name):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            return True
        except TimeoutException:
            allure.attach(driver.get_screenshot_as_png(), name=f"{step_name}_超时", attachment_type=AttachmentType.PNG)
            raise
#文本点击
def wait_for_clickable_element(driver, xpath, timeout=10):
    """
    等待指定的元素变为可点击状态
    :param driver: WebDriver 实例
    :param xpath: 要查找的元素 XPath
    :param timeout: 最大等待时间
    :return: 找到的 WebElement
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        return element
    except Exception as e:
        raise TimeoutError(f"等待元素可点击失败: {xpath}") from e

def click_element(driver, xpath, step_name):
    """通用点击操作封装"""
    with allure.step(step_name):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            return True
        except TimeoutException:
            allure.attach(driver.get_screenshot_as_png(), name=f"{step_name}_超时", attachment_type=AttachmentType.PNG)
            raise

def js_click_element(driver, xpath, step_name):
    """使用 JS 强制点击元素并记录日志"""
    with allure.step(f"JS点击: {step_name}"):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name=f"{step_name}_错误截图", attachment_type=allure.attachment_type.PNG)
            raise
@pytest.fixture(scope="session")
def shared_data():
    return {}
def generate_random_string(length=6):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_phone():
    """生成随机手机号（中国格式）"""
    return "1" + "".join(random.choices(string.digits, k=10))

def generate_random_email(username_length=6):
    """生成随机邮箱"""
    username = generate_random_string(username_length)
    return f"{username}@example.com"

@pytest.fixture(scope="session")
def department_name():
        """生成随机部门名称，格式为 '测试部门-XX'，并返回该名称"""
        base_name = "测试部门-"
        random_number = random.randint(10, 99)  # 生成10到99之间的随机数
        return f"{base_name}{random_number}"

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

@pytest.fixture(scope="module")
def phone():
        """使用faker生成中国地区11位手机号，确保以133开头"""
        suffix = fake.random_int(min=0, max=99999999)  # 生成 0 ~ 99999999 之间的整数
        return f"133{suffix:08d}"  # 格式化为 8 位，不足补零

@pytest.fixture(scope="module")
def email():
        return faker.Faker().unique.email()

    # input——test文本封装
def input_text(driver, xpath, text, step_name, retry=3):
        """通用输入文本操作封装 + 自动重试"""
        with allure.step(step_name):
            for i in range(retry):
                try:
                    input_box = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, xpath))
                    )
                    input_box.clear()  # 可选：清除旧内容
                    input_box.send_keys(text)
                    return True
                except StaleElementReferenceException as e:
                    if i < retry - 1:
                        print(f"元素过期，第 {i + 1} 次重试...")
                        time.sleep(1)
                    else:
                        allure.attach(driver.get_screenshot_as_png(), name=f"{step_name}_超时",
                                      attachment_type=AttachmentType.PNG)
                        raise e
            raise TimeoutException(f"无法输入文本到元素：{xpath}")
@allure.step("根据文本查找元素并点击")
def click_element_by_text(driver, tag_name, text, timeout=10):
    try:
        xpath = f'//{tag_name}[contains(text(), "{text}")]'
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
        return True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name=f"点击 {text} 失败",
                      attachment_type=allure.attachment_type.PNG)
        print(f"点击 {text} 失败: {e}")
        return False