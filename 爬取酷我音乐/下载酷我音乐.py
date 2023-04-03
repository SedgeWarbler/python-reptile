import os
from urllib.parse import urlparse

import requests

url = 'https://dl.stream.qqmusic.qq.com/C4000020wJDo3cx0j3.m4a?guid=1234679400&vkey=5BA2472BAF2E33AAB431E7800C66816A111B3FC93B07D5CA01806DCEC9A72B28D0C4D4BC69709A4A036B4BC3E9468CD9E18D6AD91998ACA1&uin=892171962&fromtag=120032'
parsed_url = urlparse(url)  # 解析url

# 获取文件名称和后缀
filename, extension = os.path.splitext(parsed_url.path)

response = requests.get(url)
with open('稻香' + extension, 'wb') as f:
    f.write(response.content)
