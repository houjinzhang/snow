import time

import allure
from conftest import click_element

@allure.step("点击菜单中的应用")
def click_app_menu(driver):
    return click_element(driver, "//*[@id='root']/section/section/aside/div[1]/div[2]/div/div[2]", "点击菜单中的应用")
@allure.step("点击删除按钮")
def click_delete_button(driver):
    return click_element(driver,  '//*[@id="root"]/section/section/section/main/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[7]/div/span/div/div[2]/span', "点击删除按钮")
@allure.step("点击确认删除按钮")
def click_confirm_delete_button(driver):
    return click_element(driver, '/html/body/div[3]/div[2]/div/div[2]/div[3]/button[2]',  "点击确认删除按钮")





def test_case_appdel(login):
    driver = login
    click_app_menu(driver)
    click_delete_button(driver)
    click_confirm_delete_button(driver)
    time.sleep(1)