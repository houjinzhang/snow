#组织架构用户编辑-更多
import time
import allure
from conftest import click_element, driver,wait_for_clickable_element,input_text

@allure.step("点击组织架构菜单")
def step_1(driver):
    click_element(driver, "//*[@id='root']/section/section/aside/div[1]/div[2]/div/div[1]", "点击组织架构菜单")
@allure.title("组织架构用户编辑-更多-重置第一个部门下，第一个用户的密码，停用用户启用用户")
def step_2(driver):
    # 点击第一个部门
    click_element(driver, "//*[@id='root']/section/section/section/main/div/div/div[1]/aside/div[1]/div[2]/div/div[2]/div/div[1]/span[3]/span", "点击第一个部门")
    
    # 点击"更多"按钮
    click_element(driver, "//span[@class='arco-link' and contains(text(), '更多')]", "点击更多")

    # 点击"停用用户"
    text_click = wait_for_clickable_element(driver, "//div[contains(text(), '停用用户')]")
    text_click.click()

    # 输入停用原因
    input_text(driver, '//*[@id="msg_input"]', "web", "停用原因")

    # 确认停用
    click_element(driver, '/html/body/div[4]/div[2]/div/div[2]/div[3]/button[2]', "点击确定停用")

    # 重新点击"更多"按钮
    click_element(driver, "//span[@class='arco-link' and contains(text(), '更多')]", "点击更多")

    # 点击"删除用户"
    test_click = wait_for_clickable_element(driver, "//div[contains(text(), '删除用户')]")
    test_click.click()

    # 确认删除
    click_element(driver, '/html/body/div[3]/div[2]/div/div[2]/div[3]/div/div[2]/button', "点击确定删除")


@allure.step("删除第一个部门")
def step_3(driver):
    # 点击第一个部门
    click_element(driver,
                  "//*[@id='root']/section/section/section/main/div/div/div[1]/aside/div[1]/div[2]/div/div[2]/div/div[1]/span[3]/span",
                  "点击第一个部门")


@allure.step("点击三个点查看")
def step_4(driver):
    click_element(driver,
                  "//*[@id='root']/section/section/section/main/div/div/div[1]/aside/div[1]/div[2]/div/div[2]/div/div[1]/div",
                  "点击三个点")

    # 点击“删除部门”
    text_click = wait_for_clickable_element(driver, "//div[contains(text(), '删除')]")
    text_click.click()

    time.sleep(5)
    click_element(driver, '/html/body/div[3]/div[2]/div/div[2]/div[3]/button[2]', "点击确定删除")


def test_case_1(login):
    driver =  login
    step_1(driver)
    step_2(driver)
    step_3(driver)
    step_4(driver)
