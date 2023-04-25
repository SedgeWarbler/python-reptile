import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains  # 行动动作

url = 'https://passport.bilibili.com/login'
service = Service(executable_path='工具/chromedriver.exe')

driver = webdriver.Chrome(service=service)
driver.get(url)

time.sleep(1)

account = driver.find_element(By.CSS_SELECTOR,
                              '#app > div.login_wp > div.login__main > div.main__right > div.login-pwd > div.tab__form > div:nth-child(1) > input[type=text]')
account.send_keys("17665494182")

password = driver.find_element(By.CSS_SELECTOR,
                               '#app > div.login_wp > div.login__main > div.main__right > div.login-pwd > div.tab__form > div:nth-child(3) > input[type=password]')
password.send_keys('liu19980320')

primary = driver.find_element(By.CSS_SELECTOR, '.btn_primary')
primary.click()

time.sleep(2)
verify = driver.find_element(By.CSS_SELECTOR,
                             'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_panelshowclick > div.geetest_panel_next > div > div > div.geetest_table_box > div.geetest_window > div > div.geetest_item_wrap > img')
verify.screenshot('yzm.png')  # 验证码保存图片

x = 100
y = 200
ActionChains(driver).move_to_element(verify, x, y).click().perform()  # 动作执行，在这个浏览器对应的这个验证码模块  对应的 xy轴进行点击
