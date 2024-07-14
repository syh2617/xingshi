#! -*- coding:utf-8 -*-
import json
from neo_db.config import graph, CA_LIST
from py2neo import Graph,NodeMatcher
import codecs

fw = open('data.json', 'w', encoding='utf-8')
k = graph.run(
    "match(n) return n.Name,n.cate,n.历史来源,n.家族名人,n.分布,n.姓氏图腾"
).data()

tempDict = list(k)

tempDict2={}
for index in tempDict:
    a=index['n.Name']
    if index['n.历史来源']==None:
        continue
    tempDict2[a]= {
        "姓氏" : index['n.Name'],
        "历史来源" : index['n.历史来源'],
        "家族名人" : index['n.家族名人'],
        "分布" : index['n.分布'],
        "姓氏图腾" : index['n.姓氏图腾'],
    }

#print(tempDict2)
l1 = json.dumps(tempDict2, ensure_ascii=False)
fw.write(l1)

