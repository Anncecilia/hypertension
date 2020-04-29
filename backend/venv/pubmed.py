# -*- coding: utf-8 -*-
 
"""
@Datetime: 2020/3/29

"""
import os
import re
import time
import sys
import getopt
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
 
import pandas as pd
import requests
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import pymongo
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
 
BASE_DIR = 'html'
 
if not os.path.exists(BASE_DIR):
    os.mkdir(BASE_DIR)
 
 
class PubMed(object):
    def __init__(self, url):
        self.url = url
        # self.url = 'https://www.ncbi.nlm.nih.gov/pubmed/{}'.format(id)
        self.retry = 0
 
    def download(self):
        try:
            # response = requests.get(self.url, headers=headers)
            response = requests.get(self.url, headers=headers)
            if response.status_code == 200:
                self.parse(response.content)
        except Exception as e:
            traceback.print_exc()
            print('error:')
            print(self.url)
            while True:
                self.retry += 1
                if self.retry < 5:
                    try:
                        response = requests.get(self.url, headers=headers)
                        if response.status_code == 200:
                            self.parse(response.content)
                            return
                    except Exception as e:
                        print(e)
                        time.sleep(10)
                else:
                    print('下载失败')
                    print(self.url)
                    return
 
    def parse(self, response):
        doc = pq(response, parser='html')
        periodical_item = doc('.cit')
        periodical = periodical_item.children().text()
        try:
            periodical_datetime = re.search('</a>(.*?);', periodical_item.__str__()).group(1)
        except AttributeError:
            periodical_datetime = re.search('</a>(.*?).', periodical_item.__str__()).group(1)
        title = doc('.rprt_all h1').text()
        authors_items = doc('.auths a').items()
        authors = ','.join(list(map(lambda x: x.text(), authors_items)))
        author_info = doc('.ui-ncbi-toggler-slave dd').text()
        keywords = doc('.keywords p').text()
        abstract = doc('.abstr').text()
        data_dict = {
            'title': title, 
            'abstract': abstract,
            'keywords':keywords,
            'author': authors, 
            'author_info': author_info,
            'journal': periodical, 
            'date': periodical_datetime,
            'src':"美国生物医学文献数据库（PubMed）",
            'url': self.url,
            'is_update':False,		
            'is_submit':False,
            'is_marked':False,
            'valid':True
        }
        self.write_mongo(data_dict)
        print(self.url + '下载完成')
 
    @staticmethod
    def write_csv(filename, data=None, columns=None, header=False):
        """ 写入 """
        if header:
            df = pd.DataFrame(columns=columns)
            df.to_csv(filename, index=False, mode='w')
        else:
            df = pd.DataFrame(data=data)
            df.to_csv(filename, index=False, header=False, mode='a+')
    
    @staticmethod
    def write_mongo(paper):
        client = pymongo.MongoClient('mongodb://localhost:27017')
        #指定数据库
        db = client.Literature
        #指定集合
        collection = db.Document
        
        # result = collection.insert_one(paper)
        
        # 插入数据，若存在完全相同的则不插入
        name = {
            'title': paper['title']
        }
        
        collection.update(
            name,
            {'$setOnInsert': paper},
            upsert = True
        )
 
def filter_url_list(urls_list):
    df = pd.read_csv('pubmed_result.csv')
    has_urls = df.url.tolist()
    url_list = set(urls_list) - set(has_urls)
    print('共：{} 完成：{} 还剩：{}'.format(len(urls_list), len(has_urls), len(url_list)))
    return list(url_list)

def get_url_list(soup):
    # print(html)
    paper_url = soup.select('[class="rslt"] [class="title"] a')
    url = []
    for i in paper_url:
        url.append(i.get("href"))
    # print(url)
    
    
    return url
    
 
def read_data():
    # 设置
    base_url = "https://www.ncbi.nlm.nih.gov/pubmed/?term="
    page_url = "https://www.ncbi.nlm.nih.gov"

    lists = []
    page_urls = []
    
    
    # 参数设置
    # 查询的主题
    keys = ''   
    # 爬取的起始页
    start_num = ''
    # 要爬取的页数
    num = ''
    
    #命令行参数
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hk:s:n:",["key_word=","startpage=","page_num="])
        print(opts)
        # print(args)
    except getopt.GetoptError:
        print ('union.py -k <keywords> -s <startpage> -n <pagenum>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('union.py -k <keywords> -s <startpage> -n <pagenum>')
            sys.exit()
        elif opt in ("-k", "--key_word"):
            keys = arg
        elif opt in ("-s", "--startpage"):
            start_num = arg
        elif opt in ("-n", "--page_num"):
            num = arg
        else:
            pass
            
    print(keys)
    print(num)
    print(start_num)
    
    start_url = base_url + keys
    
    browser = webdriver.Chrome()
  
    now_url = start_url
    
    browser.get(now_url)
    # browser.implicitly_wait(10)
    print("a")
    element = WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="rslt"]'))
    )
    
    print("b")
     
    for i in range(int(start_num), int(start_num) + int(num)):
        print("c")
        print("i: " + str(i))
        source = browser.page_source   
        soup = BeautifulSoup(source, "html.parser")
        if soup:
            print("in soup")
            lists = get_url_list(soup)
        else:
            print("get url error!")
        
        for list in lists:
            page = page_url + list
            page_urls.append(page)
            
        next = browser.find_element_by_xpath("//a[@class='active page_link next']")
        if(next):
            next_url = next.click()
        else:
            print("翻页出错！")
            break
            
    
        
    print(page_urls)
    return page_urls
 
 
def main(url):
    """ 主函数 """
    # print("main")
    
    # for i in url:
        # pubmed = PubMed(url=i)
        # pubmed.download()
        
    pubmed = PubMed(url=url)
    pubmed.download()
 
 
if __name__ == '__main__':
    
    # if not os.path.exists('pubmed_result.csv'):
        # columns = ['url', 'periodical', 'periodical_datetime', 'title', 'authors', 'author_info', 'keywords','abstract']
        # PubMed.write_csv(filename='pubmed_result.csv', columns=columns, header=True)
    # else:
        # url_list = filter_url_list(url_list)
    print("start")
    url_list = read_data()
    # main()
    pool = ThreadPoolExecutor()
    pool.map(main, url_list)
    pool.shutdown()
 
    # # 写入excel
    # df = pd.read_csv('pubmed_result.csv')
    # writer = pd.ExcelWriter('pubmed_result.xlsx')
    # df.to_excel(writer, 'table', index=False)
    # writer.save()