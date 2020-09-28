from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import MeCab
import pandas as pd

TechnologyList = ["C","C++","C#","Java","Go","Ruby","Python","Javascript","Typescript","React","Vue","jQuery","Rails","Django","fortran","Swift","Kotlin","React Native"]
domainList = ["バックエンド","フロントエンド","インフラ","iOS","android"]
OutputList = []

df = pd.read_csv("domain_web.csv")
idx = 0
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
for row in df.itertuples():
    print(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])              
    if idx==0:
        idx += 1
        driver.get(row[3])
        time.sleep(1)
        driver.find_element_by_id("project-description-signin").click()
        time.sleep(1)
        driver.find_element_by_css_selector(".email-signin.login-button.new-ui-button-inverted-cleared").click()
        time.sleep(1)
        mail_input = driver.find_element_by_xpath('//*[@id="email"]')
        time.sleep(1)
        mail_input.send_keys("oldmaid138@gmail.com")
        driver.find_element_by_id("next-step-button").click()
        time.sleep(1)
        pass_input = driver.find_element_by_xpath('//*[@id="password"]')
        pass_input.send_keys("password")
        driver.find_element_by_xpath('//*[@id="next-step-button"]').click()
        time.sleep(3)
        if len(driver.find_elements_by_xpath('//*[@id="select-occupation-type"]/div[1]/span/i')) > 0:
            driver.find_element_by_xpath('//*[@id="select-occupation-type"]/div[1]/span/i').click()
        time.sleep(1)
        t = driver.find_element_by_xpath('//*[@id="project-show-body"]/div/div[1]/div/div').text
        m = MeCab.Tagger()
        nouns = [line.split("\t")[0] for line in m.parse(t).splitlines()]
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
        OutputList.append([row[2],row[3],row[4],row[5],domain,row[7],tech,t])
    else:   
        driver.get(row[3])
        if len(driver.find_elements_by_xpath('//*[@id="select-occupation-type"]/div[1]/span/i')) > 0:
            driver.find_element_by_xpath('//*[@id="select-occupation-type"]/div[1]/span/i').click()
        time.sleep(3)
        t = driver.find_element_by_xpath('//*[@id="project-show-body"]/div/div[1]/div/div').text
        m = MeCab.Tagger()
        nouns = [line.split("\t")[0] for line in m.parse(t).splitlines()]
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
        OutputList.append([row[2],row[3],row[4],row[5],domain,row[7],tech,t])
df = pd.DataFrame(OutputList,columns=["会社名","URL","タイトル","経験","技術領域","形式","言語タグ","本文"])
df.to_csv("output/web.csv",encoding='utf_8_sig')


driver.quit()


