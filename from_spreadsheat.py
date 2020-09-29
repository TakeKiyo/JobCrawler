from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import MeCab
import pandas as pd

TechnologyList = ["C","C++","C#","Java","Go","Ruby","Python","JavaScript","TypeScript","React","Vue","jQuery","Rails","Django","fortran","Swift","Kotlin","React Native"]
domainList = ["バックエンド","フロントエンド","インフラ","iOS","android"]
OutputList = []

df = pd.read_csv("2020夏のITエンジニアインターンの情報が集まる魔法のスプレッドシート - 2020.csv")
idx = 0
for row in df.itertuples():     
    m = MeCab.Tagger()
    nouns = [line.split("\t")[0] for line in m.parse(str(row[3])).splitlines()]
    print(type(row[3]))
    print(row[3])
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
    OutputList.append([row[1],row[11],row[2],"",domain,"体験",tech,row[3]])
df = pd.DataFrame(OutputList,columns=["会社名","URL","タイトル","経験","技術領域","形式","言語タグ","本文"])
df.to_csv("output/spread_sheat.csv",encoding='utf_8_sig')




