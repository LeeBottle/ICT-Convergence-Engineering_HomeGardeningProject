# -*- coding: utf-8 -*-
"""
스마트 대파 화분 프로젝트 - 급수 및 수분 센서 제어 모듈 (water.py)
담당: 이병한 (팀장)
"""
import RPi.GPIO as GPIO
import datetime
import time

init = False
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setwarnings(False)


def get_last_watered():
    """최근 급수한 일시를 last_watered.txt 파일에서 조회"""
    try:
        with open("last_watered.txt", "r", encoding="utf-8") as f:
            return f.readline()
    except Exception:
        return "NEVER!"


def get_status(pin=17):
    """토양 수분 센서의 디지털 입력 상태 읽기 (0: 습함, 1: 건조)"""
    GPIO.setup(pin, GPIO.IN)
    return GPIO.input(pin)


def init_output(pin):
    """지정 핀을 출력 모드로 초기화"""
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)


def auto_water(delay=5, pump_pin=22, water_sensor_pin=11):
    """
    주기적으로 토양 수분을 체크하여 건조할 경우 자동으로 펌프 가동
    """
    consecutive_water_count = 0
    init_output(pump_pin)
    print("Here we go! Press CTRL+C to exit")
    try:
        while True and consecutive_water_count < 10:
            time.sleep(delay)
            wet = (get_status(pin=water_sensor_pin) == 0)
            if not wet:
                if consecutive_water_count < 5:
                    pump_on(pump_pin, 1)
                consecutive_water_count += 1
            else:
                consecutive_water_count = 0
    except KeyboardInterrupt:
        # CTRL+C 입력 시 GPIO 리소스 정리
        GPIO.cleanup()


def pump_on(pump_pin=22, delay=1):
    """워터 펌프 릴레이를 활성화하여 1초간 급수 실행"""
    init_output(pump_pin)
    with open("last_watered.txt", "w", encoding="utf-8") as f:
        f.write("Last watered {}".format(datetime.datetime.now()))
    GPIO.output(pump_pin, 1)
    time.sleep(delay)
    GPIO.output(pump_pin, 0)
