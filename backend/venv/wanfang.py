import re
import time
 
import requests
from requests import RequestException

import conference
import perio
import sys
import getopt
 
def get_page(url):
    try:
        # 添加User-Agent，放在headers中，伪装成浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        return None
    except RequestException as e:
        print(e)
        return None
 
def get_url(html,type):
    url_list = []
    pattern = re.compile("this.id,'(.*?)'",re.S)
    ids = pattern.findall(html)
 
    for id in ids:
        if type == 'c':
            url_list.append('http://www.wanfangdata.com.cn/details/detail.do?_type=conference&id='+id)
        # elif type == 'd':
            # url_list.append('http://www.wanfangdata.com.cn/details/detail.do?_type=degree&id=' + id)
        else:
            url_list.append('http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id=' + id)
 
    return url_list
 
def get_info(url,type):
    if type == 'c':
        # print("C")
        conference.main(url)
    else:
        perio.main(url)
 
if __name__ == '__main__':
    # 参数设置
    # 查询的主题
    key_word = ''   
    # 爬取的起始页
    start_page = ''
    # 要爬取的页数
    page_num = ''
    # type = input('请选择论文类型(p:期刊 c:会议)：')
    type = ''
    
    #命令行参数
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hk:s:n:t:",["key_word=","startpage=","page_num=","type="])
        print(opts)
        # print(args)
    except getopt.GetoptError:
        print ('wanfang.py -k <keywords> -s <startpage> -n <pagenum> -t <type>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('wanfang.py -k <keywords> -s <startpage> -n <pagenum> -t <type>')
            sys.exit()
        elif opt in ("-k", "--key_word"):
            key_word = arg
        elif opt in ("-s", "--startpage"):
            start_page = arg
        elif opt in ("-n", "--page_num"):
            page_num = arg
        elif opt in ("-t", "--type"):
            type = arg
        else:
            pass
            
    print(key_word)
    print(page_num)
    print(start_page)
    print(type)
 
    if type == 'c':
        base_url = 'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=conference&pageSize=20&page={}&searchWord={}&showType=detail&order=pro_pub_date&isHit=&isHitUnit=&firstAuthor=false&navSearchType=conference&rangeParame='
    # elif type == 'd':
        # base_url = 'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=degree&pageSize=20&page={}&searchWord={}&showType=detail&order=orig_pub_date&isHit=&isHitUnit=&firstAuthor=false&navSearchType=degree&rangeParame='
    else:
        base_url = 'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=perio&pageSize=20&page={}&searchWord={}&showType=detail&order=common_sort_time&isHit=&isHitUnit=&firstAuthor=false&navSearchType=perio&rangeParame='
        pass
        
    # print(base_url)
    
    for page in range(int(start_page),int(start_page)+int(page_num)):
        new_url = base_url.format(page,key_word)
        print(new_url)
        #爬取当前页面 发送请求、获取响应
        html = get_page(new_url)
        #解析响应 提取当前页面所有论文的url
        url_list = get_url(html,type)
        for url in url_list:
            #获取每篇论文的详细信息
            get_info(url,type)
            time.sleep(1) #间隔1s