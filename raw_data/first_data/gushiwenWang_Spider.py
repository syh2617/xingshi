import bs4
import requests
import time
import re
import csv
from bs4 import BeautifulSoup

#古诗文网 《百家姓》
xing= {'202018018苏玉恒':["历史来源","家族名人","地望分布"]}#存储所有姓氏（起源、名人、分布）的文字资料
# 设置 User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def keep_chinese_and_numbers(text):
    # 使用正则表达式匹配中文字符、中文标点符号和阿拉伯数字
    pattern = re.compile(r'[\u4e00-\u9fa5，。、；：！？【】（）《》“”‘’0-9]+')
    result = pattern.findall(text)
    # 将匹配结果列表连接成一个字符串并返回
    return ''.join(result)

#存储所有  姓氏链接
def getLink():
    r = requests.get('https://so.gushiwen.cn/guwen/book_e5f673a3c14d.aspx', headers=headers)
    soup = bs4.BeautifulSoup(r.content.decode('utf-8'), 'html.parser')
    dll = soup.find(class_="bookcont")
    k=[]
    for aa in dll.find_all('a'):
        text = aa['href']
        full_link = f"https://so.gushiwen.cn{text}"
        k.append(full_link)
    return k

#爬取 每个姓氏url的html
def getHtml(url):
    try:
        rr=requests.get(url,timeout=30)
        rr.raise_for_status()
        rr.encoding='utf-8'
        return rr.text
    except Exception as ex:
        print("爬取{}网页时出错，出错原因：{}。".format(url,ex))
        return ""

#从每个姓氏html中，找出有用信息
def getTxt(html):
    aaa=""
    bbb=""
    ccc=""
    soup2=bs4.BeautifulSoup(html, 'html.parser')
    #han 为姓氏
    han=soup2.title
    han=han.string.strip()
    han=han[4:]
    lenn=len(han)
    han=han[:lenn-5]
    #chinese_text 为起源、名人、分布
    chinese_text = ''
    for paragraph in soup2.find_all('p'):
        text=paragraph.get_text()
        chinese_text += keep_chinese_and_numbers(text)
        chinese_text +='\n'
    # 找到每个部分的起始位置
    start_aaa = chinese_text.find("历史来源")
    start_bbb = chinese_text.find("家族名人")
    start_ccc = chinese_text.find("地望分布")
    if start_ccc==-1:
        start_ccc = chinese_text.find("迁徙分布")
        if han=='沙' or han=='能' or han=='宰':
            start_ccc = chinese_text.find("迁徙分布",start_ccc+5)
    if start_ccc==-1:
        start_ccc = chinese_text.find("迁移分布")
    # 切分字符串
    if start_bbb==-1:
        start_bbb=start_ccc
    aaa = chinese_text[start_aaa:start_bbb]
    bbb = chinese_text[start_bbb:start_ccc]
    ccc = chinese_text[start_ccc:]
    #去结尾
    start_index = ccc.rfind("\n", 0, ccc.rfind("\n") - 1) + 1
    end_index = ccc.rfind("\n", 0, start_index) + 1
    ccc=ccc[:end_index]
    if han=='姓':
        indexx=bbb.find('\n')
        bbb=bbb[:indexx]+'\n'

    xing[han]=[han,aaa,bbb,ccc]
    #测试

    return han
    #print(ccc)

#主程序
#先爬取特定姓氏链接，再进特定网站 爬取网站内容

xingshi=getLink() #存储所有姓氏链接

i=0
for url in xingshi:#姓氏资料，循环爬

    i=i+1

    html=getHtml(url)
    han=getTxt(html)
    #time.sleep(1)
    with open("D:\\PycharmProjects\\pythonProject1\\venv\\20240414_20241231\\xing_gushiwen.csv", 'a+', encoding='utf-8-sig',newline='') as csvFile:
        writer=csv.writer(csvFile)
        writer.writerow(xing[han])

    #if i%10==0: print(i)

