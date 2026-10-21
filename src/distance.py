# -*- coding: utf-8 -*-
"""
스마트 대파 화분 프로젝트 - 초음파 거리 센서(HC-SR04) 제어 모듈 (distance.py)
담당: 강민철 (팀원)
"""
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(24, GPIO.IN)


def distance(GPIO_TRIGGER=18, GPIO_ECHO=24):
    """
    HC-SR04 초음파 거리 센서를 통해 센서와 물체 사이의 거리(cm)를 측정
    - Trig: 10us 펄스 전송
    - Echo: 신호 수신 시간 측정 (음속 343m/s 적용)
    """
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.5)

    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    # 거리(cm) = (반사 시간 * 음속 34300 cm/s) / 2
    measured_distance = (TimeElapsed * 34300) / 2
    return round(measured_distance, 2)
