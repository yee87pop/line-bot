import requests
import time
from bs4 import BeautifulSoup

def crawler(reply):
    url="https://tw.piliapp.com/time-now/tw/taipei/"
    r = requests.get(url) #將此頁面的HTML GET下來
    time.sleep(2)
    soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
    
    sel = soup.select("div.time") #取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel
    b=[]
    for s in sel:
        b.append(s.text)
    return sel
print(crawler("Gossiping"))