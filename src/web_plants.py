# -*- coding: utf-8 -*-
"""
스마트 대파 화분 프로젝트 - Flask 모니터링 & 원격 제어 웹 서버 (web_plants.py)
담당: 이병한 (팀장)
"""
from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import water
import os
import time
import distance
import Adafruit_DHT
import requests
import pymysql

sensor = Adafruit_DHT.DHT11
DHT_PIN = 4
BASE_HEIGHT = 21

app = Flask(__name__)


def template(title="HELLO!", text=""):
    """웹 페이지 렌더링에 필요한 센서 데이터 및 상태 딕셔너리 구성"""
    now = datetime.datetime.now()
    h, t = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    timeString = now.strftime('%Y-%m-%d %H:%M:%S')

    d = distance.distance()
    height = BASE_HEIGHT - d
    height = round(height, 2)

    templateData = {
        'title': title,
        'time': timeString,
        'text': text,
        'temp': t,
        'humi': h,
        'height': height
    }
    return templateData


@app.route("/")
def hello():
    """메인 대시보드 화면"""
    templateData = template()
    return render_template('main.html', **templateData)


@app.route("/last_watered")
def check_last_watered():
    """마지막 급수 일시 조회"""
    templateData = template(text=water.get_last_watered())
    return render_template('main.html', **templateData)


@app.route("/sensor")
def action():
    """토양 수분 센서 상태 확인"""
    status = water.get_status(17)
    if status == 1:
        message = "Water me please!"
    elif status == 0:
        message = "I'm a happy plant"
    else:
        message = "NOT CONNECT"
    templateData = template(text=message)
    return render_template('main.html', **templateData)


@app.route("/water")
def action2():
    """원격 수동 1회 급수 (펌프 1초 가동)"""
    water.pump_on()
    templateData = template(text="Watered Once")
    return render_template('main.html', **templateData)


@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    """자동 급수 백그라운드 프로세스 (auto_water.py) ON/OFF 토글"""
    running = False
    if toggle == "ON":
        templateData = template(text="Auto Watering On")
        for process in psutil.process_iter():
            try:
                if len(process.cmdline()) > 1 and process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text="Already running")
                    running = True
                    break
            except Exception:
                pass
        if not running:
            os.system("python3 auto_water.py &")
    else:
        templateData = template(text="Auto Watering Off")
        os.system("pkill -f water.py")
        os.system("pkill -f auto_water.py")
    return render_template('main.html', **templateData)


@app.route("/db")
def savestatus():
    """DB에 적재된 센서 데이터를 텍스트 파일(Plant.txt)로 내보내기"""
    try:
        connect = pymysql.connect(
            host='localhost',
            user='root',
            password='1234',
            db='Plant',
            charset='utf8'
        )
        cur = connect.cursor()
        with open("Plant.txt", 'w', encoding='utf-8') as f:
            sql = "SELECT * FROM DHT"
            cur.execute(sql)
            result = cur.fetchall()
            for row_data in result:
                h = str(row_data[2])
                data = "{},{},{},{}\n".format(row_data[0], row_data[1], h, row_data[3])
                f.write(data)
        cur.close()
        connect.close()
        templateData = template(text="DB Data Saved to Plant.txt")
    except Exception as e:
        templateData = template(text="DB Export Failed: " + str(e))
    return render_template('main.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
