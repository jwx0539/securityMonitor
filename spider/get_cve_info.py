import re
import time
import requests
import os
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs


nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_CVE_urls():
    urls = []
    res = requests.get('https://cassandra.cerias.purdue.edu/CVE_changes/today.html')
    #print(res.text)
    targets = re.findall(r"New entries:(.*?)Graduations",res.text,re.S|re.M)
    for target in targets:
        soup = bs(target,'html.parser')
        tags = soup.find_all('a')
        #print(urls)
        for i in tags:
            url = i['href']
            urls.append(url)
        return urls

def CVE_info():  
    urls = get_CVE_urls()
    select_msg = ''
    wordlist = []
    keywords = []
    if(len(urls)==0):
        msg = nowtime + '<p>今日CVE_today风和日丽，无大事发生!!!</p>'
        return msg
    else:
        msg_header = '<p>今日CVE_today一共<font size="3" color="red">' + str(len(urls))+'</font>个。'
        for url in urls:
            res = requests.get(url, timeout=60)
            soup = bs(res.text, 'html.parser')
            cveId = soup.find(nowrap='nowrap').find('h2').string
            table = soup.find(id='GeneratedTable').find('table')
            company = table.find_all('tr')[8].find('td').string
            createdate = table.find_all('tr')[10].find('td').string
            content = table.find_all('tr')[3].find('td').text
            data = {'time':nowtime,'from':'CVE-Today-'+cveId,'content':content,'link':url}
            DBNAME = ''
            DBUSERNAME = ''
            DBPASSWORD = ''
            DB = ''    #数据库地址
            PORT = 27017
            db_conn = MongoClient(DB, PORT)
            na_db = getattr(db_conn, DBNAME)
            na_db.authenticate(DBUSERNAME, DBPASSWORD)
            c = na_db.cvedatas
            c.update_one({"content": data['content']}, {'$set': data}, True)
            wordlist.append(data)
        return wordlist
            
        

if __name__ == '__main__':
    CVE_info()
    