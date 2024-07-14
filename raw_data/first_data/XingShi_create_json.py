import csv
import json

#


xing_gushiwen_file_path="D:\\PycharmProjects\\KGQA_XS-master\\raw_data\\first_data\\xing_gushiwen.csv"

xingShiTuTeng_file_path="D:\\PycharmProjects\\\KGQA_XS-master\\raw_data\\first_data\\XingShiTuTeng.txt"

xing_QiYuan_file_path="D:\\PycharmProjects\\KGQA_XS-master\\raw_data\\first_data\\xing_QiYuan.txt"

#xing_QiYuan.txt 该文件由自己整理所得

tuTeng={}
xingGuShiWen={}
#把xing_gushiwen.csv里的数据放进字典xingGuShiWen,再把图腾txt放进xingGuShiWen
with open(xing_gushiwen_file_path, 'r', encoding='utf-8-sig',newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        rowa=row[0]
        rowb=row
        xingGuShiWen[rowa]=rowb


with open(xingShiTuTeng_file_path, 'r', encoding='utf-8-sig',newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if row[0][0]=='百':continue
        text=row[0]
        han=text[0]#姓
        num=text.find('：')
        text=text[num+1:]
        xingGuShiWen[han].append(text)

#创建一个json：entities_item_mimini.json
# all_xing字典 ：包含每个姓氏的详细信息

all_xing={
    "华夏始祖":{
        "历史来源":["-"],
        "家族名人":["-"],
        "分布":["-"],
        "姓氏图腾":["-"]
    }
}

for value in xingGuShiWen.values():
    #有的姓氏没图腾，
    if len(value)<5:
        value.append('')
    #我把  xing_QiYuan.txt中存在  并且 xingGuShiWen字典中不存在  的姓氏找出来 ， 放到了 xing_gushiwen.csv（用记事本打开）  末尾
    if len(value)<5:
        value.append('')
    if len(value)<5:
        value.append('')
    if len(value)<5:
        value.append('')

    if (len(value[1])>0 and value[1].find("来源")>=0 and value[1].find("来源")<=4):
        value[1]=value[1][4:]
    if (len(value[2])>0 and value[2].find("名人")>=0 and value[2].find("名人")<=4):
        value[2]=value[2][4:]
    if (len(value[3])>0 and value[3].find("分布")>=0 and value[3].find("分布")<=4):
        value[3]=value[3][4:]

    text1=value[1]
    if len(value[1])>0:
        text1=value[1].split("\n")
        text1=[string for string in text1 if string != '']
    text2 = value[2]
    if len(value[2] )> 0:
        text2 = value[2].split("\n")
        text2 = [string for string in text2 if string != '']
    text3 = value[3]
    if len(value[3] )> 0:
        text3 = value[3].split("\n")
        text3 = [string for string in text3 if string != '']

    all_xing[value[0]]={
        "历史来源": text1,
        "家族名人": text2,
        "分布": text3,
        "姓氏图腾": [value[4]]
    }

filename1 = "entities_item_mimini.json"

with open(filename1, 'w', encoding='utf-8') as json_file:
    json.dump(all_xing, json_file, indent=4, ensure_ascii=False)

print("JSON文件已创建：", filename1)

# 创建一个json：vizdata_mimini_aglin1.json
# all_links_nodes字典 ：links(姓之间的联系)nodes(每个姓)

all_links_nodes={
    "links": [],
    "nodes": []
}

one_node={
    "class": "祖先",
    "group": "0",
    "id": "华夏始祖",
    "size": "30"
}

all_links_nodes["nodes"].append(one_node)

one_link={
    "relation": "后代",
    "source": "",
    "target": "",
    "value": 3
}

zong_links_nodes=[]#存储xing_QiYuan.txt
all_links= []
all_nodes= {'华夏始祖':0}
with open(xing_QiYuan_file_path, 'r', encoding='utf-8-sig',newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        zong_links_nodes.append(row)


one_node = {
            "class": "后裔",
            "group": "2",
            "id": "",
            "size": "8"
        }
one_node = {
            "class": "祖先",
            "group": "1",
            "id": "",
            "size": "10"
        }

i=0
## i作为分隔符，区分单姓(i==0)、复姓(i==1)
for index in zong_links_nodes:
    if index[0][0]=='1':
        i=1
        continue
    text=index[0]
    k_index=text.find('：')
    start_a=text[:k_index]
    end_a=text[k_index+1:]

    #添加link
    if i==0:
        for k in end_a:
            all_links.append( [start_a,k] )
    elif i==1:
        all_links.append( [start_a,end_a] )

    #添加node
    if i==1:
        all_nodes[end_a]=2
        if start_a=="华夏始祖":
            all_nodes[end_a] = 1

    #由于该图为树状图，添加完成根节点后，只看end_a就行了
    if i==0:
        for indexxx in end_a:
            all_nodes[indexxx]=2
            if start_a == "华夏始祖":
                all_nodes[indexxx] = 1

for index in all_links:
    all_links_nodes["links"].append({"relation": "后代","source": index[0],"target": index[1],"value": 3})

i=0
for key in all_nodes.keys():
    if i==0:
        i=1
        continue
    if all_nodes[key]==1:
        all_links_nodes["nodes"].append({"class": "祖先","group": "1","id": key,"size": "20"})
    elif all_nodes[key]==2:
        all_links_nodes["nodes"].append({"class": "后裔","group": "2","id": key,"size": "8"})
#nodes
#print(all_links_nodes["links"])
#print(all_links_nodes["nodes"])
#print(zong_links_nodes)
#print(all_links)
#print(all_nodes)

filename2 = "vizdata_mimini_aglin.json"

with open(filename2, 'w', encoding='utf-8') as json_file:
    json.dump(all_links_nodes, json_file, indent=4, ensure_ascii=False)

print("JSON文件已创建：", filename2)


#后续



all_nodes['华夏始祖']=1
with open("fangji_spo.txt", 'w+', encoding='utf-8-sig',newline='') as file:
    for index in all_links:
        text=index[1]+'||'+'后代'+'||'+index[0]+'||'

        key = index[1]
        if all_nodes[key] == 1:
            text = text + "祖先"
        elif all_nodes[key] == 2:
            text = text + "后裔"
        text=text+"||"

        key=index[0]
        if all_nodes[key] == 1:
            text=text+"祖先"
        elif all_nodes[key] == 2:
            text = text + "后裔"

        text = text + "\n"
        file.write(text)
        #print(text)
print("fangji_spo.txt已创建")

with open("zhongyao_spo.txt", 'w+', encoding='utf-8-sig',newline='') as file:
    for index in all_xing:
        #{'历史来源': '', '家族名人': '', '分布': '', '姓氏图腾': ['']}
        text=index

        k=' '.join(all_xing[text]['历史来源'])
        if k=='':k='暂无资料'
        ans=text+'&&'+'历史来源'+'&&'+k+'&&'+'姓氏'+'&&'+'历史来源'+'\n'
        file.write(ans)
    #    print(ans)

        k = ' '.join(all_xing[text]['家族名人'])
        if k=='':k='暂无资料'
        ans=text+'&&'+'家族名人'+'&&'+k+'&&'+'姓氏'+'&&'+'家族名人'+'\n'
        file.write(ans)

        k = ' '.join(all_xing[text]['分布'])
        if k == '': k = '暂无资料'
        ans=text+'&&'+'分布'+'&&'+k+'&&'+'姓氏'+'&&'+'分布'+'\n'
        file.write(ans)

        k = ' '.join(all_xing[text]['姓氏图腾'])
        if k == '': k = '暂无资料'
        ans=text+'&&'+'姓氏图腾'+'&&'+k+'&&'+'姓氏'+'&&'+'姓氏图腾'+'\n'
        file.write(ans)

print("zhongyao_spo.txt已创建")

filename1 = "fangji.json"

#with open(filename1, 'w', encoding='utf-8') as json_file:
    #json.dump(all_links_nodes, json_file, indent=4, ensure_ascii=False)

print("JSON文件已创建：", filename1)

