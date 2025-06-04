import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import click_element, login, click_element_by_text


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
@allure.step("下载win64")
def click_win64(driver):
    click_element(driver,'//*[@id="initialData"]/div/div/div[3]/div[2]/div/div/div/div[1]/button',"下载win64")
@allure.step("下载win32")
def click_win32(driver):
    click_element(driver,'//*[@id="initialData"]/div/div/div[3]/div[2]/div/div/div/div[2]/button',"下载win32")
    click_element_by_text(driver, "span", "确定", timeout=5)
    time.sleep(4)
@allure.title("windows64、32下载")
def  test_download_link(login):
    driver = login
    click_connector_menu(driver)
    select_connector_group(driver)
    deploy_connector(driver)
    click_win64(driver)
    click_win32(driver)