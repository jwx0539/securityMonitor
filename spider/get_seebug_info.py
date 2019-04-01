#! /usr/bin/env python3
# encoding: utf-8
import asyncio
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
from pyppeteer import launch
async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://www.seebug.org')
    await page.waitFor("body > div.footer-up")
    #print(urls)
    wordlist = []
    vuln_time_elements = await page.xpath('//td[@class="text-center datetime hidden-sm hidden-xs td-time"]')
    vuln_post_time = [await (await item.getProperty('textContent')).jsonValue() for item in vuln_time_elements][:10]
    #print(vuln_post_time)
    poc_time_elements = await page.xpath('//td[@class="td-time datetime hidden-sm hidden-xs"]')
    poc_post_time = [await (await item.getProperty('textContent')).jsonValue() for item in poc_time_elements][1:]
    #print(poc_post_time)
    vulns_elements = await page.xpath('//td[@class="vul-title-wrapper"]')
    vuln_content = [await(await item.getProperty('textContent')).jsonValue() for item in vulns_elements][:10]
    vuln_link_elements = await page.xpath('//td[@class="vul-title-wrapper"]/a')
    vuln_link = [await(await item.getProperty('href')).jsonValue() for item in vuln_link_elements][:10]
    #print(vuln_link)
    for i in range(10):
        vuln_data = {'time':vuln_post_time[i],'link':vuln_link[i],'from':'Seebug','content':vuln_content[i]}
        DBNAME = ''
        DBUSERNAME = ''
        DBPASSWORD = ''
        DB = ''    #数据库地址
        PORT = 27017
        db_conn = MongoClient(DB, PORT)
        na_db = getattr(db_conn, DBNAME)
        na_db.authenticate(DBUSERNAME, DBPASSWORD)
        c = na_db.seebugdatas
        c.update_one({"content": vuln_data['content']}, {'$set': vuln_data}, True)
        wordlist.append(vuln_data)
    print(wordlist)
    
        
    

    await browser.close()
asyncio.get_event_loop().run_until_complete(main())