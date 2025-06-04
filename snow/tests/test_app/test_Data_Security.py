import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import click_element, login


@allure.step("点击菜单中的应用")
def click_app_menu(driver, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="root"]/section/section/aside/div[1]/div[2]/div/div[2]'))
        )
        element.click()
        return True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="点击菜单失败", attachment_type=allure.attachment_type.PNG)
        print(f"❌ 点击菜单失败: {e}")
        return False


@allure.step("找到新建立的应用并点击【配置】按钮")
def find_app_config_button(driver, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="root"]/section/section/section/main/div/div/div[2]/div[1]/div[2]'
                '/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[7]/div/span/div/div[1]/span'))
        )
        element.click()
        return True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="找不到配置按钮", attachment_type=allure.attachment_type.PNG)
        print(f"❌ 找不到配置按钮: {e}")
        return False


@allure.step("点击数据安全")
def click_data_security(driver, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="root"]/section/section/section/div/div[3]/div[3]/span'))
        )
        element.click()
        return True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="点击数据安全失败", attachment_type=allure.attachment_type.PNG)
        print(f"❌ 点击数据安全失败: {e}")
        return False


@allure.step("配置数据安全策略")
def click_download_control(driver, timeout=10):
    try:
        # 点击下载管控
        download_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="download"]/div/div/div/div[1]/button'))
        )
        download_button.click()

        # 点击文件类型下拉框
        file_type_dropdown = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="download"]/div/div/div[2]/div/div[1]/div/div[1]/div/div/input'))
        )
        file_type_dropdown.click()

        # 选择“全部”文件类型
        all_option = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH,
                '//div[contains(@class, "arco-cascader-list-item") and normalize-space()="全部"]'))
        )
        all_option.click()

        # 下载规则
        download_rule = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="download"]/div/div/div[2]/div/div[2]/div'))
        )
        download_rule.click()

        # 转存到网盘
        save_to_cloud = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "转存到【网盘】")]'))
        )
        save_to_cloud.click()

        # 允许使用网盘文件
        allow_cloud = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="uploadControl"]/div/span/label/span[1]/div'))
        )
        allow_cloud.click()

        return True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="配置数据安全失败", attachment_type=allure.attachment_type.PNG)
        print(f"❌ 配置数据安全失败: {e}")
        return False


@allure.step("点击保存")
def click_save(driver, timeout=10):
    try:
        save_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="root"]/section/section/section/main/div/div/div[2]/div[3]/div/div/button'))
        )
        save_button.click()
        return True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="点击保存失败", attachment_type=allure.attachment_type.PNG)
        print(f"❌ 点击保存失败: {e}")
        return False


@allure.title("数据安全")
@allure.story("数据安全操作")
@allure.description("数据安全操作")
def test_Data_Security(login):
    driver = login

    with allure.step("步骤1：点击菜单中的应用"):
        assert click_app_menu(driver), "点击菜单中的应用失败"

    with allure.step("步骤2：找到新建立的应用并点击【配置】按钮"):
        assert find_app_config_button(driver), "找不到配置按钮"


    with allure.step("步骤3：点击数据安全"):
        assert click_data_security(driver), "点击数据安全失败"
        time.sleep(2)

    with allure.step("步骤4：配置数据安全策略"):
        assert click_download_control(driver), "配置数据安全失败"
        time.sleep(2)

    with allure.step("步骤5：点击保存"):
        assert click_save(driver), "点击保存失败"

    time.sleep(2)
