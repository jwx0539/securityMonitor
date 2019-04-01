import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import time
import os



nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def anquanke_info():
	url = 'https://www.anquanke.com/'
	#keywords = config.keywords#关注的关键字
	wordlist = []
	select_msg = ''
	res = requests.get(url,timeout=60)
	#print(res.text)
	soup = bs(res.text,'html.parser')
	divs = soup.find_all('div',{'class':'title'})[0:9]
	spans = soup.find_all('span',{'class':'date'})
	#print(divs)
	i = 0 
	list_date = [span.find('span').text for span in spans]
	#print(list_date)
	for div in divs:
		content = div.find('a').string
		#print(description)
		site = 'https://www.anquanke.com' + div.find('a')['href']
		#print(site)
		data = {'time':list_date[i],'from':'安全客','content':content,'link':site}
		i +=1
		DBNAME = ''
		DBUSERNAME = ''
		DBPASSWORD = ''
		DB = ''     #数据库地址
		PORT = 27017
		db_conn = MongoClient(DB, PORT)
		na_db = getattr(db_conn, DBNAME)
		na_db.authenticate(DBUSERNAME, DBPASSWORD)
		c = na_db.anquankedatas
		c.update_one({"content": data['content']}, {'$set': data}, True)
		wordlist.append(data)
	#print(wordlist)
	return wordlist
				
				


if __name__ == '__main__':
	anquanke_info()