#! -*- coding:utf-8 -*-
from KGQA.ltp import get_CRUD_array
from neo_db.config import graph, CA_LIST
from spider.show_profile import get_profile
from py2neo import Graph,NodeMatcher
import codecs
import os
import json
import base64
import subprocess

def query(name):
    matcher = NodeMatcher(graph)
    result1 = matcher.match("Entity", Name=name)
    if result1 :print()
    else:name = "查无此姓"
    data = graph.run(
    "match(p )-[r]->(n:Entity{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
        Union all\
    match(p:Entity {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name,name)
    )
    data = list(data)
    return get_json_data(data)

def get_json_data(data):
    json_data={'data':[],"links":[]}
    d=[]
    for i in data:
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        d.append(i['p.Name']+"_"+i['p.cate'])
        d.append(i['n.Name']+"_"+i['n.cate'])
        d=list(set(d))
    name_dict={}
    count=0
    for j in d:
        j_array=j.split("_")
    
        data_item={}
        name_dict[j_array[0]]=count
        count+=1
        data_item['name']=j_array[0]
        data_item['category']=CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for i in data:
   
        link_item = {}
        
        link_item['source'] = name_dict[i['p.Name']]
        
        link_item['target'] = name_dict[i['n.Name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)

    return json_data


def get_KGQA_answer(array):
    # array = ['吴', '名人', '的']
    data_array=[]
    kk=0
    matcher = NodeMatcher(graph)
    for i in range(len(array)-2):
        if i==0:
            name=array[0]
        else:
            name=data_array[-1]['p.Name']
        # print("name:", name)
        # print("array:", array)
        # print("similar_words[array[1]]:", similar_words[array[1]])

        result1 = matcher.match("Entity", Name=name)
        if result1:kk=1
        else:continue
        data = graph.run(
            "match(p )-[r]->(n:Entity{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
                Union all\
            match(p:Entity {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name, name)
        )

        # print("data：", data)
        data = list(data)
        data_array.extend(data)
        
        print("==="*36)
    #打开图片
    if kk==0:
        name="查无此姓"
        array[0]="查无此姓"
        data = graph.run(
            "match(p )-[r]->(n:Entity{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
                Union all\
            match(p:Entity {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name, name)
        )

        # print("data：", data)
        data = list(data)
        data_array.extend(data)
    print("data_array:", data_array)
    with open("D:/PycharmProjects/KGQA_XS-master/spider/images/"+"%s.jpg" % (str(array[0])), "rb") as image:
            base64_data = base64.b64encode(image.read())
            b=str(base64_data)
    #
    num=0
    string1=array[1]
    if ('源' in string1)or(('史' in string1)): num = 1  # 来源、起源
    if '祖' in string1: num = 1  # 祖先 历史来源
    if '名人' in string1: num = 2  # 家族名人
    if '布' in string1: num = 3  # 分布
    if '在' in string1: num = 3  # 分布在
    if '位' in string1: num = 3  # 位于
    if '图腾' in string1: num = 4  # 姓氏图腾


    print(array)
    return [get_json_data(data_array), get_profile(str(array[0]),num), b.split("'")[1]]
    # return [get_json_data(data_array)]

def get_answer_profile(name):
    with open("./spider/images/"+"%s.jpg" % (str(name)), "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)
    return [get_profile(str(name),0), b.split("'")[1]]


def get_CRUD_answer(array):
    # array = ['吴', '名人', '的']
    '''
    get_CURD_array 该函数进行 增删改查过程 的分词，输入格式设置
    1.添加
        添加&&{祖先姓氏}&&{后裔姓氏}
    2.删除
        删除&&{姓氏}
        删除&&{姓氏}&&{属性}
    3.修改
        修改&&{姓氏}&&{属性}&&{新内容}
    '''
    data_array = []
    matcher = NodeMatcher(graph)

    num=0
    if len(array)>=3:
        if ('源' in array[2]) or('祖' in array[2])or('史' in array[2]): num = 1  # 来源、起源# 祖先 历史来源
        if '名人' in array[2]: num = 2  # 家族名人
        if ('布' in array[2]) or('在' in array[2])or('位' in array[2]): num = 3  # 分布
        if '图腾' in array[2]: num = 4  # 姓氏图腾
    print(array)

    k='1'
    if array[0]=="添加":
        #添加 关系
        print("添加")
        if len(array) == 3:
            result1 = matcher.match("Entity", Name=array[1])
            result2 = matcher.match("Entity", Name=array[2])
            if result1:print(1)
            else:
                graph.run(
                    "MERGE(p:Entity {cate:'后裔', Name: '%s'}) SET p.历史来源 = '暂无资料', p.家族名人 = '暂无资料', p.分布 = '暂无资料', p.姓氏图腾 = '暂无资料'"
                    % ( array[1]))
            if result2:print(2)
            else:
                graph.run(
                    "MERGE(p:Entity {cate:'后裔', Name: '%s'}) SET p.历史来源 = '暂无资料', p.家族名人 = '暂无资料', p.分布 = '暂无资料', p.姓氏图腾 = '暂无资料'"
                    % (array[2]))
            graph.run(
                "MATCH(e: Entity), (cc: Entity) \
                WHERE e.Name='%s' AND cc.Name='%s'\
                CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
                RETURN r" % (array[1], array[2], "后代", "后代")
            )
        else:
            k="输入格式错误"
    elif array[0]=="删除":
        print("删除")
        node_to_delete = matcher.match("Entity", Name=array[1]).first()
        if len(array)==2 and node_to_delete:
            # 删除 姓氏
            graph.delete(node_to_delete)
        elif len(array)==3 and node_to_delete and num!=0:
            # 删除 姓氏属性
            node_to_delete[array[2]] = "暂无资料"
            graph.push(node_to_delete)
        else:
            k = "输入格式错误"
    elif array[0]=="修改":
        print("修改")
        node_to_changge = matcher.match("Entity", Name=array[1]).first()
        if len(array)==4 and node_to_changge and num!=0:
            node_to_changge[array[2]] = array[3]
            graph.push(node_to_changge)
        else:
            k = "输入格式错误"
    else:
        k = "输入格式错误"


    name = array[1]
    if k == "输入格式错误":
        name=k
    result = matcher.match("Entity", Name=name)
    if result:
        print(name,"存在")
    else:
        name="华夏始祖"
        print(name,"不存在")
    data = graph.run(
        "match(p )-[r]->(n:Entity{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
            Union all\
        match(p:Entity {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name, name)
    )
    data = list(data)
    data_array.extend(data)
    print("===" * 36)


    # 打开图片
    #print("data_array:", data_array)
    with open("D:/PycharmProjects/KGQA_XS-master/spider/images/" + "%s.jpg" % (name), "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)

    subprocess.call(["python", "../spider/json/data_process.py"])
    subprocess.call(["python", "../static/neo2json.py"])
    return [get_json_data(data_array), get_profile(name, num), b.split("'")[1]]


if __name__ == '__main__':
    # json_data=query("吴")
    # print(json_data)##

    KGQA = get_KGQA_answer(['匈', '来源', '的'])
    #KGQA=get_CRUD_answer(get_CRUD_array("添加-22-45"))

    print("===" * 36)
    print(KGQA)

        



