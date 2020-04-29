import string
import json
import re
import os
from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
from flask import request
from flask_cors import CORS
from py2neo import Graph,Node,Relationship,NodeMatcher 
from bson import json_util
from goto import with_goto
from bson.objectid import ObjectId
from multiprocessing import Process
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

app = Flask(__name__,
# static_folder = "D:/xxx/CODE/hypertension/frontend/dist/static",
# template_folder = "D:/xxx/CODE/hypertension/frontend/dist"
)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['DEBUG'] = True  # 开启 debug

mongo = PyMongo(app, uri="mongodb://localhost:27017/Literature")  # 开启数据库实例

# BackgroundScheduler: 适合于要求任何在程序后台运行的情况，当希望调度器在应用后台执行时使用。
scheduler = BackgroundScheduler()	
 
##连接neo4j数据库，输入地址、用户名、密码
# graph = Graph('http://localhost:7474',username='neo4j',password='13579zxc2468')
# graph.delete_all()
    
    

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
       

@app.route('/mongo/query')	
def QueryUser():		
    data = request.args
    data = data.to_dict()
    print(data)
    if(data['table'] == "disease" and data['msg']):
        # 查询语句
        condition = {}
        filter = {}
        condition['$regex'] = data['msg']
        filter["name"] = condition

        res = mongo.db.disease.find(filter)	
        len_res = res.count()
        if(len_res):
            dict2 = []
            id = 1
            for i in res:
                dict1 = {}
                dict1["name"] = i['name']
                dict1["chapter_or_code"] = i['chapter_or_code']
                dict1["valid"] = i['valid']
                dict2.append(dict1)
                id = id + 1
            print(dict2)
            result = {
                'msg': "查询成功!",
                'code': 200,
                'data': dict2
            }
            print("查询成功!")
            result_json = jsonify(result)
        else:
            result = {
                'msg': "查询为空!",
                'code': 400,
                'data': ""
            }
            print("查询为空!")
            result_json = jsonify(result)
    elif(not data['msg']):
        res = mongo.db.disease.find().limit(10)
        print (res)
        print (type(res))
        if(res):
            dict2 = []
            id = 1
            for i in res:
                dict1 = {}
                dict1["name"] = i['name']
                dict1["chapter_or_code"] = i['chapter_or_code']
                dict1["valid"] = i['valid']
                dict2.append(dict1)
                id = id + 1
            print(dict2)
            print("查询成功!")
            result = {
                'msg': "查询成功!",
                'code': 200,
                'data': dict2
            }
            result_json = jsonify(result)
        else: 
            result = {
                'msg': "查询为空!",
                'code': 400,
                'data': ""
            }  
            print("查询为空!")
            result_json = jsonify(result)
    else:
        print("ERROR!")
        result = {
            'msg': "ERROR!",
            'code': 400,
            'data': ""
        }
        result_json = jsonify(result)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    return result_json

def test(datas):
    dict2 = {}
    id = 1
    for data in datas:
        dict1 = {}
        #print(data)
        #print(type(data))
        print(data['r'])
        relation = str(data['r'])
        a = relation.split('->')
        a[1] = a[1].replace('(', '')
        a[1] = a[1].replace(')', '')
        end_node = a[1]
        b = a[0].split('-')
        b[0] = b[0].replace('(', '')
        b[0] = b[0].replace(')', '')
        start_node = b[0]
        b[1] = b[1].replace('[:', '')
        b[1] = b[1].replace(']', '')
        relation = b[1]
        print(start_node)
        print()
        print(relation)
        #dict1["id"] = id
        dict1["start_node"] = start_node
        dict1["end_node"] = end_node
        dict1["relation"] = relation
        dict2[id] = dict1
        id = id + 1
    
    print (dict2)
    return dict2
        
        
        
        #dict['r'] = 
        #print(type(data['r']))
        
