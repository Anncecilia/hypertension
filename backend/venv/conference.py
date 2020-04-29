import os
import re
 
import requests
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
    keyword = soup.select('[title="知识脉络分析"][href="#"][onclick^="wfAnalysis"]') #返回列表 ^表示以什么开头 找到title=x，href=x，οnclick=x的节点
    keywords = ''
    for word in keyword:
        keywords = keywords + word.text + ';'
 
    #作者
    author = soup.select('[onclick^="authorHome"]')
    if author:
        author = author[0].text
    else:
        author = ''
 
    #作者单位
    unit = soup.select('[class^="unit_nameType"]')
    if unit:
        unit = unit[0].text
    else:
        unit = ''
 
    #母体文献
    pattern = re.compile('母体文献.*?<div class="info_right author">(.*?)</div>',re.S)
    literature = re.findall(pattern, html)
    if literature:
        literature = literature[0]
    else:
        literature = ''
    # print(literature)
 
    #会议名称
    conference = soup.select('[href="#"][onclick^="searchResult"]')[0].text
    print(conference)
 
    #会议时间
    pattern = re.compile('会议时间.*?<div class="info_right">(.*?)</div>', re.S)
    date = pattern.findall(html)
    if date:
        date = date[0].strip()
    else:
        date = ''
 
    # 会议地点
    pattern = re.compile('会议地点.*?<div class="info_right author">(.*?)</div>', re.S)
    address = re.findall(pattern, html)
    if address:
        address = address[0].strip()
    else:
        address = ''
    # print(address)
 
    # 主办单位
    organizer = soup.select('[href="javascript:void(0)"][onclick^="searchResult"]')
    if organizer:
        organizer = organizer[0].text
    else:
        organizer = ''
    # print(organizer)
 
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
        'author':author,
        'author_unit':unit,
        'type':"会议论文",
        'literature':literature,
        'conference':conference,
        'date':date,
        'address':address,
        'organizer':organizer,
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