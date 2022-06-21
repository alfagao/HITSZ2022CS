"""
2022-04-01: 将Crawler整合, 提供一些接口
    文章发布首页 --> 各页文章url(存储) --> 文章内容(存储)
"""
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from sz.SZfilter import page_content_fill, soup_filter_next, soup_filter_page
# 深圳市疫情信息发布页--第一页，起始页
sz_pageListStart = "http://www.sz.gov.cn/szzt2010/yqfk2020/qktb/index.html"
user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 '
    'Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 '
    'Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 '
    'Safari/537.36 Edge/16.16299',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; "
    ".NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR "
    "2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR "
    "3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; "
    ".NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR "
    "3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 ("
    "Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 "
    "Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

class Crawler:
    def __init__(self, page_url):
        self.page_url = page_url   # 当前页面url
        self.soup = BeautifulSoup('')   # 当前页面对应的BeautifulSoup对象
        self.data = []      # 存放爬取结果, 应当是一个字典列表

    # 请求网页资源, 并把网页转为BeautifulSoup对象存储在
    def __parse_html(self):
        ua = random.choice(user_agent_list)
        header = {'User-Agent': ua,
                  'Connection': 'close'}
        res = requests.get(self.page_url, headers=header, verify=True)  # 获取网页
        res.encoding = res.apparent_encoding  # 解码资源
        self.soup = BeautifulSoup(res.text, 'lxml')

    # soup对象获取url, 依据soup_filter将soup范围缩小
    # 再在小范围内寻找所有a标签里的href, 返回目标url队列
    def __get_passage_url(self, soup_filter_page):
        small_soup = soup_filter_page(self.soup)
        all_href = small_soup.find_all('a')
        return [href['href'] for href in all_href]

    # 更新当前页面url
    def __update_page(self, soup_filter_next):
        # 更新当前页面url
        next_url = soup_filter_next(self.soup)
        if next_url is None:
            return False
        else:
            self.page_url = next_url
            return True

    # 将data[{}, {}, ...]写入csv, path为相对路径
    def __write_to_csv(self, path):
        pd.DataFrame(self.data).to_csv(path, index=False)

    # 爬取 文章列表发布页，获取每页的文章url, 自动翻页, 将所有的文章url放入data并写入文件
    def get_all_passage_links(self, soup_filter_page, soup_filter_next, path):
        cnt = 1
        flag = True
        while flag:
            pid = str(cnt).zfill(3)
            self.__parse_html()
            page_data = self.__get_passage_url(soup_filter_page)
            self.data += [{"pid": pid, "url": url} for url in page_data]
            flag = self.__update_page(soup_filter_next)
            print(cnt, " pages have got!")
            cnt += 1
        self.__write_to_csv(path)

    # data存放着所有文章url，现在要依据url获取每篇文章内容
    # passage_id, publish_date, title, content
    def get_passage(self, passage_filter, path):
        n = len(self.data)
        for i in range(n):
            self.page_url = self.data[i]['url']
            self.__parse_html()
            self.data[i] = passage_filter(self.soup)
            print(i+1, "passages successfully got!")
        self.__write_to_csv(path)

# 爬取原始疫情发布文章并存储
def crawl_details():
    sz_crawler = Crawler(sz_pageListStart)
    sz_crawler.get_all_passage_links(soup_filter_page, soup_filter_next, "./passage/passage_urls.csv")
    sz_crawler.get_passage(page_content_fill, "./passage/szDiseaseDetails.csv")
