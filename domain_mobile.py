from bs4 import BeautifulSoup
import requests
import urllib.request, urllib.error
from lxml import html
import pandas as pd
import time
allList = []

data = urllib.request.urlopen("https://www.wantedly.com/projects?type=mixed&page=1&occupation_types%5B%5D=jp__engineering&hiring_types%5B%5D=internship&fields%5B%5D=jp__mobile_engineer")

soup_parsed_data = BeautifulSoup(data, 'html.parser')
totalNum = int(soup_parsed_data.find('span',class_='total').text)
firstURL = "https://www.wantedly.com/projects?type=mixed&page="
LastURL = "&occupation_types%5B%5D=jp__engineering&hiring_types%5B%5D=internship&fields%5B%5D=jp__mobile_engineer"
for i in range(1,int((totalNum/10)+2)):
    tmpURL = firstURL + str(i) + LastURL
    data = urllib.request.urlopen(tmpURL)
    soup_parsed_data = BeautifulSoup(data, 'html.parser')
    URLList = soup_parsed_data.find_all('h1', class_='project-title')
    CompanyList = soup_parsed_data.find_all('div', class_='company-name')
    for j in range(len(URLList)):
        tmpList = []
        tmpList.append(CompanyList[j].h3.a.text)
        tmpList.append("https://www.wantedly.com/"+URLList[j].a["href"])
        tmpList.append(URLList[j].a.text)
        tmpList.append("スマホアプリ開発経験")
        tmpList.append("モバイル")
        tmpList.append("実務経験")
        allList.append(tmpList)
    time.sleep(3)
    print("取得件数: "+ str(len(allList)))
print("総取得件数: "+ str(len(allList)))
df = pd.DataFrame(allList,columns=["会社名","URL","タイトル","経験","技術領域","形式"])
df.to_csv("domain_mobile.csv")