from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import allure
from allure_commons.types import AttachmentType
import time

from conftest import click_element


@allure.step("点击菜单中的应用")
def click_app_menu(driver):
    click_element(driver,
                  '//*[@id="root"]/section/section/aside/div[1]/div[2]/div/div[2]',
                  "点击菜单中的应用")


@allure.step("找到新建立的应用并点击【配置】按钮")
def find_app_config_button(driver):
    click_element(driver,
                  '//*[@id="root"]/section/section/section/main/div/div/div[2]/div[1]/div[2]'
                  '/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[7]/div/span/div/div[1]/span',
                  "查找配置按钮")

@allure.step("点击行为管控")
def click_behavior_control(driver):
    if click_element(driver,
                     '//*[@id="root"]/section/section/section/div/div[3]/div[2]/span',
                     "点击行为管控"):
        with allure.step("✅ 点击行为管控成功"):
            allure.attach(driver.get_screenshot_as_png(), name="点击行为管控成功",
                          attachment_type=AttachmentType.PNG)

@allure.step("勾选行为管控策略项")
def select_behavior_control_options(driver):
    options_xpaths = [
        ('禁用开发者工具', '//*[@id="funlimit"]/div/span/label[1]/span[1]/div'),
        ('禁用另存为', '//*[@id="funlimit"]/div/span/label[2]/span[1]/div'),
        ('禁用打印', '//*[@id="funlimit"]/div/span/label[3]/span[1]/div'),
        ('禁止截屏/录屏/共享屏幕', '//*[@id="funlimit"]/div/span/label[4]/span[1]/div'),
        ('启动数字水印', '//*[@id="watermark"]/div/div/div/div/button')
    ]

    for label, xpath in options_xpaths:
        with allure.step(f"勾选 {label}"):
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                element.click()
            except StaleElementReferenceException:
                # 如果出现 stale 元素，重新查找再点击
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                element.click()
            except TimeoutException:
                allure.attach(driver.get_screenshot_as_png(), name=f"{label}_Timeout",
                              attachment_type=AttachmentType.PNG)
                raise


@allure.step("保存策略配置")
def save_strategy_configuration(driver):
    if click_element(driver,
                     '//*[@id="root"]/section/section/section/main/div/div/div[2]/div[3]/div/div/button',
                     "保存策略配置"):
        with allure.step("✅ 策略配置已保存"):
            allure.attach(driver.get_screenshot_as_png(), name="创建成功截图",
                          attachment_type=AttachmentType.PNG)


@allure.step("测试流程：配置行为管控策略")
@allure.story("配置行为管控策略")
@allure.title("测试流程：配置行为管控策略")
def test_strategy(login):
    driver = login

    with allure.step("步骤1：点击菜单中的应用"):
        click_app_menu(driver)
        time.sleep(2)
    with allure.step("步骤2：找到新建立的应用并点击配置"):
        find_app_config_button(driver)
        time.sleep(2)
    with allure.step("步骤3：点击行为管控"):
        click_behavior_control(driver)
        time.sleep(2)
    with allure.step("步骤4：勾选行为管控策略选项"):
        select_behavior_control_options(driver)
        time.sleep(2)
    with allure.step("步骤5：保存策略配置"):
        save_strategy_configuration(driver)
        time.sleep(2)
    # 可选等待时间，便于观察结果
    time.sleep(5)
