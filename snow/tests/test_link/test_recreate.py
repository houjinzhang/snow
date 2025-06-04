import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from conftest import click_element, login,click_element_by_text

from faker import Faker
fake = Faker('zh_CN')
@pytest.fixture()
def link_name():
    """使用faker随机生成连接器组名称"""
    return fake.name()
@allure.step("点击连接器菜单")
def click_connector_menu(driver):
    return click_element(driver,
                         '//*[@id="root"]/section/section/aside/div[1]/div[2]/div/div[3]',
                         "进入连接器")
@allure.step("选择新生成的连接器组（第一个）")
def select_connector_group(driver):
    click_element(driver,'//*[@id="root"]/section/section/section/main/div/div/div[1]/aside/div/div[3]/div/div/div/div[1]',
                  "选择新生成的连接器组")
@allure.step("部署连接器")
def deploy_connector(driver):
    return click_element(driver,
                  "//*[@id='root']/section/section/section/main/div/div/div[2]/div[1]/div[1]/div[1]/button",
                  "点击部署连接器")


@allure.step("点击重新生成")
@allure.step("点击重新生成")
def click_renew_button(driver):
    try:
        click_element_by_text(driver, "span", "重新生成")
        click_element(driver, '/html/body/div[4]/span/div[1]/div/div/div[2]/button[2]', "确定")
        click_element_by_text(driver, "span", "确定", timeout=5)
        return True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="点击重新生成失败", attachment_type=allure.attachment_type.PNG)
        print(f"点击重新生成失败: {e}")
        return False

@allure.title("重新生成安装包")
def test_recreate(login):
    driver = login
    click_connector_menu(driver)
    select_connector_group(driver)
    deploy_connector(driver)
    click_renew_button(driver)



