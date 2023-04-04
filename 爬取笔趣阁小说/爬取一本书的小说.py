"""
爬取整本小说
"""
import os
import requests
import parsel
import re


# 小说章节处理
def section(name, href):
    response = requests.get(href)

    selector = parsel.Selector(response.text)

    title = selector.css(".content .wap_none::text").get()  # 获取章节名称
    content = selector.css("#chaptercontent::text").getall()
    content = "\n\n".join(content)

    f = open(name + "\\" + title + ".txt", mode="w", encoding='utf-8')
    f.write(content)


url = "https://www.biquge9.com/book/1198/"  # 小说目录
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

# 获取目录下面所有章节
response = requests.get(url, header)

selector = parsel.Selector(response.text)
name = selector.css(".info h1::text").get()  # 获取小说名称
# name = selector.css(".info h1::attr(helf)").get()  # 可以获取标签里面的属性

# 创建小说名称目录
if not os.path.exists(name):
    os.mkdir(name)

# 通过正则获取小说所有章节链接
href = re.findall('<dd><a href ="(.*?)">.*?</a></dd>', response.text)
# re.sub(".*?","",title) #正则替换 替换的是整个匹配到的内容

for index in href:
    index_url = "https://www.biquge9.com" + index
    section(name, index_url)
