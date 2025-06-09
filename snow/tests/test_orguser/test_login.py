import time
import allure
import pytest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="function")
@allure.story("登录功能")
def driver():
    # 设置 Chrome 选项
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # 启用无头模式
    chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速（可选）
    chrome_options.add_argument("--no-sandbox")  # 提高兼容性（可选）
    # 初始化 WebDriver
    service = Service(executable_path='C:/Users/Administrator/Desktop/chromedriver-win64/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    yield driver
    # 测试结束后关闭浏览器
    driver.quit()
@allure.story("登录功能")
@allure.title("登录测试")
@allure.description("测试登录功能")
def test_login(driver):
    driver.get("https://10.2.0.252/")

    # 直接等待并点击 details-button
    print("正在查找 'details-button'")
    details_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "details-button"))
    )
    details_button.click()
    print("已点击 'details-button'")
    # 点击继续前往网址
    print("正在查找 'proceed-link'")
    proceed_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "proceed-link"))
    )
    proceed_link.click()
    print("已点击 'proceed-link'")
    # 使用 XPath 根据 placeholder 定位元素
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="请输入手机号/邮箱"]'))
    )
    # 输入账号密码
    driver.find_element(By.XPATH, '//input[@placeholder="请输入手机号/邮箱"]').send_keys("13332386332")
    driver.find_element(By.XPATH, '//input[@placeholder="请输入密码"]').send_keys("PxCeadN5ac")
    # 点击登录按钮
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    print("登录成功")
    time.sleep(1)
    