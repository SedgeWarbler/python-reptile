import os
import requests
from urllib.parse import urlparse

class reptileKuwo:
    """
    爬取酷我
    """
    search_music_api = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key='

    play_url_api = 'http://www.kuwo.cn/api/v1/www/music/playUrl?mid='

    def __init__(self, key):
        self.music_name = None
        self.key = key
        self.search_music_api = self.search_music_api + self.key

    def searchMusicBykeyWord(self):
        """
        搜索应用关键字，获取音乐列表
        :return:
        """
        header = {
            'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1680241151; _ga=GA1.2.810277490.1680241151; _gid=GA1.2.1296653774.1680241151; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1680242698; _gat=1; kw_token=FMSL5TGQIG',
            'csrf': 'FMSL5TGQIG',
            'Host': 'www.kuwo.cn',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.kuwo.cn/search/list',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        response = requests.get(self.search_music_api, headers=header)
        if response.status_code != 200:
            print("爬取列表失败,状态：" + str(response.status_code))
            return

        result = response.json()
        if result['code'] != 200:
            print("获取列表失败")
            return

        data = result['data']['list']
        for value in data:
            self.music_name = value['name']
            rid = value['rid']
            self.playUrl(rid)

    def playUrl(self, mid):
        """
        获取音乐播放链接
        :return:
        """
        play_url_api = self.play_url_api + str(mid)

        header = {
            'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1680241151; _ga=GA1.2.810277490.1680241151; _gid=GA1.2.1296653774.1680241151; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1680243621; kw_token=EBCGF64LPHN',
            'Host': 'www.kuwo.cn',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }

        response = requests.get(play_url_api, headers=header)
        if response.status_code != 200:
            print("获取" + self.music_name + "播放链接失败")
            return

        result = response.json()
        if result['code'] == -1:
            print(self.music_name + ':' + result['msg'])
            return

        self.downloadMusic(result['data']['url'])

    def downloadMusic(self, url):
        """
        爬取酷我音乐
        :return:
        """
        # 解析url以及参数
        parsed_url = urlparse(url)
        # 获取后缀
        filename, extension = os.path.splitext(parsed_url.path)
        response = requests.get(url)

        # 创建文件然后下载音乐
        if not os.path.isdir(self.key):
            os.mkdir(self.key)
            os.chmod(self.key, 0o777)

        with open(self.key + '/' + self.music_name + extension, 'wb') as f:
            f.write(response.content)
        print("下载完成：" + self.key + '/' + self.music_name + extension)


key = input("输入你要爬取的关键字：")

kuwo = reptileKuwo(key)
kuwo.searchMusicBykeyWord()
