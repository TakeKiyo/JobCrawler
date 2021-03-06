from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import MeCab
import pandas as pd

TechnologyList = ["C","C++","C#","Java","Go","Ruby","Python","JavaScript","TypeScript","React","Vue","jQuery","Rails","Django","fortran","Swift","Kotlin","React Native","Docker","Kubernetes"]
domainList = ["サーバー","フロント","インフラ","iOS","Android","Web"]
OutputList = []

df = pd.read_csv("2020夏のITエンジニアインターンの情報が集まる魔法のスプレッドシート - 2020.csv")
idx = 0
for row in df.itertuples():    
    if idx != 0:
        m = MeCab.Tagger()
        nouns = [line.split("\t")[0] for line in m.parse(str(row[3])).splitlines()]
        commonDomain = list(set(nouns) & set(domainList))
        domain=""
        if len(commonDomain)!=0:
            for i in range(len(commonDomain)):
                if i != 0:
                    domain += ","
                domain += str(commonDomain[i])
        commonTech = list(set(nouns) & set(TechnologyList))
        tech = ""
        if len(commonTech) != 0:
            for i in range(len(commonTech)):
                if i != 0:
                    tech += ","
                tech += str(commonTech[i])
        OutputList.append([row[1],row[11],row[2],"",domain,"体験",tech,row[3],row[8]])
    idx += 1
df = pd.DataFrame(OutputList,columns=["会社名","URL","タイトル","経験","技術領域","形式","言語タグ","本文","応募締切"])
df.to_csv("output/spread_sheet.csv",encoding='utf_8_sig')




