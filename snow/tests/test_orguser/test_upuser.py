import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType


@allure.step("找到web测试部门并点击")
def find_web_dept(driver, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="root"]/section/section/section/main/div/div/div[1]/aside/div[1]/div[2]/div/div[2]/div/div[1]/span[3]/span'))
        )
        element.click()
        return True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="找不到部门", attachment_type=AttachmentType.PNG)
        print(f"❌ 找不到部门：{e}")
        return False


@allure.step("点击新添加的用户，修改部门")
def click_add_user(driver, timeout=10):
    try:
        # 显式等待目标元素出现，最多等待10秒
        span = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="arco-link" and contains(text(), "更多")]'))
        )
        span.click()

        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH,
                '//div[contains(@class, "arco-dropdown-menu-item") and contains(text(), "修改部门")]'))
        )
        element.click()
        return True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="点击用户失败", attachment_type=AttachmentType.PNG)
        print(f"❌ 点击用户失败：{e}")
        return False


@allure.step("迁移至部门")
def click_confirm_button(driver, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="department_input"]/div/div[2]'))
        )
        element.click()
        time.sleep(2)

        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="arco-tree-select-popup-0"]/div/div[2]/span[3]'))
        )
        element.click()
        time.sleep(2)

        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH,
                '/html/body/div[3]/div[2]/div/div[2]/div[3]/button[2]'))
        )
        driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
        return True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="迁移部门失败", attachment_type=AttachmentType.PNG)
        print(f"❌ 迁移部门失败：{e}")
        return False


@allure.title('更新用户状态（部门）')
@allure.story('更新用户状态（部门）')
@allure.description('更新用户状态（部门）')
def test_upuser(login):
    driver = login

    with allure.step("步骤1：点击web测试部门"):
        assert find_web_dept(driver), "找不到部门"

    with allure.step("步骤2：点击新添加的用户，修改部门"):
        assert click_add_user(driver), "点击用户失败"

    with allure.step("步骤3：迁移至部门"):
        assert click_confirm_button(driver), "迁移部门失败"

    time.sleep(2)
