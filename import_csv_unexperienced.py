import mysql.connector
import pandas as pd 
import math

# コネクションの作成
conn = mysql.connector.connect(
    host='127.0.0.1',
    port='33306',
    user='root',
    password='',
    database='gsskt'
)
conn.ping(reconnect=True)
print("接続: "+str(conn.is_connected()))

df = pd.read_csv("output/unexperienced.csv")
experience_word = ["未経験可","Web開発経験","スマホアプリ開発経験"]
technology_word  = ["C","C++","C#","Java","Go","Ruby","Python","Javascript","Typescript","React","Vue","jQuery","Rails","Django","fortran","Swift","Kotlin","React Native"]
style_word = ["実務経験","体験"]
domain_word = ["バックエンド","フロントエンド","インフラ","iOS","android"]
cur = conn.cursor(buffered=True)
for row in df.itertuples():
    try:
        #recruiting_infoに登録
        cur.execute("INSERT INTO gs_recruiting_items (name, content) VALUES (%s, %s)", (row[4],row[9]))
        conn.commit()
        cur.execute("SELECT last_insert_id() FROM gs_recruiting_item_experiences")
        gs_recruiting_item_id = cur.fetchone()[0]
        #recruiting_itemsに登録

        #gs_recruiting_item_experiencesに登録
        if type(row[5]) != float: #nanの判定
            cur.execute("INSERT INTO gs_recruiting_item_experiences (gs_recruiting_item_id, experience) VALUES (%s, %s)", (gs_recruiting_item_id, experience_word.index(row[5])))
        

        #gs_recruiting_item_technologies
        if type(row[8]) != float: #nanの判定
            technology_word_list = row[8].split(",")
            for item in technology_word_list:
                cur.execute("INSERT INTO gs_recruiting_item_technologies (gs_recruiting_item_id, technology) VALUES (%s, %s)", (gs_recruiting_item_id, technology_word.index(item)))
        
        #gs_recruiting_item_stylesに登録
        if type(row[7]) != float: #nanの判定
            cur.execute("INSERT INTO gs_recruiting_item_styles (gs_recruiting_item_id, style) VALUES (%s, %s)", (gs_recruiting_item_id, style_word.index(row[7])))
        
        #gs_recruiting_item_domainsに登録
        if type(row[6]) != float: #nanの判定
            domain_word_list = row[6].split(",")
            for item in domain_word_list:
                cur.execute("INSERT INTO gs_recruiting_item_domains (gs_recruiting_item_id, domain) VALUES (%s, %s)", (gs_recruiting_item_id, domain_word.index(item)))

        conn.commit()
    except:
        conn.rollback()
        raise