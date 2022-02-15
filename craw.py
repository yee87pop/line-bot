# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 19:39:29 2021

@author: eason
"""

import requests
from bs4 import BeautifulSoup

def crawler(reply):
    url="https://www.ptt.cc/bbs/"+reply+"/index.html"
    my_headers = {'cookie': 'over18=1;'}
    r = requests.get(url,headers = my_headers) #將此頁面的HTML GET下來
    soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
    sel = soup.select("div.title a") #取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel
    b=[]
    for s in sel:
        b.append(s.text)
    return str(b)
crawler("Gossiping")