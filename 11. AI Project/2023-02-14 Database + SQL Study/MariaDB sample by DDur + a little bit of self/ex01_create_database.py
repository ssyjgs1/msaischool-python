'''작성되어 있는 CSV파일에서 데이터를 읽어와서 이를 DB로 보내는 스크립트'''
'''CRUD는 대부분의 컴퓨터 소프트웨어가 가지는 기본적인 데이터 처리 기능인 Create(생성), Read(읽기), Update(갱신), Delete(삭제)를 묶어서 일컫는 말'''

import pandas as pd
from mysql.connector import (connection)
from important_data import *

def main():
    # sql에서 실행할 query문 모음
    sql_0 = "DROP DATABASE `drone_project`;" # DROP은 데이터베이스에서 테이블(행, index, 권한 포함)을 제거한다. 테이블의 행이 제거될때, DML(데이터 조작 명령어) 트리거가 실행되지 않는다.
    sql_1 = "CREATE DATABASE `drone_project`;" # CREATE는 새로운 데이터베이스를 생성해주는 명령어
    sql_2 =f'''
        CREATE TABLE `{TABLE_CUSTOMER}` (
        `id` INT(11) UNSIGNED NOT NULL,
        `name` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
        `email` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_general_ci')
        COLLATE='utf8mb4_general_ci'
        ENGINE=InnoDB;
        '''
    sql_3 =f'''
    CREATE TABLE `{TABLE_WEBCAM}` (
        `id` INT(10) UNSIGNED NOT NULL,
        `label` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
        `num` INT(10) UNSIGNED ZEROFILL NOT NULL,
        `threshold` FLOAT UNSIGNED NOT NULL,
        `time` DATETIME NOT NULL,
        `latitude` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
        `longitude` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
        `send_email` TINYINT(3) UNSIGNED ZEROFILL NOT NULL)
    COLLATE='utf8mb4_general_ci'
    ENGINE=InnoDB;
    '''

    # MariaDB 접속을 위한 설정 부분(계정명, 비밀번호, host 주소)
    conn = connection.MySQLConnection(
        user     = USER,
        password = PASSWORD,
        host     = HOST,
    )
    cur = conn.cursor()

    # 0. Databse 삭제 (기존에 있었던 게 있으면 삭제)
    try:
        cur.execute(sql_0) # 앞서 작성한 SQL query문
    except Exception as e:
        print(e)

    # 1. Database 생성
    cur.execute(sql_1) # 앞서 작성한 SQL query문
    conn.close()

    # 2. Table 생성
    conn = connection.MySQLConnection( # MariaDB 접속을 위한 설정 및 위에서 CREATE문으로 생성한 데이터베이스 이름 지정
        user     = USER,
        password = PASSWORD,
        host     = HOST,
        database = DATABASE
    )
    cur = conn.cursor()
    cur.execute(sql_2) # 앞서 작성한 SQL query문
    cur.execute(sql_3) # 앞서 작성한 SQL query문
    conn.close()

# 실행 부분
if __name__ == '__main__':
    main()