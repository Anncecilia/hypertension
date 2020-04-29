# -*- coding: utf-8 -*-

import os
import re
import time
import sys
import getopt
import requests
from bs4 import BeautifulSoup
from requests import RequestException
import pymongo

# 添加User-Agent，放在headers中，伪装成浏览器
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

def get_html():
    start_rul = "http://discovery.imicams.ac.cn/primo_library/libweb/action/search.\
do?srt=date&srtChange=true&frbg=&&fn=search&indx=1&dscnt=0&scp.scps=primo_central_multiple_fe&tb\
=t&mode=Basic&vid=imicams&ct=search&srt=rank&tab=article_tab&dum=true&vl(freeText0)="

    # print(start_rul)
    
    # 参数设置
    # 查询的主题
    keys = ''   
    # 爬取的起始页
    start_page = ''
    # 要爬取的页数
    page_num = ''
    
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
            start_page = arg
        elif opt in ("-n", "--page_num"):
            page_num = arg
        else:
            pass
            
    print(keys)
    print(page_num)
    print(start_page)
        

    url = start_rul + keys 
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            
            #使用beautifulSoup进行解析
            soup = BeautifulSoup(response.text,'lxml')
            url_list = []
            base_url = "http://discovery.imicams.ac.cn/primo_library/libweb/action/"
            
            # 获取开始爬虫的第i页面
            if(int(start_page) > 1):
                for i in range(1,int(start_page)):
                    next_url = soup.select('[title="到下页"]')
                    print(next_url[0]['href'])
                    next_url = next_url[0]['href']
                    response = requests.get(next_url, headers=headers)  
                    soup = BeautifulSoup(response.text,'lxml')
            elif(int(start_page) == 1):
                pass
            else:
                print("start page ERROR")
                return None
                
            # 获取文献网址列表
            for i in range(int(start_page),int(start_page)+int(page_num)):
                #返回文献url列表
                lists = soup.select('[id^="exlidResult"][title^="查看记录详细信息"]') 
                for list in lists:
                    #keywords = keywords + word.text + ';'
                    url = base_url + list['href']
                    # print(url)
                    url_list.append(url)
                next_url = soup.select('[title="到下页"]') 
                # print(next_url[0]['href'])
                next_url = next_url[0]['href']
                response = requests.get(next_url, headers=headers)
                if response.status_code == 200:
                    response.encoding = 'utf-8'
                    soup = BeautifulSoup(response.text,'lxml')
                else:
                    print("response.status_code error")
                    return None
            
            return url_list
        return None
    except RequestException as e:
        print(e)
        return None
        
def get_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.text
    else:
        print("response.status_code error")
        return None
    
    
        
def get_info(page,url):
    soup = BeautifulSoup(page,'lxml')
    
    print("start\n")
    #题目
    title = soup.select('[class="EXLResultTitle"]')[0].text
    print(title)
    
    #关键词
    keyword = soup.select('[id="主题1"] [class="EXLLinkedField"]') #返回列表 ^表示以什么开头 找到title=x，href=x，οnclick=x的节点
    keywords = ''
    for word in keyword:
        word = word.text
        word = word.strip()
        keywords = keywords + word + ';'
    # print(keywords)
    
    #作者
    author = soup.select('[class="EXLResultAuthor"]')
    if(author):
        author = author[0].text
    else:
        author = ''
    # print(author)
    
    #journal
    journal = soup.select('[id="源自于1"]')
    if(journal):
        journal = journal[0].text
        journal = journal.replace("源自于:","")
        journal = journal.strip()
        pass
    else:
        journal = ''
    # print(journal)
    
    #摘要
    abstract = soup.select('[id="摘要1"]')
    if(abstract):
        abstract = abstract[0].text
        abstract = abstract.replace("摘要:","")
        abstract = abstract.strip()
        pass
    else:
        abstract = ''
    # print(abstract)
    
    
    # print("\n")
    
    
    #字典形式
    paper = {
        'title':title,
        'abstract':abstract,
        'keywords':keywords,
        'author':author,
        'journal':journal,
        'url':url,
        'src':"中国医学科学院医学信息研究所文献平台(UnionSearch)",
        'is_update':False,		
        'is_submit':False,
        'is_marked':False,
        'valid':True
    }
    # print(paper)
    return paper

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
    
    conference_col.update(
        name,
        {'$setOnInsert': paper},
        upsert = True
    )

if __name__ == '__main__':
    list = get_html()
    # print(list)
    # print(len(list))
    for i in list:
        page = get_page(i)
        if(page):
            info = get_info(page,i)
            save_p(info)
        else:
            print("get_page error")
        
    
    
       
