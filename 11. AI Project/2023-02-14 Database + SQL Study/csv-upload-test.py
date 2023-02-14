import pandas as pd
import pymysql
import csv
# from mysql.connector import (connection)

# 기본 setting
conn = pymysql.connect(
    charset='utf8',
    user     = "ㅁㅁㅁㅁ",
    password = "ㅇㅇㅇㅇ",
    host     = "000.000.000.000",
    database = "drone_project"
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# 5. 데이터 csv, txt 파일 업로드
# CSV 파일 경로...
with open('customer.csv', 'r', encoding='utf8') as f:
    csvReader = csv.reader(f)
    next(csvReader)     # 첫줄에 row값 있을때

    # 컬럼 매핑
    for row in csvReader:
        id = (row[0])
        customer_name = (row[1])
        email = (row[2])
        print(id)
        print(customer_name)
        print(email)
        sql = "INSERT INTO customer (id, customer_name, email) VALUES (%s, %s, %s)"
        cursor.execute(sql, (id, customer_name, email))

# DB의 변화 저장
conn.commit()
f.close()
conn.close()