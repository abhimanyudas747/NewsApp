# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 19:48:41 2021

@author: Abhimanyu Das
"""

import sqlite3
import uvicorn
from fastapi import FastAPI
import nest_asyncio

nest_asyncio.apply()

app = FastAPI()
@app.get("/")
def home():
    con = sqlite3.connect('news.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM news').fetchall()
    response = convert_to_json(res)
    return response

def convert_to_json(items):
    news = []
    keys = ['ID', 'TIMESTAMP', 'HEADLINE', "CONTENT", 'PUBDATE', 'IMGURL', 'LINK']
    for i in range(len(items)):
        entry = {}
        for j in range(7):
            entry[keys[j]] = items[i][j]
            
        news.append(entry)
        
    resp = {'news' : news[::-1]}
    return resp



    
def run():
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
    
if __name__ == "__main__":
    run()
