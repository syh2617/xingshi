# -*- coding: utf-8 -*-
#import pyltp
#LTP_DATA_DIR = '/myLTP2/ltp_data_v3.4.0'  # ltp模型目录的路径

import os
from jieba import lcut_for_search
from neo_db.config import graph, CA_LIST
from py2neo import Graph,NodeMatcher


'''
get_CURD_array 该函数进行 增删改查过程 的分词，输入格式设置
1.添加  
    添加&&{祖先姓氏}&&{后裔姓氏}
2.删除  
    删除&&{姓氏}
    删除&&{姓氏}&&{属性}
3.修改  
    修改&&{姓氏}&&{属性}&&{内容}
'''
def get_CRUD_array(words):
    target_array = words.split('-')
    print("苏玉恒-get_CRUD_array")

    if target_array[1][-1]=='姓':
        target_array[1]=target_array[1][0:-1]
    if words[0:2]=="添加":
        if target_array[2][-1] == '姓':
            target_array[2] = target_array[2][0:-1]
    if words[0:2]!="添加" and words[0:2]!="删除" and words[0:2]!="修改":
        target_array.clear()
        target_array.append("输入格式错误")
        target_array.append("华夏始祖")
    return target_array

def get_target_array(words):
    words = words.replace("姓", "")
    word = words.split('的')
    if len(word)==1:word.append('1')
    #分词 搜索引擎模式
    word0=lcut_for_search(word[0])

    matcher = NodeMatcher(graph)
    target_array=[]
    for i in word0:
        result1 = matcher.match("Entity", Name=i)
        if result1:
            target_array.append(i)
            break
    target_array.append(word[1])
    target_array.append("1")
    return target_array

if __name__ == '__main__':
    question = "张的历史来源是什么样"
    target_array = get_target_array(str(question))
    print(target_array)
    #print("w："[1])


