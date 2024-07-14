#! -*- coding:utf-8 -*-
#将数据导入到neo4j中
#先启动neo4j,运行完creat_graph.py，然后才能运行neo2json.py
#标签名，关系名中不要有括号以及英文句号

import subprocess
from py2neo import Graph, Node, Relationship#,NodeSelector
from config import graph


count = 0
with open("../raw_data/fangji_spo.txt", encoding='utf-8') as f:
    graph.run('MATCH (n) DETACH DELETE n')  #删除图数据库中数据
    for line in f.readlines():
        count += 1
        if count <= 1000000:
            rela_array=line.strip("\n").split("||")
            print(count)
            graph.run("MERGE(p: Entity{cate:'%s',Name: '%s'})"% (rela_array[3], rela_array[0]))
            graph.run("MERGE(p: Entity{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[2]))
            graph.run(
                "MATCH(e: Entity), (cc: Entity) \
                WHERE e.Name='%s' AND cc.Name='%s'\
                CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
                RETURN r" % (rela_array[2], rela_array[0], rela_array[1],rela_array[1])
            )
        
with open("../raw_data/zhongyao_spo.txt", encoding='utf-8') as f:
    count=0
    for line in f.readlines():
        count += 1
        if count <= 1000000:
            rela_array= line.replace("\n", " ").split("&&")
            print(count)
            if count==1:
                rela_array[0]='华夏始祖'
                rela_array[1]='历史来源'
                rela_array[2]='暂无资料'
            graph.run("MATCH (n {Name: '%s'})  SET n.%s = '%s'"% (rela_array[0], rela_array[1],rela_array[2]))

subprocess.call(["python", "../spider/json/data_process.py"])
subprocess.call(["python", "../static/neo2json.py"])
