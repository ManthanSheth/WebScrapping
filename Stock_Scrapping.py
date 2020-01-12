import requests
from bs4 import BeautifulSoup
import urllib, csv, os, datetime, urllib.request, re, sys
import urllib.request as urllib2
from urllib.error import URLError, HTTPError
start1=1417372200
end1=1419964200
diff=86400
l = []
Dict = {}

for vYear in range(2015,2016):
    monthrange=1
    range1=0
    range2=0
    for vMonth in range(1,13):
        if(vMonth==1):
            range1=31
            range2=29
        elif (vMonth==2):
            if(vYear%4 == 0):
                range1=29
                range2=31
            else:
                range1=28
                range2=31
        elif(vMonth==3):
            range1=31
            range2=30
        elif(vMonth==4):
            range1=30
            range2=31
        elif(vMonth==5):
            range1=31
            range2=30
        elif(vMonth==6):
            range1=30
            range2=31
        elif(vMonth==7):
            range1=31
            range2=31
        elif(vMonth==8):
            range1=31
            range2=30
        elif(vMonth==9):
            range1=30
            range2=31
        elif(vMonth==10):
            range1=31
            range2=30
        elif(vMonth==11):
            range1=30
            range2=31
        elif(vMonth==12):
            range1=31
        for vDay in range(1,range1):                    
            theDate=str(vYear) + "/" + str(vMonth) + "/" + str(vDay)
            if(vMonth!=12):
                start1=start1+diff
                date1=theDate+"    "+str(start1)
                #print(date1)
        for vDay in range(1,range2):
            end1=end1+diff
        strings1=str(start1)+"  "+str(end1)            
        url1="https://ca.finance.yahoo.com/quote/AAPL/history?period1="+str(start1)+"&period2="+str(end1)+"&interval=1d&filter=history&frequency=1d"
        req = urllib.request.Request(url1)
        try:
            urllib.request.urlopen(req)
        except HTTPError  as identifier:
            continue
        except URLError  as identifier:
            continue
        i1=urllib2.urlopen(url1).getcode()
        print(i1)
        if urllib2.urlopen(url1).getcode() != 11001:
            print(strings1) 
            page = requests.get(url1)
            content = page.content
            soup = BeautifulSoup(content, "html.parser")
        else:
            continue

        all = soup.find("div", {"class": "Pb(10px) Ovx(a) W(100%)"}).find("span").text
        table = soup.find_all("table", {"class": "W(100%) M(0)"})
        jj=0
        for items in table:
           for i in range(len(items.find_all("tr")) - 1):
               d = {}
               try:
                   items.find_all("td", {"class": "Py(10px) Ta(start) Pend(10px)"})[i].text
                   d["date"] = items.find_all("td", {"class": "Py(10px) Ta(start) Pend(10px)"})[i].text
                   aa= items.find_all("td", {"class": "Py(10px) Pstart(10px)"})[jj+0].text
                   d["open"] =aa
                   aa2=items.find_all("td", {"class": "Py(10px) Pstart(10px)"})[jj+1].text
                   d["High"] = aa2
                   aa3=items.find_all("td", {"class": "Py(10px) Pstart(10px)"})[jj+2].text
                   d["Law"] = aa3
                   aa4=items.find_all("td", {"class": "Py(10px) Pstart(10px)"})[jj+3].text
                   d["Close"] = aa4
                   aa5= items.find_all("td", {"class": "Py(10px) Pstart(10px)"})[jj+4].text
                   d["Adj close"]=aa5 
                   aa6= items.find_all("td", {"class": "Py(10px) Pstart(10px)"})[jj+5].text
                   d["Volume"] =aa6
                   jj=jj+6

               except:
                   d["date"] = "None"
                   d["open"] = "None"
                   d["High"] = "None"
                   d["Law"] = "None"
                   d["Close"] = "None"
                   d["Adj close"] = "None"
                   d["Volume"] = "None"
                   # print("")
               l.append(d)

import pandas

dataFrame = pandas.DataFrame(l)
print(dataFrame)
dataFrame.to_csv("D:\Mtech\Scraping\stocks1.csv")
