import sys

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

"""
    需要下载 chromedriver 且与自己安装的浏览器版本一样，详情可以查百度
"""

# 设置浏览器选择
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)  # 不自动关闭浏览
# 这里操作会打开浏览器
service = Service('../chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.douyin.com/user/MS4wLjABAAAA4N4OrZzTSmCPp8vVAqCeyU215Kav2JgFv2Lfy4DNWRs')
# driver.execute_script(js)  #可以执行js

# 这里设置十秒秒的原因是让手动操作完验证码之后页面加载出来在执行后面的代码流程  阻塞后面的步骤
time.sleep(5)

# 默认执行js，下拉到最底部
for i in range(5):
    time.sleep(1)
    driver.execute_script("document.documentElement.scrollTop=document.documentElement.scrollHeight+500")

# By.CSS_SELECTOR 表示通过什么元素标识去获取
list = driver.find_elements(By.CSS_SELECTOR,
                            '#douyin-right-container > div._bEYe5zo > div > div > div:nth-child(3) > div.mwo84cvf > div.wwg0vUdQ > div.UFuuTZ1P > ul > li')

for li in list:
    video_url = li.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    print(video_url)
