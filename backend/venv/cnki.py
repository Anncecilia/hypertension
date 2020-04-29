
#（代码补充说明：标注“参数设置”后面的代码中可以通过简单修改，就可以爬取不同主题，不同页数，使用不同的代理IP ）

#!/usr/bin/env python3

# -*- coding: utf-8 -*-

#-加载将会使用到的函数库

import requests                                     # 读取网页
import random                                       # 随机选择代理Ip
import string
import re
import pymongo
import time
import sys
import getopt
from lxml import etree                              # 用于解析网页
from bs4 import BeautifulSoup                       # 解析网页
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from requests import RequestException
from concurrent.futures import ThreadPoolExecutor
import multiprocessing


#--获得代理IP列表

def get_ip_list(urlip, headers2):
    web_data = requests.get(urlip, headers=headers2)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for k in range(1, len(ips)):
        ip_info = ips[k]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

#-从代理IP列表里面随机选择一个


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies



def get_html(url, headers):
    try:
        # response = requests.get(url, headers=headers, proxies=proxies)
        s = requests.session()
        s.keep_alive = False # 关闭多余连接
        response = s.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        else:
            print("requests.get error")
        return None
    except RequestException as e:
        print(e)
        return None
   
        
        
def save_p(paper):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    #指定数据库
    db = client.Literature
    #指定集合
    conference_col = db.Document
    
    # result = conference_col.insert_one(paper)
    
    # 插入数据，若存在完全相同的则不插入
    name = {
        'title': paper['title']
    }
    
    result = conference_col.update(
        name,
        {'$setOnInsert': paper},
        upsert = True
    )
    print (result)
    print("\n")
    return None


# 根据解析的页面，获取每一页的文章链接
def get_url_list(soup):
    # print(html)
    # print(soup)
    paper_url = soup.select('[class="name"] a[class="fz14"][target="_blank"]')
    # print(paper_url)
    url = []
    # 获取每一个文章链接
    for i in paper_url:
        attr = i.get("href").split("&")
        attr_dict = {}
        attr_dict["filename"] = ''
        attr_dict["dbcode"] = ''
        
        #链接处理，筛选除filename dbcode
        for msg in attr:
            
            if msg.startswith("FileName="):
                attr_dict["filename"] = msg.replace("FileName=","")
            elif msg.startswith("DbCode="):
                attr_dict["dbcode"] = msg.replace("DbCode=","")
            else:
                pass
          
        # print(attr_dict)
        if(attr_dict["filename"] and attr_dict["dbcode"]):
            # 合成所需链接
            true_url = "http://kns8.cnki.net/KCMS/detail/detail.aspx?dbcode=" + attr_dict["dbcode"] + "&filename=" + attr_dict["filename"]
            url.append(true_url)
        else:
            pass
        
        
    print(url)
    
    return url

   
def read_data(argv):
    # 参数设置
    keywords = ''   # 查询的主题
    start_num = ''
    num = ''
    
    #命令行参数
    try:
        opts, args = getopt.getopt(argv,"hk:s:n:",["keywords=","startpage=","num="])
        print(opts)
        # print(args)
    except getopt.GetoptError:
        print ('cnki.py -k <keywords> -s <startpage> -n <pagenum>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('cnki.py -k <keywords> -s <startpage> -n <pagenum>')
            sys.exit()
        elif opt in ("-k", "--keywords"):
            keywords = arg
        elif opt in ("-s", "--startpage"):
            start_num = arg
        elif opt in ("-n", "--num"):
            num = arg
        else:
            pass
            
    print(keywords)
    print(num)
    print(start_num)
    
    
    start_url = 'http://kns8.cnki.net/kns/DefaultResult/Index?dbcode=SCDB&kw=' + \
        keywords + '&korder=SU'
    now_url = start_url    
    lists = []
    page_urls = []
    
    
    print(start_url)
    
    browser = webdriver.Chrome()
    browser.get(now_url)

    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="fz14"]'))
    )
    source = browser.page_source
    soup = BeautifulSoup(source, 'lxml')        
    
    #获取每一页的文章链接 
    for i in range(int(start_num), int(start_num) + int(num)):
        print("i: " + str(i))        
        if soup:
            lists = get_url_list(soup)
        else:
            print("get url error!")
        
        for list in lists:
            page = list
            page_urls.append(page)
        # print(page_urls)
  
  
  
        #为解决，没有下一页
  
  
        next = browser.find_element_by_xpath("//*[@id='PageNext']")
        if(next):
            #next_url = next.click()
            source = ""
            soup = ""
            next_url = browser.execute_script("arguments[0].click();", next)
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="fz14"]'))
            )
            time.sleep(1)
            source = browser.page_source   
            soup = BeautifulSoup(source, 'lxml')
        else:
            print("翻页出错！")
            break
    # print(page_urls)
    return page_urls
    
    
def get_info(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        
    urlip = 'http://www.xicidaili.com/nt/'          # 提供代理IP的网站  
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }    
    # ip_list = get_ip_list(urlip, headers2)
    # proxies = get_random_ip(ip_list)
    
    # 每一篇文章的具体信息
    html = get_html(url, headers)
    #使用beautifulSoup进行解析
    soup = BeautifulSoup(html,'lxml') 
    #去除soup里面的标签
    [s.extract() for s in soup('sup')]
    
    # 标题
    title = soup.select('[class="wx-tit"] h1')[0].text
    # print(title)
    
    
    # 作者
    author = soup.select('[class="author"][id="authorpart"] span a')
    authors = ''
    for i in author:
        authors = authors + i.text + ';'
    # print(authors)
    
    
    # 作者单位
    author_unit = soup.select('h3 [class="author"][target="_blank"]')
    author_info = ''
    for i in author_unit:
        author_info = author_info + i.text + ';'
    # print(author_info)
    


    
    # 摘要
    abstract = soup.select('[class="abstract-text"]')[0].text
    # print(abstract)
    
    # #期刊
    # journal_info = soup.select('[class="top-tip"] span a')
    # journal = ''
    # for i in journal_info:
        # journal = journal + i.text.strip().replace("\t",'') + "-"
        # # print(i.text)
    # journal = journal.strip("-")
    # print(journal)
    
    
    #期刊
    journal_info = soup.select('[class="top-tip"] span')
    if(journal_info):
        journal = journal_info[0].text.replace(" ",'').replace("\n",'').replace("\r",'')
    else:
        journal = ''
    # print(journal)
    
    #关键词
    keyword = soup.select('[class="keywords"]') #返回列表 ^表示以什么开头 找到title=x，href=x，οnclick=x的节点
    keywords = ''
    for word in keyword:
        keywords = keywords + word.text.replace(" ",'').replace("\n",'').replace("\r",'') + ';'
    keywords = keywords.strip(";")   
    # print(keywords)
    
    # print("\n")

    #字典形式
    paper = {
        'title':title,
        'abstract':abstract,
        'keywords':keywords,
        'author':authors,
        'author_info':author_info,
        'journal':journal,
        'url':url,
        'src':"中国知识资源总库（CNKI）",
        'is_update':False,		
        'is_submit':False,
        'is_marked':False,
        'valid':True
    }
    # print(paper)
    return paper
    

if __name__ == '__main__':

    
    url_list = read_data(sys.argv[1:])
    for url in url_list:
        paper = get_info(url)
        save_p(paper)
        
    # pool = ThreadPoolExecutor(max_workers=5)
    # pool.map(get_info, url_list)
    # pool.shutdown()
    
    # p = multiprocessing.Process(target = get_info, args = (url_list,))
    # p.start()
    