def print_object(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

@app.route('/test')
def test1():
    data = request.args
    data = data.to_dict()
    print("1")
    print(data)  
    return render_template('index.html')
        
@app.route('/graph/create')
def neo4j_graph_create():        
    # 创建结点
    test_node_1 = Node('ru_yi_zhuan', name='皇帝') # 修改的部分
    test_node_2 = Node('ru_yi_zhuan', name='皇后') # 修改的部分
    test_node_3 = Node('ru_yi_zhuan', name='公主') # 修改的部分
    graph.create(test_node_1)
    graph.create(test_node_2)
    graph.create(test_node_3)

    ##创建关系
    #分别建立了test_node_1指向test_node_2和test_node_2指向test_node_1两条关系，关系的类型为"丈夫、妻子"，两条关系都有属性count，且值为1。
    node_1_zhangfu_node_1 = Relationship(test_node_1,'丈夫',test_node_2)
    node_1_zhangfu_node_1['count'] = 1
    node_2_qizi_node_1 = Relationship(test_node_2,'妻子',test_node_1)
    node_2_munv_node_1 = Relationship(test_node_2,'母女',test_node_3)
     
    node_2_qizi_node_1['count'] = 1
     
    graph.create(node_1_zhangfu_node_1)
    graph.create(node_2_qizi_node_1)
    graph.create(node_2_munv_node_1)
     
    print(graph)
    print(test_node_1)
    print(test_node_2)
    print(node_1_zhangfu_node_1)
    print(node_2_qizi_node_1)
    print(node_2_munv_node_1)
    
    #matcher = NodeMatcher(graph) 
    #nodes = matcher.match("ru_yi_zhuan")
    #new_nodes = list(nodes)
    #print(new_nodes)
    
    results = graph.run("MATCH ()-[r]->() RETURN r").data()
    # print(results)
    # results = list(results)
    # print(type(results))
    
    res = test(results)
    
    
    # for rel in graph.match(r_type="丈夫"):
        # print(rel.start_node["name"])
        # print(rel.end_node["name"])
    
    # new_links = get_links(results)
    # print(new_links)
    
    #result_json = json.dumps(results, ensure_ascii=False)
    result_json = jsonify(res)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    print(result_json)
    # print(type(result_json))
    
    data = request.args
    data = data.to_dict()
    print(data)
    
    return result_json
    
@app.route('/graph/query')  
def neo4j_graph_query():    
    matcher = NodeMatcher(graph) 
    nodes = matcher.match("ru_yi_zhuan")
    new_nodes = list(nodes)
    print(new_nodes)
    return render_template('index.html')
    
    
@app.route('/user/login')  
def Login():
    data = request.args
    data = data.to_dict()
    flag = 0 #判断用户名、手机号是否为空
    print(data)
    if(data["name"]):
        res = mongo.db.User.find_one({'name': data['name'],'password':data['password']})	
        # print(res)
        flag = 1 # 用户名不为空
    elif(data["phone"]):
        res = mongo.db.User.find_one({'phone': data['phone'],'password':data['password']})	
        flag = 1 # 手机号不为空
    else:
        pass
        
    # 查询到结果，登录成功
    if(res and flag):
        dict1 = {}
        dict1["id"] = str(res['_id'])
        dict1["name"] = res['name']
        dict1["password"] = res['password']
        dict1["phone"] = res['phone']
        print(dict1)
        res = {
            "msg": "登陆成功",
            "code": 200,
            "data": dict1
        }
    # res为none，密码错误，导致查找失败
    elif(flag):
        res = {
            "msg": "密码错误",
            "code": 400,
            "data": ""
        }
    else:
        res = {
            "msg": "用户名或手机号为空",
            "code": 400,
            "data": ""
        }
   
    result_json = jsonify(res)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    
    return result_json
    
    
@app.route('/user/register')  
def Register():
    data = request.args
    data = data.to_dict()
    print(data)
    # 判断是否有该用户
    if(mongo.db.User.find_one({'name': data['name']})):
        result = {
            "msg": "用户名已存在",
            "code": 400,
            "data": ""
        }
        print("用户名已存在")
    elif(mongo.db.User.find_one({'phone': data['phone']})):
        result = {
            "msg": "手机号已存在",
            "code": 400,
            "data": ""
        }
        print("手机号已存在")
    else:
        # 插入数据
        res = mongo.db.User.insert_one(data)
        # print(res)
        # print(res.inserted_id)
        id = json_util.dumps(res.inserted_id)
        print(type(id))
        id = json.loads(id)
        response = {
            "id": id["$oid"]
        }
        result = {
            "msg": "成功",
            "code": 200,
            "data": response
        }
   
    result_json = jsonify(result)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    
    return result_json


def RunSpider(src_c, key_c, src_e, key_e, page_num, start_page,):
    # 选择了wanfang
    if('1' in src_c):
        keywords_wf = ''
        for i in key_c:
            keywords_wf = keywords_wf + i + "+"
        keywords_wf = keywords_wf.strip("+")
        # cmd_c = "python wanfang.py -k " + keywords_wf + " -n " + page_num + " -s " + start_page + " -t c"
        # print(cmd_c )
        # os.system(cmd_c )
        cmd_p = "python wanfang.py -k " + keywords_wf + " -n " + page_num + " -s " + start_page + " -t p"
        print(cmd_p )
        os.system(cmd_p )
    # 选择了cnki
    if('2' in src_c):
        keywords_cnki = ''
        for i in key_c:
            keywords_cnki = keywords_cnki + i + "%20"
        keywords_cnki = keywords_cnki.strip("%20")
        cmd = "python cnki.py -k " + keywords_cnki + " -n " + page_num + " -s " + start_page
        print(cmd)
        os.system(cmd)
    if('3' in src_c):
        key_union = ''
        for i in key_c:
            key_union = key_union + i + "+"
        key_union = key_union.strip("+")
        cmd = "python union.py -k " + key_union + " -n " + page_num + " -s " + start_page
        print(cmd)
        os.system(cmd)
    if('1' in src_e):
        key_pub = ''
        for i in key_e:
            key_pub = key_pub + i + "+"
        key_pub = key_pub.strip("+")
        cmd = "python pubmed.py -k " + key_pub + " -n " + page_num + " -s " + start_page
        print(cmd)
        os.system(cmd)


@app.route('/set/spider')  
def SetSpider():
    data = request.args
    data = data.to_dict()
    # print(data)
    # print("src_c")
    # print(data["src_c"])
    # print("src_e")
    # print(data["src_e"])
    # print("key_c")
    # print(data["key_c"])
    # print("key_e")
    # print(data["key_e"])
    # print("time")
    # print(data["time"])
    # print("circle")
    # print(data["circle"])
    # print("start_page")
    # print(data["start_page"])
    # print("page_num")
    # print(data["page_num"])
    # print("spider_switch")
    # print(data["spider_switch"])
    
    
    # os.system("python wanfang.py")  
    
    src_c = json.loads(data["src_c"])
    src_e = json.loads(data["src_e"])
    key_c = json.loads(data["key_c"])
    key_e = json.loads(data["key_e"])
    time = data["time"]
    circle = data["circle"]
    start_page = data["start_page"]
    page_num = data["page_num"]
    spider_switch = data["spider_switch"]
    print(src_c)
    print(src_e)
    
    
    msg = ''
    
    
    
    # print(type(src_c))
    # print(len(src_c) or len(src_e))
    
    # 爬虫开关
    if(spider_switch == "false"):
        res = {
            "msg":  "爬虫关闭",
            "code": 200,
            "data": ""
        }
    else:
        # 没有设置任何文献源
        if(not (len(src_c) or len(src_e))):
            print("请选择文献源")
            msg = "请选择文献源"
        else:
            # 查询中文文献却没设置任何关键词
            if(len(src_c) and ((not key_c) and (not key_e))):
                if(msg):
                    msg = msg + ",请输入中/英文关键词"
                else:
                    msg = "请输入中/英文关键词"
            else:
                pass
            # 查询外文文献却没设置英文关键词
            if(len(src_e) and (not key_e)):
                if(msg):
                    msg = msg + ",请输入英文关键词"
                else:
                    msg = "请输入英文关键词"
            else:
                pass
            # 没设置时间
            if(not time):
                if(msg):
                    msg = msg + ",请设置爬虫运行时间"
                else:
                    msg = "请设置爬虫运行时间"
            else:
                pass
            # 没设置周期
            if(not circle):
                if(msg):
                    msg = msg + ",请设置爬虫运行周期"
                else:
                    msg = "请设置爬虫运行周期"
            else:
                pass    
            # 没设置起始页
            if(not start_page):
                if(msg):
                    msg = msg + ",请设置起始页"
                else:
                    msg = "请设置起始页"
            else:
                pass  
            # 没设置爬取页数
            if(not page_num):
                if(msg):
                    msg = msg + ",请设置爬取页数"
                else:
                    msg = "请设置爬取页数"
            else:
                pass 
        if(msg):
            res = {
                "msg": msg,
                "code": 400,
                "data": ""
            }
        else:
            res = {
                "msg": "设置成功",
                "code": 200,
                "data": ""
            }

            # 多进程管理
            #p1 = Process(target = RunSpider,args=(src_c,key_c, src_e, key_e, page_num, start_page, )) #必须加,号 
            #p1.start()
            
            
            # 获取时间
            time = time.split(':')
            print(time[0])
            print(time[1])
            print(circle)
            #定时设置
            trigger = ""
            if(circle == "day"):
                trigger = CronTrigger(hour=time[0], minute=time[1])
            elif(circle == "week"):
                trigger = CronTrigger(hour=time[0], minute=time[1], day_of_week='mon')
            elif(circle == "month"):
                trigger = CronTrigger(hour=time[0], minute=time[1], day=1) 
            elif(circle == "year"):
                trigger = CronTrigger(hour=time[0], minute=time[1], day=1, month=1)   
            else:
                trigger = CronTrigger(hour=time[0], minute=time[1])
           
           
            exist_jobs = scheduler.get_jobs()
            print(exist_jobs)
            if(exist_jobs):
                # print("is_exist")
                #scheduler.shutdown()
                #scheduler.remove_job('my_job_id')
                # print(scheduler.get_jobs())
                scheduler.reschedule_job('my_job_id', trigger=trigger) #修改任务
                #scheduler.start()
            else:
                scheduler.add_job(RunSpider, trigger, args=[src_c,key_c, src_e, key_e, page_num, start_page], id='my_job_id', replace_existing=True) #添加test函数任务
                scheduler.start()
            
            
    result_json = jsonify(res)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    
    return result_json
    
@app.route('/search/paper/unmark/list')  
def GetPaperUnmarkList():
    #res = mongo.db.collection.find(filter)	
    res = mongo.db.Document.find({"is_marked":False}).limit(50)
    len_res = res.count()
    if(len_res):
        dict2 = []
        # id = 1
        for i in res:
            dict1 = {}
            dict1["id"] = str(i['_id'])
            dict1["title"] = i['title']
            dict1["src"] = i['src']
            dict2.append(dict1)
            # id = id + 1
        print(dict2)
        result = {
            'msg': "查询成功!",
            'code': 200,
            'data': dict2
        }
    else:
        result = {
            'msg': "查询失败!",
            'code': 400,
            'data': ""
        }
    result_json = jsonify(result)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    return result_json   
    
    
@app.route('/search/paper/mark/list')  
def GetPaperMarkList():
    data = request.args
    data = data.to_dict()
    info = json.loads(data["info"])
    print(info)
    # 初始请求，所有文献
    if(info['type'] == "start"):
        #res = mongo.db.collection.find(filter)	
        res = mongo.db.Document.find({"is_update":True}).limit(20)
    # searchkey
    elif(info['type'] == "common"):
        print("search_key")
        condition = {}
        filter = {}
        condition['$regex'] = info["search_key"]
        filter["title"] = condition
        filter["is_update"] = True
        res = mongo.db.Document.find(filter)	
            
    #high search
    else:
        print("search_high")
        condition_title = {}
        condition_key = {}
        condition_author = {}
        filter = {}
        
        condition_title['$regex'] = info["title"]
        filter["title"] = condition_title
        
        if(info["src"]):
            filter["src"] = info["src"]
        else:
            pass
        
        condition_key['$regex'] = info["key"]
        filter["keywords"] = condition_key
        
        condition_author['$regex'] = info["author"]
        filter["author"] = condition_author
        
        filter["is_update"] = True
        print(filter)
        res = mongo.db.Document.find(filter)	
        
        
    len_res = res.count()
    if(len_res):
        dict2 = []
        # id = 1
        for i in res:
            dict1 = {}
            dict1["id"] = str(i['_id'])
            dict1["title"] = i['title']
            dict1["author"] = i['author']
            dict1["src"] = i['src']
            dict2.append(dict1)
            # id = id + 1
        print(dict2)
        result = {
            'msg': "查询成功!",
            'code': 200,
            'data': dict2
        }
    else:
        result = {
            'msg': "查询失败!",
            'code': 400,
            'data': ""
        }
    
    result_json = jsonify(result)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    return result_json   
 
    
@app.route('/search/paper/detail')  
def GetPaperDetail():
    data = request.args
    data = data.to_dict()
    print(data)
    id = data["id"]
    print(id)
    res = mongo.db.Document.find_one({"_id":ObjectId(id)})
    #len_res = res.count
    if(res):
        print(res)
        res["_id"] = str(res['_id'])
        res.pop("is_submit") 
        res.pop("is_update") 
        res.pop("is_marked") 
        res.pop("valid") 
        result = {
            'msg': "查询成功!",
            'code': 200,
            'data': res
        }
    else:
        result = {
            'msg': "查询该文献失败!",
            'code': 400,
            'data': ''
        }
        
    result_json = jsonify(result)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    return result_json  
      
    
@app.route('/search/paper/save')
def PaperSave():
    data = request.args
    data = data.to_dict()
    print(data)
    id = data["id"]
    print(id)
    res = mongo.db.Document.find_one({"_id":ObjectId(id)})
    if(res):
        backup = res
        # res["start_name"] = data["start_name"]
        # res["start_type"] = data["start_type"]
        # res["end_name"] = data["end_name"]
        # res["end_type"] = data["end_type"]
        # res["rel_name"] = data["rel_name"]
        # res["rel_attr"] = data["rel_attr"]
        # res["evi_level"] = data["evi_level"]
        # res["mark_user"] = data["mark_user"]
        
        data.pop("id")
        info = data
        print(info)
        res["mark_info"] = info
        res["is_marked"] = True
        res.pop("_id") 
    
        print(res)
    
        # 插入表格
        name = {
            'title': res['title']
        }
        res_insert = mongo.db.Document.update_one(
            name,
            {'$set': res},
            # upsert = True
        )
        # res_insert = mongo.db.DocumentMarked.insert_one(res)
        print(res_insert)
        print(res_insert.matched_count, res_insert.modified_count)
        if(res_insert.modified_count):
            result = {
                'msg': "保存成功!",
                'code': 200,
                'data': ""
            }
        else:
            result = {
                'msg': "保存失败！",
                'code': 400,
                'data': ""
            }
    else:
        result = {
            'msg': "查询该文献失败!",
            'code': 400,
            'data': ""
        }

    
    result_json = jsonify(result)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    return result_json      
    
    
@app.route('/search/paper/update')   
def GetPaperUpdateList():
    res = mongo.db.Document.find({"is_marked":True,"is_submit":False,"valid":True})
    len_res = res.count()
    if(len_res):
        dict2 = []
        # id = 1
        for i in res:
            print(i)
            dict1 = {}
            dict1["id"] = str(i['_id'])
            dict1["title"] = i['title']
            dict1["mark_user"] = i['mark_user']
            dict2.append(dict1)
            # id = id + 1
        print(dict2)
        result = {
            'msg': "查询成功!",
            'code': 200,
            'data': dict2
        }
    else:
        result = {
            'msg': "所有标注文献已更新",
            'code': 200,
            'data': ""
        }
    result_json = jsonify(result)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    return result_json  


@app.route('/submit/update')  
def SubmitUpdatePaper():
    condition = {"is_marked":True,"is_submit":False}
    res = mongo.db.Document.update_many(
        condition, 
        {'$set': {
            'is_submit': True
        }},
    )
    print(res.matched_count, res.modified_count)
    if(res.modified_count):
        result = {
            'msg': "提交更新成功!",
            'code': 200,
            'data': ""
        }
    else:
        result = {
            'msg': "提交更新失败!",
            'code': 400,
            'data': ""
        }

    result_json = jsonify(result)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    return result_json    
        
    
@app.route('/paper/invalid')  
def PaperInvalid():
    data = request.args
    data = data.to_dict()
    print(data)
    id = data["id"]
    print(id)
    res = mongo.db.Document.find_one({"_id":ObjectId(id)})
    if(res):
        print(res)
        res["is_marked"] = True
        res["valid"] = False
        
        # 插入表格
        name = {
            'title': res['title']
        }
        res_insert = mongo.db.Document.update_one(
            name,
            {'$set': res},
            # upsert = True
        )
        # res_insert = mongo.db.DocumentMarked.insert_one(res)
        print(res_insert)
        print(res_insert.matched_count, res_insert.modified_count)
        if(res_insert.modified_count):
            result = {
                'msg': "该文献已修改为不合格",
                'code': 200,
                'data': ''
            }
        else:
            result = {
                'msg': "修改失败",
                'code': 400,
                'data': ''
            }
    else:
        result = {
            'msg': "查询该文献失败!",
            'code': 400,
            'data': ''
        }
        
    result_json = jsonify(result)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    return result_json 


@app.route('/upload', methods=['POST', 'GET', 'OPTIONS'])
def Upload():
    if request.method == 'GET' or request.method == 'POST' or request.method == 'OPTIONS':
        if request.method == 'GET':
            print("get")
        if request.method == 'POST':
            print("post")
        if request.method == 'OPTIONS':
            print("OPTIONS")
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/uploads',f.filename)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        result = {
            'msg': "文件上传成功",
            'code': 200,
            'data': ''
        }
    else:
        print("error")
        result = {
            'msg': "文件上传失败",
            'code': 400,
            'data': ''
        }
    result_json = jsonify(result)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    return result_json 

@app.route('/paper/pdf/list')  
def GetPdfList():
    path = "static/uploads"
    list = os.listdir(path)
    print (list)
    result = {
        'msg': "获取文件列表成功",
        'code': 200,
        'data': list
    }
    result_json = jsonify(result)
    result_json.headers.add('Access-Control-Allow-Origin', '*')
    return result_json 
    

if __name__ == '__main__':
    app.run(debug = True)