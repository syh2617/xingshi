#! -*- coding:utf-8 -*-
from py2neo import Graph,DatabaseError

try:
    # 尝试连接数据库
    graph =Graph('http://localhost:7474',user='neo4j',password='123syh123', name="neo4j")
    print("连接成功！")
except DatabaseError as e:
    print("连接失败:", e)
CA_LIST = {"祖先": 0, "后裔": 1}
similar_words = {
    "后代": "后代",
    "后裔": "后裔",
    "祖先": "祖先",
    "姓氏": "姓氏",
    "历史来源": "历史来源",
    "分布": "分布",
    "姓氏图腾":"姓氏图腾",
    "家族名人":"家族名人",

}

