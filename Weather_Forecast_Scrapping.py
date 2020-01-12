from bs4 import BeautifulSoup
import urllib, csv, os, datetime, urllib.request, re, sys
import urllib.request as urllib2
from urllib.error import URLError, HTTPError

try:
	file = open(os.path.expanduser(r"Weather_Forecat_Data.csv"), "wb")
	file.write(b"Date,Mean Temperature,Max Temperature,Min Temperature,Heating Degree Days, Average Humidity, Max Humidity, Minimum Humidity, Average Wind Speed, Events"  + b"\n")
except:
	os.remove(os.path.expanduser(r"Weather_Forecat_Data.csv"))
	file = open(os.path.expanduser(r"Weather_Forecat_Data.csv"), "wb")
	file.write(b"Date,Mean Temperature,Max Temperature,Min Temperature,Heating Degree Days, Average Humidity, Max Humidity, Minimum Humidity, Average Wind Speed, Events"  + b"\n")

for vYear in range(2014,2017):
	for vMonth in range(1,13):
		for vDay in range(1,32):
			if (vYear%4 == 0):
				if (vMonth==2 and vDay>29):
					break
			else:
				if (vMonth==2 and vDay>28):
					break				
			if (vMonth in [4, 6, 9, 11] and vDay>30):
				break			

			theDate=str(vYear) + "/" + str(vMonth) + "/" + str(vDay)

			theurl="https://www.wunderground.com/history/airport/CYTZ/" + theDate +"/DailyHistory.html?hdf=1"
			#url = urllib2.urlopen(theurl)
			req = urllib.request.Request(theurl)
			try:
				urllib.request.urlopen(req)
			except HTTPError  as identifier:
				continue
			except URLError  as identifier:
				continue
			i1=urllib2.urlopen(theurl).getcode()
			print(i1)
			if urllib2.urlopen(theurl).getcode() != 11001:
				thepage = urllib.request.urlopen(theurl)
				soup=BeautifulSoup(thepage, "html.parser")
			else:
				continue 

			Max=soup.find_all('tr')[3].find_all('td')[1].find(attrs={"class":"wx-value"}).text			

			if soup.find_all('tr')[2].find_all('td')[1].text.strip()=="-":
				Mean="N/A"
			else:
				Mean=soup.find_all('tr')[2].find_all('td')[1].find(attrs={"class":"wx-value"}).text

			Min=soup.find_all('tr')[4].find_all('td')[1].find(attrs={"class":"wx-value"}).text
			HeatingDegreeDays=soup.find_all('tr')[6].find_all('td')[1].text

			if soup.find_all('tr')[7].find_all('td')[0].text=="Growing Degree Days":
				x=9
			else:
				x=8
            
			#DewPoint=soup.find_all('tr')[x].find_all('td')[1].find(attrs={"class":"wx-value"}).text
			AvgHumidity=soup.find_all('tr')[x+1].find_all('td')[1].text
			MaxHumidity=soup.find_all('tr')[x+2].find_all('td')[1].text
			MinHumidity=soup.find_all('tr')[x+3].find_all('td')[1].text
			#Percipitation=soup.find_all('tr')[x+5].find_all('td')[1].find(attrs={"class":"wx-value"}).text
			#SeaLevelPressure=soup.find_all('tr')[x+7].find_all('td')[1].find(attrs={"class":"wx-value"}).text
			AvgWindSpeed=soup.find_all('tr')[x+9].find_all('td')[1].find(attrs={"class":"wx-value"}).text
			#MaxWindSpeed1=soup.find_all('tr')[x+10].find_all('td')[1].find(attrs={"class":"wx-value"})
			#MaxWindSpeed=MaxWindSpeed1.text
			#Visibility=soup.find_all('tr')[x+12].find_all('td')[1].find(attrs={"class":"wx-value"}).text
			Events=soup.find_all('tr')[x+13].find_all('td')[1].text.strip().replace(","," ").replace('\n','').replace('\t','')

			CombinedString=theDate + ","+Mean+ ","+Max+ ","+Min+ ","+HeatingDegreeDays+ ","+AvgHumidity+ ","+MaxHumidity+ ","+MinHumidity+ ","+AvgWindSpeed+ ","+Events + "\n"
			file.write(bytes(CombinedString, encoding="ascii",errors='ignore'))

			print(CombinedString)

file.close()
