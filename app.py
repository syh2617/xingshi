#! -*- coding:utf-8 -*-
import subprocess

from flask import Flask, render_template, request, jsonify
from py2neo import Graph
import codecs
import os
import json
from neo_db.query_graph import query,get_KGQA_answer,get_answer_profile,get_CRUD_answer
from KGQA.ltp import get_target_array,get_CRUD_array
from static.neo2json import get_json_data
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

def index(name=None):
    return render_template('index.html', name = name)

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

@app.route('/KGQA', methods=['GET', 'POST'])
def KGQA():
    return render_template('KGQA.html')

@app.route('/CRUD', methods=['GET', 'POST'])
def CRUD():
    return render_template('CRUD.html')

@app.route('/get_all_relation', methods=['GET', 'POST'])
def get_all_relation():
    subprocess.call(["python", "D:/PycharmProjects/KGQA_XS-master/static/neo2json.py"])
    print("苏玉恒-get_all_relation-更新关系图")
    graph = Graph('http://localhost:7474', user='neo4j', password='123syh123', name="neo4j")
    print("连接成功！")
    data = graph.run(
        "match(p)-[r]->(n:Entity) return p.Name,r.relation,n.Name,p.cate,n.cate"
    ).data()
    data = list(data)
    json_data = get_json_data(data)
    target_file_path = r"D:\PycharmProjects\KGQA_XS-master\static\fangji.json"
    f = codecs.open(r'D:\PycharmProjects\KGQA_XS-master\static\fangji.json', 'w+', 'utf-8')
    f.write(json.dumps(json_data, indent=4, ensure_ascii=False))
    return render_template('all_relation.html')


@app.route('/CRUD_answer',methods=['GET','POST'])
def CRUD_answer():
    question = request.args.get('name')
    json_data = get_CRUD_answer(get_CRUD_array(str(question)))
    return jsonify(json_data)

@app.route('/KGQA_answer', methods=['GET', 'POST'])
def KGQA_answer():
    question = request.args.get('name')
    json_data = get_KGQA_answer(get_target_array(str(question)))
    return jsonify(json_data)

@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    json_data=query(str(name))
    return jsonify(json_data)

if __name__ == '__main__':
    app.debug=True
    app.run()
