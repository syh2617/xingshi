import codecs
import json
from neo_db.config import graph

#with open('D:/PycharmProjects/KGQA_XS-master/spider/json/data.json', encoding='utf-8') as f:
    #data = json.load(f)

def get_profile(name,num):
    k = graph.run(
        "match(n) return n.Name,n.cate,n.历史来源,n.家族名人,n.分布,n.姓氏图腾"
    ).data()

    tempDict = list(k)

    data = {}
    for index in tempDict:
        a = index['n.Name']
        if index['n.历史来源'] == None:
            continue
        data[a] = {
            "姓氏": index['n.Name'],
            "历史来源": index['n.历史来源'],
            "家族名人": index['n.家族名人'],
            "分布": index['n.分布'],
            "姓氏图腾": index['n.姓氏图腾'],
        }





    print("name=",name)
    s=''
    for i in data[name]:
        data[name][i]=data[name][i].replace(" ", "<br>")
        st="<dt class = \"basicInfo-item name\" >"+ str(i)+" \
        <dd class = \"basicInfo-item value\" >"+str(data[name][i])+"</dd ></dt >"
        s+=st
    i=0
    if num==  1:
        i="历史来源"
    if num == 2:
        i = "家族名人"
    if num == 3:
        i = "分布"
    if num == 4:
        i = "姓氏图腾"
    if num!=0:
        data[name][i] = data[name][i].replace(" ", "<br>")
        s = "<dt class = \"basicInfo-item name\" >" + str(i) + " \
                <dd class = \"basicInfo-item value\" >" + str(data[name][i]) + "</dd ></dt >"
    return s

if __name__ == '__main__':
    s = get_profile("吴")
    print(s)