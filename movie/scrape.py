import requests, bs4
import re

# 基本URL
URL_HEAD = 'http://sample.babyblue1000.com/main_files/movie/'
URL_EXTENSION = '.htm'

class ResponseMovieSite(object):
    file_name = None
    actor_name = None
    title = None

    def __init__(self,file_name):
        self.file_name = file_name

        # ファイル名からURL用ページを推測
        url = self._get_page(self.file_name)
        print(url)

        # ページの情報を取得
        res = requests.get(url)
        res.encoding = res.apparent_encoding

        # WEBページを解析
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        # 主演テキストを抽出
        self.actor_name = self._get_actor_name(soup);
        # タイトルテキストを抽出
        self.title = self._get_title(soup);

    def info(self):
        return {
            'title' : self.title,
            'actor_name' : self.actor_name,
        }

    # ファイル名からURLを成形
    def _get_page(self,file_name):
        url_page_name = ''
        DL_PATTERN = r'(\d{4})[_](\d{1})([.mp4])'

        if file_name.startswith('take'):
            # takeXXXXパターン
            url_page_name = file_name.replace('take','')[0:4] + URL_EXTENSION

        elif re.match(DL_PATTERN,file_name) is not None:
            url_page_name = file_name[0:4] + URL_EXTENSION
            print(url_page_name)
        return URL_HEAD + url_page_name

    def _get_actor_name(self,soup):
        # 主演欄を抽出
        search = re.compile('.*主演.*')
        actor_text = soup.find_all(text=search)[0]
        # 女優名だけを取得
        actor_name = actor_text.split(':')[1]
        return actor_name
    
    def _get_title(self,soup):
        # タイトル欄を抽出
        search = re.compile('.*タイトル.*')
        title_text = soup.find_all(text=search)[0]
        # 女優名だけを取得
        title = title_text.split(':')[1]
        return title
    
