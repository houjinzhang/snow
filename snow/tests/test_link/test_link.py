import time

from allure_commons.types import AttachmentType
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.wait import WebDriverWait
from conftest import click_element,input_text,check_error_message



@allure.step("点击连接器菜单")
def click_connector_menu(driver):
    return click_element(driver,
                         '//*[@id="root"]/section/section/aside/div[1]/div[2]/div/div[3]',
                         "进入连接器")


@allure.step("点击新建连接器组加号")
def click_link_menu(driver):
    try:
        icon = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'arco-icon-plus'))
        )
        icon.click()
        return True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="点击加号失败", attachment_type=AttachmentType.PNG)
        print(f"点击元素失败: {e}")
        return False
@allure.step("输入名称webtest")
def input_link_name(driver):
    return input_text(driver,
                      '//*[@id="name_input"]',
                      "webtest",
                      "输入名称")
@allure.step("输入描述")
def input_link_desc(driver):
    try:
        input_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="description_input"]'))
        )
        input_box.send_keys("web测试")
        return True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="截图", attachment_type=allure.attachment_type.PNG)
        print(f"输入描述失败: {e}")
@allure.step("点击确定按钮")
def click_confirm_button(driver):
    try:
        # 点击确定按钮
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[span[text()="确定"]]'))
        )
        confirm_button.click()

        if check_error_message(driver, "连接器组名称重复", 3):
            return False

        return True

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="点击确定失败", attachment_type=AttachmentType.PNG)
        print(f"点击确定按钮失败: {e}")
        return False


    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="点击确定失败", attachment_type=AttachmentType.PNG)
        print(f"点击确定按钮失败: {e}")
        return False


@allure.feature("连接器管理")
@allure.story("创建连接器组")
@allure.title("创建连接器组")
def test_link(login):
    driver = login

    # 步骤1：点击连接器菜单
    assert click_connector_menu(driver), "点击连接器菜单失败"

    # 步骤2：点击新建连接器组加号
    assert click_link_menu(driver), "点击新建连接器组加号失败"

    # 步骤3：输入名称webtest
    assert input_link_name(driver), "输入名称失败"

    # 步骤4：输入描述
    assert input_link_desc(driver), "输入描述失败"

    # 步骤5：点击确定按钮
    click_confirm_button(driver)

    time.sleep(5)

