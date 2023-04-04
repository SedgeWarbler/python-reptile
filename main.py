import json
import os.path
import re
import ffmpeg

import parsel
import requests


class bilibili:
    def __init__(self, keyword):
        self.dir = ''
        self.title = ''
        self.keyword = keyword
        self.keyword_url = 'https://search.bilibili.com/all?keyword=' + keyword
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Referer': 'https://www.bilibili.com'
        }

    def video_list(self):
        response = requests.get(self.keyword_url, headers=self.header)
        if response.status_code != 200:
            print("查询关键字失败")
            return

        selector = parsel.Selector(response.text)
        list_url = selector.css(
            "#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.video.i_wrapper.search-all-list > div > div > div > div.bili-video-card__wrap.__scale-wrap > a::attr(href)").getall()

        for url in list_url:
            self.video_details(url)

    def video_details(self, video_url):
        response = requests.get('https:' + video_url, headers=self.header)
        if response.status_code != 200:
            print("获取视频详情失败")
            return

        self.title = re.findall('<h1 title="(.*?)" class="video-title tit">', response.text)[0].replace(' ', '')
        details = re.findall('<script>window.__playinfo__=(.*?)</script>', response.text)
        js = json.loads(details[0])
        data = js['data']

        video_url = data['dash']['video'][0]['baseUrl']
        audio_url = data['dash']['audio'][0]['baseUrl']

        self.download(video_url, 'video')
        self.download(audio_url, 'audio')

        self.compound()

    def download(self, url, type):
        response = requests.get(url, headers=self.header)
        if response.status_code != 200:
            print("下载视频失败")
            return

        # 创建文件夹
        self.dir = self.keyword + "/" + self.title
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        if type == 'video':
            with open(self.dir + '/video.mp4', 'wb') as file:
                file.write(response.content)
        elif type == 'audio':
            with open(self.dir + '/audio.mp3', 'wb') as file:
                file.write(response.content)

    def compound(self):
        video_file = self.dir + '/video.mp4'
        audio_file = self.dir + '/audio.mp3'
        output_file = self.dir + '/output.mp4'

        # 设置视频和音频输入文件
        input_video = ffmpeg.input(video_file)
        input_audio = ffmpeg.input(audio_file)

        # 合并视频和音频流
        output = ffmpeg.output(input_video, input_audio, output_file)

        # 运行合成命令
        ffmpeg.run(output)


bilibili = bilibili("颜值")
bilibili.video_list()
