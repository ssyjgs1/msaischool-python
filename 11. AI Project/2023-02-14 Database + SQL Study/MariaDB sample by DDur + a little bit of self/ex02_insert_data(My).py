'''ex01_create_database.py에서 실행하여 생성된 데이터베이스에 csv파일을 읽어와서 데이터를 입력하고 전송하는 스크립트'''

import pandas as pd
from mysql.connector import (connection)
import csv

# 1. data 추가 - csv 파일 읽어오기
f = open(r'customer.csv')
csvreader = csv.reader(f)
next(csvreader)

conn = connection.MySQLConnection( # MariaDB 접속을 위한 설정 및 위에서 CREATE문으로 생성한 데이터베이스 이름 지정
        user     = "ㅁㅁㅁㅁ",
        password = "ㅁㅁㅁㅁ",
        host     = "000.000.000.000",
        database = "drone_project"
    )
cur = conn.cursor(prepared=True)

for row in csvreader :
    id = row[0]
    customer_name = row[1]
    email = row[2]
    sql = "INSERT INTO customer (id, customer_name, email) values (%s, %s, %s)"
    # sql = f"""INSERT INTO customer (id, customer_name, email) values ({id}, {customer_name}, {email})"""
    cur.execute(sql, (id, customer_name, email))

conn.commit() # 데이터베이스에 들어간 변경사항 저장
f.close()
conn.close()