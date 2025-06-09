import time
import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def pytest_collection_modifyitems(config, items):
    """控制测试用例执行顺序"""
    order = [
        "test_link",
        "test_download_link",
        "test_dow_linux",
        "test_recreate"
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
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="请输入手机号/邮箱"]'))
    )

    driver.find_element(By.XPATH, '//input[@placeholder="请输入手机号/邮箱"]').send_keys("13332386332")
    driver.find_element(By.XPATH, '//input[@placeholder="请输入密码"]').send_keys("PxCeadN5ac")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    return driver

def click_element(driver, xpath, step_name, retry=3):
    """通用点击操作封装 + 自动重试"""
    with allure.step(step_name):
        for i in range(retry):
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                element.click()
                return True
            except StaleElementReferenceException as e:
                if i < retry - 1:
                    print(f"元素过期，第 {i+1} 次重试...")
                    time.sleep(1)
                else:
                    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name}_超时", attachment_type=AttachmentType.PNG)
                    raise e
        raise TimeoutException(f"无法点击元素：{xpath}")
#input——test文本封装
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
                    print(f"元素过期，第 {i+1} 次重试...")
                    time.sleep(1)
                else:
                    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name}_超时", attachment_type=AttachmentType.PNG)
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



#页面错误信息通用函数
@allure.step("检查是否存在错误提示")
def check_error_message(driver, message_text, timeout=5):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, f'//*[contains(text(), "{message_text}")]'))
        )
        print(f"发现错误提示: {element.text}")
        allure.attach(driver.get_screenshot_as_png(), name="错误提示", attachment_type=AttachmentType.PNG)
        return True
    except TimeoutException:
        return False


