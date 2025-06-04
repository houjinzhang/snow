import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from conftest import click_element, login,click_element_by_text



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
    click_element(driver,
                  "//*[@id='root']/section/section/section/main/div/div/div[2]/div[1]/div[1]/div[1]/button",
                  "点击部署连接器")
@allure.step("点击linux")
def click_linux(driver):
    click_element_by_text(driver, "span", "Linux")

@allure.step("复制脚本和下载离线安装包，等3s，点击确定")
def click_confirm(driver):
    click_element(driver, '//*[@id="initialData"]/div/div/div[3]/div[2]/div/div/div/div[1]/div[2]/button', "复制脚本")
    click_element(driver, '//*[@id="initialData"]/div/div/div[3]/div[2]/div/div/div/div[1]/div[3]/button', "下载离线安装包")
    click_element_by_text(driver, "span", "确定", timeout=5)
@allure.title("Linux下载")
def test_dow_linux(login):
    driver = login
    with allure.step("点击连接器菜单"):
        click_connector_menu(driver)
    with  allure.step("选择新生成的连接器组（第一个）"):
        select_connector_group(driver)
    with allure.step("部署连接器"):
        deploy_connector(driver)
    with allure.step("点击linux"):
        click_linux(driver)
    with allure.step("复制脚本和下载离线安装包，等3s，点击确定"):
        click_confirm(driver)
        time.sleep(5)

