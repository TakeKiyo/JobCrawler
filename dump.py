import mysql.connector
import pandas as pd 

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

experience_word = ["未経験可","Web開発経験","スマホアプリ開発経験","競プロ経験"]
technology_word  = ["C","C++","C#","Java","Go","Ruby","Python","Javascript","Typescript","React","Vue","jQuery","Rails","Django","fortran","Swift","Kotlin","React Native"]
style_word = ["実務経験","体験"]
domain_word = ["バックエンド","フロントエンド","インフラ","iOS","Android"]

file_path_list = ["output/infra.csv","output/mobile.csv","output/web.csv"]
for file in file_path_list:
    df = pd.read_csv(file)
    print(file + " start")
    cur = conn.cursor(buffered=True)
    for row in df.itertuples():
        try:
            #engineer_internsに登録
            cur.execute("INSERT INTO engineer_interns (title, content, company, entry_button_url, created, modified) values (%s, %s, %s, %s,%s,%s)",(row[4],row[9],row[2],row[3],time.strftime('%Y-%m-%d %H:%M:%S'),time.strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            cur.execute("SELECT last_insert_id() FROM gs_recruiting_item_experiences")
            engineer_intern_id = cur.fetchone()[0]

            #engineer_intern_experiencesに登録
            if type(row[5]) != float: #nanの判定
                cur.execute("INSERT INTO engineer_intern_experiences (engineer_intern_id, experience) VALUES (%s, %s)", (engineer_intern_id, experience_word.index(row[5])+1))
            
            #engineer_intern_technologies
            if type(row[8]) != float: #nanの判定
                technology_word_list = row[8].split(",")
                for item in technology_word_list:
                    cur.execute("INSERT INTO engineer_intern_technologies (engineer_intern_id, technology) VALUES (%s, %s)", (engineer_intern_id, technology_word.index(item)+1))
            
            #engineer_intern_styles
            if type(row[7]) != float: #nanの判定
                cur.execute("INSERT INTO engineer_intern_styles (engineer_intern_id, style) VALUES (%s, %s)", (engineer_intern_id, style_word.index(row[7])+1))
            
            #engineer_intern_domains
            if type(row[6]) != float: #nanの判定
                domain_word_list = row[6].split(",")
                for item in domain_word_list:
                    cur.execute("INSERT INTO engineer_intern_domains (engineer_intern_id, domain) VALUES (%s, %s)", (engineer_intern_id, domain_word.index(item)+1))

            conn.commit()
        except:
            conn.rollback()
            raise
    print(file + " done")