import os.path
import sys
import urllib.parse
import uuid

import requests

url = 'https://www.kuaishou.com/graphql'

header = {
    'Cookie': 'kpf=PC_WEB; clientid=3; did=web_e7963ff0a307caaccb57405d1009da7b; kpn=KUAISHOU_VISION',
    'Referer': 'https://www.kuaishou.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

keyword = input("请输入爬取的关键字：")
# 创建文件
dir = "快手/" + keyword + '/'
if not os.path.isdir(dir):
    os.makedirs(dir)

json = {
    "operationName": "visionSearchPhoto",
    "variables": {
        "keyword": keyword,
        "pcursor": "",
        "page": "search"
    },
    "query": "fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    searchSessionId\n    pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n"
}

print("爬取中")

for pcursor in range(5):
    json['variables']['pcursor'] = str(pcursor)
    response = requests.post(url, headers=header, json=json)
    if response.status_code != 200:
        continue

    data = response.json()

    if 'data' in data and 'visionSearchPhoto' in data['data'] and 'feeds' in data['data']['visionSearchPhoto']:
        feeds = data['data']['visionSearchPhoto']['feeds']
    else:
        print("爬取到的数据格式错误")
        sys.exit()

    # 获取视频
    for video in feeds:
        video_url = video['photo']['manifest']['adaptationSet'][0]['representation'][0]['url']
        video_result = requests.get(video_url)
        if video_result.status_code != 200:
            continue

        file_name_extension = os.path.splitext(urllib.parse.urlparse(video_url).path)[1]
        file_name = str(uuid.uuid4()) + '.' + file_name_extension

        with open(dir + file_name, 'wb') as file:
            file.write(video_result.content)

print("下载完成")
