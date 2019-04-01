import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import time
from PIL import Image
from fateadm_api import FateadmApi
import datetime
from selenium import webdriver
from pymongo import MongoClient
import random
import re

user_agent = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)'
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50'
]

def cookie_init():
	retries = 1
	while retries < 3:
		cookie = {}
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/65.0.3325.181 Safari/537.36'}
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-dev-shm-usage')
		client = webdriver.Chrome(options=chrome_options)
		client.get("https://weixin.sogou.com/antispider/?from=%2fweixin%3Ftype%3d2%26query%3d360CERT")
		path = './1.png'
		imgpath = './yzm.png'
		client.get_screenshot_as_file(path)
		im = Image.open(path)
		box = (705, 598, 900, 680)  # 设置要裁剪的区
		region = im.crop(box)
		region.save(imgpath)
		capt = client.find_element_by_xpath('//*[@id="seccodeInput"]')
		test = FateadmApi('','','','')  #打码平台接口
		code = test.PredictFromFile('30600','./yzm.png')  #打码平台识别
		#code = '123456'
		print(code)
		capt.send_keys(code)
		time.sleep(1)
		client.find_element_by_xpath('//*[@id="submit"]').click()
		time.sleep(2)
		#print(new_html)
		for item in client.get_cookies():
		    cookie[item["name"]] = item["value"]
		try:
			print(cookie['SNUID'])
		except Exception:
			print ("解锁失败。重试次数:{0:d}".format(3-retries))
			retries += 1
			continue
		time.sleep(5)
		return cookie['SNUID']

def get_info(url,table,a,tb_msg,headers):
	r = requests.get(url=url,headers=headers)
	r.encoding='utf-8'
	#print(url)
	#print(r.text)
	try:
		soup = bs(r.text,'html.parser')
		content = soup.find('a',{'uigs':'account_article_0'}).text
		send_time = soup.find_all('span')[-1].find('script').text
		re_time = re.findall(r"timeConvert\('(.*?)'\)",send_time)[0]
		#print(re_time)
		#print(send_time)
		#print(content)
		now_time = int(time.time())
		print_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		timeArray = time.localtime(int(re_time))
		otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		ava_time = now_time - int(re_time)
		#print(ava_time)
		msg = content + ' from ' + table[a]
		demo = {'time':otherStyleTime,'from':table[a],'content':content,'link':url}
		tb_msg.append(demo)
		DBNAME = ''
		DBUSERNAME = ''
		DB = ''          #数据库地址
		PORT = 27017
		db_conn = MongoClient(DB, PORT)
		na_db = getattr(db_conn, DBNAME)
		na_db.authenticate(DBUSERNAME, DBPASSWORD)
		c = na_db.wechatdatas
		c.update_one({"content": demo['content']}, {'$set': demo}, True)
		#print(tb_msg)
		with open('wechat_log.txt','a+') as f:
			f.write(print_time+'\n')
	except Exception as e:
		#print(e)
		pass
		
	
	

def wechat_info():
	table = ['360CERT','长亭安全课堂','千里目实验室','云鼎实验室','ADLab']
	tb_msg = []
	a = -1
	with open('./snuid.txt') as f:
		snuid = f.readline().strip()
		headers = {
		'Referer': 'http://weixin.sogou.com/weixin?type=1&query=python&ie=utf8&s_from=input&_sug_=n&_sug_type_=1&w=01015002&oq=&ri=5&sourceid=sugg&sut=0&sst0=1540733222633&lkt=0%2C0%2C0&p=40040108',
		'User-Agent': random.choice(user_agent),
		'Cookie': 'SUV=00D80B85458CAE4B5B299A407EA3A580;SNUID=' + snuid,
		}
		rr = requests.get(url='https://weixin.sogou.com/weixin?type=1&s_from=input&query=360CERT&ie=utf8&_sug_=n&_sug_type_=',headers=headers)
	if len(rr.text) > 6000:
		pass
	else:
		uid = cookie_init()
		headers = {
		'Referer': 'http://weixin.sogou.com/weixin?type=1&query=python&ie=utf8&s_from=input&_sug_=n&_sug_type_=1&w=01015002&oq=&ri=5&sourceid=sugg&sut=0&sst0=1540733222633&lkt=0%2C0%2C0&p=40040108',
		'User-Agent': random.choice(user_agent),
		'Cookie': 'SUV=00D80B85458CAE4B5B299A407EA3A580;SNUID=' + uid,
		}
		ff = open('./snuid.txt','w+')
		ff.write(uid)
		ff.close()
	for i in table:
		a+=1
		url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=' + i + '&ie=utf8&_sug_=n&_sug_type_='
		get_info(url,table,a,tb_msg,headers)
	print(tb_msg)
	return tb_msg
		

if __name__ == '__main__':
	wechat_info()
