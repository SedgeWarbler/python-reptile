import requests
import parsel

url = "https://www.bqg789.net/296/296486/99558365.html"
# 发送get请求
response = requests.get(url)
response.encoding = response.apparent_encoding
# print(response.text)

"""
解析数据
    css xpath re(正则)

什么时候使用css和xpath :没有办法直接对字符串数据进行提取
    当得到的数据，有标签的时候
    
re 当你没有办法使用标签提取数据的时候使用正则
"""

selector = parsel.Selector(response.text)  # 将text字符串数据转成可解析的对象

# 提取h1标签里面的文本内容 ::text   get()获取得道结果
# title = selector.css("#info > h1::text").get()  # 直接浏览器复制 selector
title = selector.xpath('//*[@id="info"]/h1/text()').get()  # content 下面的wap_none 里面的text内容

# 内容很多需要获取全部，getall
content_list = selector.css("#chaptercontent::text").getall()
content = "\n".join(content_list)  # 列表转字符串
print(content)

# 保存到文件
with open(title + ".txt", mode="w") as f:
    f.write(title)
    f.write('\n')
    f.write(content)
