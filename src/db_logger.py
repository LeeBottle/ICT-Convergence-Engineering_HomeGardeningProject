# -*- coding: utf-8 -*-
"""
스마트 대파 화분 프로젝트 - 센서 데이터 MySQL 로깅 스크립트 (db_logger.py / DB.py)
담당: 손승광 (팀원)
"""
import pymysql
import datetime
import distance
import Adafruit_DHT
import time

# MySQL 연결 설정 (DB: Plant, Table: DHT)
connect = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    db='Plant',
    charset='utf8'
)
cur = connect.cursor()
sensor = Adafruit_DHT.DHT11
DHT_PIN = 4
BASE_HEIGHT = 21

try:
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timeString = now

        # 온습도 측정 (GPIO 4)
        h, t = Adafruit_DHT.read_retry(sensor, DHT_PIN)

        # 초음파 거리 센서를 통한 식물 길이 계산
        d = distance.distance()
        height = BASE_HEIGHT - d
        height = round(height, 2)

        # DB INSERT 쿼리 실행
        sql = "INSERT INTO DHT VALUES (%s, %s, %s, %s)"
        sql_data = (t, h, height, timeString)
        cur.execute(sql, sql_data)
        connect.commit()

        print("[{}] 온도: {}°C, 습도: {}%, 높이: {}cm 기록 완료".format(timeString, t, h, height))
        time.sleep(3)
except KeyboardInterrupt:
    print("센서 로깅 종료")
finally:
    cur.close()
    connect.close()
