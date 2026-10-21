# -*- coding: utf-8 -*-
"""
스마트 대파 화분 프로젝트 - 대파 성장 모니터링 및 IFTTT 수확 알림 스크립트 (height_check.py)
담당: 강민철 (팀원)
"""
import distance
import requests
import time

# 화분 센서 설치 기준 높이 (21cm)
BASE_HEIGHT = 21

while True:
    d = distance.distance()
    height = BASE_HEIGHT - d
    height = round(height, 2)

    # 대파 길이가 17cm를 초과하여 수확 시기가 되면 IFTTT Webhook 호출
    if height > 17:
        url = "https://maker.ifttt.com/trigger/GrownUp/with/key/d3Inb7KDfA92m5BI9FpJH8"
        try:
            re = requests.post(url)
            print("수확 알림 발송 완료: 현재 길이 {}cm (응답 코드: {})".format(height, re.status_code))
        except Exception as e:
            print("알림 발송 실패:", e)
        # 1시간 대기 후 재측정 (알림 중복 폭주 방지)
        time.sleep(3600)
    else:
        # 일반 대기 (10초)
        time.sleep(10)
