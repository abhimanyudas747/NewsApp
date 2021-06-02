# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 18:04:50 2021

@author: Abhimanyu Das
"""

import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3
import time
from summarizer import Summarizer


def addNews(newsitem, timestamp, cur, con, model):
    link = newsitem.link.text
    article_resp = requests.get(link)
    if(article_resp.status_code != 200):
        return False
    article_soup = BeautifulSoup(article_resp.content, 'lxml')
    cont = article_soup.find_all("div", class_="_3YYSt")
    data = cont[0].text.replace('"', "'")
    data = model(data)
    img = article_soup.find_all("div", class_="_3gupn")
    imgurl = img[0].img['src']
    heading = newsitem.title.text.replace('"', "'")
    query = "INSERT INTO news(TIMESTAMP, HEADLINE, CONTENT, PUBDATE, IMGURL, LINK) VALUES (\
                \""+str(timestamp)+"\", \""+heading+"\", \""+data+"\", \""+newsitem.pubDate.text+"\", \""+imgurl+"\", \""+newsitem.link.text+"\" )"
    cur.execute(query)
    con.commit()                                                             
    return True



def run():
    
    
    con = sqlite3.connect('news.db')
    cur = con.cursor()
    model = Summarizer()
    checked = False
    while(True):
        
        
        
        curr_time = time.gmtime(time.time())
        
        if(curr_time.tm_hour == 0 and not checked):
            cur.execute('DELETE FROM news')
            con.commit()
            checked = True
            
        if(curr_time.tm_hour > 0):
            checked = False
            
        
        
        max_timestamp_in_db = cur.execute('select max(timestamp) from news').fetchone()[0]
        if(max_timestamp_in_db):
            latest_pub_timestamp = max_timestamp_in_db
        else:
            latest_pub_timestamp = 0
        
        
        
        resp = requests.get('https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms')
        
        soup = BeautifulSoup(resp.content, features="xml")
        
        items = soup.findAll('item')
        
        
        for i in reversed(range(len(items))):
            pubtime = items[i].pubDate.text
            date_time_obj = datetime.datetime.strptime(pubtime[5:25], '%d %b %Y %H:%M:%S')
            timestamp = datetime.datetime.timestamp(date_time_obj)
            
            if(timestamp > latest_pub_timestamp):
                res = addNews(items[i], timestamp, cur, con, model)
                if(not res):
                    print("Failed to add item", i)
                    continue
                latest_pub_timestamp = timestamp
                
        time.sleep(600) #poll every 600 seconds
        

if __name__ == '__main__':
    run()
    
