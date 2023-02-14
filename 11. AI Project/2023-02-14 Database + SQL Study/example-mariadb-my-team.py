"""HeidiSQL에 수동으로 데이터베이스(team), 테이블(webcam_taken) 만들고 데이터 형식 지정해준 다음, python 통해서 데이터 넣는 간단한 스크립트"""

from mysql.connector import (connection) # 필요한 라이브러리 import

conn = connection.MySQLConnection(
    user="ㅁㅁㅁㅁ", # MariaDB 설정할 때 만든 계정명
    password="ㅇㅇㅇㅇ", # MariaDB 설정할 때 만든 비밀번호
    host="", # MariaDB 배포되어 있는 IP주소(본인의 경우 WSL에 설치했고 Docker로 구동 중)
    port=0000, # MariaDB 설정할 때 정한 포트 번호(default=3306)
    database="ㅍㅍㅍㅍ") # HeidiSQL에서 만든 SQL database 이름(위의 예시에는 team이라는 이름)

cur = conn.cursor()
print(cur) # 연결 되어있는지 확인 --> MySQLCursor: (Nothing executed yet)

id, label, num, threshold, time, gps, flag = "", "", "", "", "", "", "" # 데이터베이스에서 테이블 내 각 row에 넣어줄 데이터 이름
sql = "" # 데이터베이스에서 돌릴 query문(=명?령어)

while True : # 데이터를 특정 조건이 발동될 때까지 계속 실행시킬 예정
    # 사용자에게서 값을 입력받게 된다
    id = input("해당 ID를 입력해주세요 : ")
    if id == "" : # Enter(=아무것도 입력하지 않음)가 눌리면 입력 중지
        break # while 반복문 종료
    label = input("해당 라벨을 입력해주세요 : ")
    num = input("해당 라벨의 번호를 입력해주세요 : ")
    threshold = input("해당 라벨의 threshold 값을 입력해주세요 : ")
    time = input("해당 개체가 탐지된 시간을 입력해주세요 : ")
    gps = input("객체가 탐지된 위치 정보를 입력해주세요 : ")
    flag = input("사용자에게 메일을 보낼지 말지를 입력해주세요 : ")
    sql = "INSERT INTO webcam_taken VALUES('"+id+"','"+label+"','"+num+"','"+threshold+"','"+time+"','"+gps+"','"+flag+"')" # SQL query문 입력
    cur.execute(sql) # SQL query문 실행

conn.commit() # 수정, 추가 등 변경사항 저장
conn.close() # 이 스크립트에서 MariaDB 접속 끝내는 부분