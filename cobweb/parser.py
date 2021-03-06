# 解析器
import types
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Parser:
    def __init__(self, func_parse_url=None, func_parse_content=None):
        self.html = None
        self.soup = None
        self.content = None
        self.urls = []
        self.base_url = None
        self.filter_str_dict = {
            'equal': ['/', '#', 'javascript:'],
            'contain': []
        }

        # 自定义url解析器
        if func_parse_url is not None:
            self.parse_url = types.MethodType(func_parse_url, self)
        # 自定义内容解析器
        if func_parse_content is not None:
            self.parse_content = types.MethodType(func_parse_content, self)

    # 解析内容
    def parse_content(self):
        self.content = self.soup.html
        return self

    # 解析 url
    def parse_url(self):
        node = self.soup.find_all('a')
        for n in node:
            url = n.get('href', '')
            if url:
                url = self.filter_url(url)
                if url:
                    self.urls.append(url)
        return self

    # 过滤url TODO 兼容性
    def filter_url(self, url):
        parse_url = urlparse(url)
        # 判断 scheme
        if parse_url.scheme and parse_url.scheme != self.base_url.scheme:
            return False
        # 判断 url 是否属于当前域名
        elif parse_url.netloc and parse_url.netloc not in self.base_url.netloc:
            return False

        if self.filter_str_dict['equal']:
            for str_ in self.filter_str_dict['equal']:
                if str_ == url:
                    return False

        if self.filter_str_dict['contain']:
            for str_ in self.filter_str_dict['contain']:
                if str_ in url:
                    return False

        if not parse_url.netloc:
            url = 'http://' + self.base_url.netloc + url
        return url

    def set_html(self, html):
        self.html = html
        self.soup = BeautifulSoup(self.html, 'html.parser', from_encoding='utf8')
        return self

    def set_base_url(self, base_url):
        self.base_url = urlparse(base_url)

    def add_filter_str(self, filter_str):
        self.filter_str_dict['equal'] += filter_str['equal']
        self.filter_str_dict['contain'] += filter_str['contain']

    def get_content(self):
        return self.content

    def get_url(self):
        return self.urls
