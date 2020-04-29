import os
import re
 
import requests
# import xlrd
# import xlutils.copy
# import xlwt
from bs4 import BeautifulSoup
from requests import RequestException
import pymongo
 
def get_html(url):
    try:
        # 添加User-Agent，放在headers中，伪装成浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        return None
    except RequestException as e:
        print(e)
        return None
 
def parse_html(html,url):
    #使用beautifulSoup进行解析
    soup = BeautifulSoup(html,'lxml')
    #题目
    title = soup.select('[style="font-weight:bold;"]')[0].text
    #摘要
    abstract = soup.select('.abstract')[0].textarea
    if abstract:
        abstract = abstract.text.strip()
    else:
        abstract=''
 
    #关键词
    keyword = soup.select('[title="知识脉络分析"][href="javascript:void(0)"][onclick^="wfAnalysis"]') #返回列表 ^表示以什么开头 找到title=x，href=x，οnclick=x的节点
    keywords = ''
    for word in keyword:
        keywords = keywords + word.text + ';'
 
    # 作者
    author = soup.select('[class="info_right_name"][onclick^="authorHomeWfAnalysis"]')
    authors = ''
    for i in author:
        authors = authors + i.text + ';'
        
 
    # #作者单位
    # unit = soup.select('[title="知识脉络分析"][class^="author"]')
    # if unit:
        # # unit = unit[0].text
        # units = ''
        # for i in unit:
            # units = units + i.text + ';'
    # else:
        # unit = ''

 
    #期刊名称
    journal = soup.select('[href="#"][onclick^="navigaPerio"]')[0].text
    print(journal)
 
 
    # Journal，english
    # pattern = re.compile('Journal.*?<div class="info_right author">(.*?)</div>', re.S)
    journal_e = soup.select('[onclick^="toJournal"]')
    if journal_e:
        journal_e = journal_e[0].text
    else:
        journal_e = ''
    # print(address)
 
    # 在线发表时间
    pattern = re.compile('在线出版日期.*?<div class="info_right author">(.*?)</div>', re.S)
    online_date = pattern.findall(html)
    if online_date:
        online_date = online_date[0].strip()
        online_date = online_date.replace("<span>", "").replace("</span>", "")
    else:
        online_date = ""
 
    #字典形式
    paper = {
        'title':title,
        'abstract':abstract,
        'keywords':keywords,
        'author':authors,
        # 'author_unit':units,
        'type':"期刊论文",
        'journal':journal,
        'journal_english':journal_e,
        'online_date':online_date,
        'url':url,
        'src':"万方数据知识服务平台",
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
        
    # print(result)
    # print(result.inserted_id)
 
 
def main(url):
    #发送请求、获取响应
    html = get_html(url)
    #解析响应
    paper = parse_html(html, url)
    #数据存储
    save_p(paper)