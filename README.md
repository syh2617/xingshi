# 中国姓氏文化可视化系统<br>

# 项目目录
1) app.py是整个系统的主入口<br>
2) templates文件夹是HTML的页面<br>
     &emsp;|——index.html 欢迎界面<br> 
     &emsp;|——search.html 搜索姓氏关系页面<br>
     &emsp;|——all_relation.html 所有姓氏关系页面<br>
     &emsp;|——KGQA.html 姓氏问答页面<br>
     &emsp;|——CRUD.html 修改资料页面<br>
3) static文件夹存放css、js、fonts，是页面的样式和效果的文件，华北水利水电大学logo和项目首页<br>
     &emsp;|——CRUD.html 修改资料页面<br>
4) raw_data文件夹是存放数据处理后的三元组文件、爬取姓氏资料的代码<br>
5) neo_db文件夹是知识图谱构建模块<br>
     &emsp;|——config.py 配置参数<br>
     &emsp;|——create_graph.py 创建知识图谱，图数据库的建立<br>
     &emsp;|——query_graph.py 知识图谱的查询<br>
6) KGQA文件夹是问答系统模块<br>
     &emsp;|——ltp.py 分词<br>
7) spider文件夹是爬虫模块<br>
     &emsp;|——已经爬取好images和json 可以不用再执行<br>
     &emsp;|——show_profile.py 是调用姓氏资料和图谱展示在前端的代码
8) images文件夹是存放项目介绍的图片
<hr>

# 部署步骤：<br>
* 0.安装所需的库 执行pip install -r requirement.txt<br>
* 1.先下载好neo4j图数据库，并配好环境。修改neo_db目录下的配置文件config.py,设置图数据库的账号和密码。<br>
* 2.切换到neo_db目录下，执行python  create_graph.py 建立知识图谱<br>
* 3.在spider目录下，运行data_process.py(已处理好)<br>
* 4.在static目录下，运行neo2json.py(已处理好)<br>
* 5.运行python app.py,浏览器打开http://127.0.0.1:5000即可查看<br>



