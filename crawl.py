import random
import time
import csv
import requests
from bs4 import BeautifulSoup
import re

USER_AGENT_LIST=[
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

refer=[
    'http://you.ctrip.com/sight/chengdu104.html',
    'http://you.ctrip.com/sight/chengdu104/4341.html',
    'http://you.ctrip.com/sight/chongqing158.html',
    'http://you.ctrip.com',
    'https://you.ctrip.com/sight/Chongqing158.html'
]

def get_ip():
    url = 'http://www.xicidaili.com/nn'
    headers = {
        'User-Agent': random.choice(USER_AGENT_LIST)}
    s = requests.get(url, headers=headers).text
    bsObj = BeautifulSoup(s, 'lxml')
    ip_text = bsObj.findAll('tr', {'class': 'odd'})   # 获取带有IP地址的表格的所有行
    ip_list = []
    for i in range(len(ip_text)):
        ip_tag = ip_text[i].findAll('td')   
        ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text() # 提取出IP地址和端口号
        ip_livetime = ip_tag[8].get_text()
#         if "天" in ip_livetime:
#             ip_list.append(ip_port)
        ip_list.append(ip_port)
    return ip_list


def crawl_xiecheng(name,view_id):
    url = 'https://sec-m.ctrip.com/restapi/soa2/12530/json/viewCommentList?_fxpcqlniredt=09031078410304677435'
    f=open('e:/'+name+'.csv','w',encoding='utf-8')
    f.write("star##time##comment"+"\n")
    flag= 0 
    ip_list=get_ip()
    pagesize=10
    pagenum=0
    while 1:
        if pagesize!=10 or pagenum==299:
            break
        time.sleep(0.5)
        print("page:",pagenum)
        data ={"pageid":10650000804,"viewid":view_id,"tagid":0,"pagenum":pagenum,"pagesize":10,
               "contentType":"json","head":{"appid":"100013776","cid":"09031078410304677435",
                                            "ctok":"","cver":"1.0","lang":"01","sid":"8888",
                                            "syscode":"09","auth":"","extension":[{"name":"protocal","value":"https"}]},
               "ver":"7.10.3.0319180000"}

        headers = {
                'Referer':'http://you.ctrip.com/',
                'User-Agent':random.choice(USER_AGENT_LIST),
                'Referer':random.choice(refer)
            }
        
        ip_str=random.choice(ip_list)
        proxies={'http':ip_str}
        html = requests.post(url, data=json.dumps(data), headers=headers,timeout = 30)
        jsondata = json.loads(html.text)['data']['comments']
        for x in jsondata:
            score = x['score']
            date = x['date']
            comment = x['content']
            comment = comment.replace("&#x0A;",' ')
            comment = comment.replace("&#x2F",' ')
            comment = comment.replace("&amp",' ')
            if x['simgs']==None:
                pic_num = 0
            else:
                pic_num = len(x['simgs'])
            result=score+"##"+date+"##"+comment.replace("\n","").replace("\r","").replace("\t","").replace("\r\n","")
            f.write(result+"\n")
        pagenum= pagenum+1
        pagesize=len(jsondata)
    f.close()
    
jingqu=open('e:/project/xiecheng/cd_viewid.csv',encoding='utf-8').readlines()
for i in range(1,len(jingqu)):
    name=jingqu[i].split(",")[0].replace("\n","")
    viewid =  jingqu[i].split(",")[1].replace("\n","")
    print(name)
    crawl_xiecheng(name,viewid)
