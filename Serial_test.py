#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import RPi.GPIO as GPIO
import requests
import json
import time 
import urllib.request

port = '/dev/ttyACM0'
brate = 115200 #boudrate
cmd = 'windspeed'

url_Ip = '34.64.175.201'
#-------------------------------------------------------------------------------------------#
# 통신 url 
control_Url = 'http://'+ url_Ip +':3000/control' # rows

IDS_Url = 'http://'+ url_Ip +':3000/button' # rowf

wind_Url = 'http://'+ url_Ip +':3000/wind' # rowa

auto_Url = 'http://'+ url_Ip +':3000/auto' # rowe

testtemp_Url = 'http://'+ url_Ip +':3000/testtemp' # rowd

app_Setting_Url = 'http://'+ url_Ip +':3000/setting' # rowx

data_op = '0'
data_fan = '0'
data_led = '0'
data_IDS_Up = '0'
data_IDS_Down = '0'
data_wm = '0'
data_soilhum = '0'
data_co2 = '0'
data_sun = '0'

data_set_temp = 0
data_set_co2 = 0
data_set_hum = 0
data_set_soilhum = 0
data_set_sun = 0
data_set_wind = 0
#-------------------------------------------------------------------------------------------#
# 개폐기 릴레이 컨트롤 
GPIO_IDS_Up = 20
GPIO_IDS_Down = 21
GPIO_IDS_Up2 = 12
GPIO_IDS_Down2 = 16 

# 관수모터 컨트롤 
GPIO_WATER = 22

# led 컨트롤 
GPIO_LED = 17

# 환풍기 컨트롤 
GPIO_FAN = 27


# GPIO SETUP 설정 
GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_IDS_Up, GPIO.OUT)
GPIO.setup(GPIO_IDS_Down, GPIO.OUT)
GPIO.setup(GPIO_IDS_Up2, GPIO.OUT)
GPIO.setup(GPIO_IDS_Down2, GPIO.OUT)
GPIO.setup(GPIO_WATER, GPIO.OUT)
GPIO.setup(GPIO_LED, GPIO.OUT)
GPIO.setup(GPIO_FAN, GPIO.OUT)

GPIO.output(GPIO_IDS_Up, True)
GPIO.output(GPIO_IDS_Down, True)
GPIO.output(GPIO_IDS_Up2, True)
GPIO.output(GPIO_IDS_Down2, True)
GPIO.output(GPIO_WATER, True)
GPIO.output(GPIO_LED, True)
GPIO.output(GPIO_FAN, True)
#--------------------------------------------------------------------------------------------#
# 변수 설정 
windspeed = '0'
wind_int = 0
ws_1 = 0   #  바람세기  
rain_1 = 0  #  우적센서      
IDS_1 = 0  # 개폐기값 초기화 (열림 / 닫힘)
LED_1 = 0 # LED 값 초기화 
FAN_1 = 0 # 환풍기 값 초기화
wm_1 = 0 # 워터펌프
sunShine_1 = 0 # 조도
Co2_1 = 0 # co2
soilHum_1 = 0 # 

count = 0

#--------------------------------------------------------------------------------------------#
# 어플에서 조작할수있는 변수

op = 0  # 어플내에서의 수동 / 자동 초기화


wm_manual = 0  # 우적센서 수동
led_manual = 0  # led 수동
fan_manual = 0  # 환풍기 수동
IDS_manual_Up = 0 # 개폐기 정회전 수동
IDS_manual_Down = 0 # 개폐기 역회전 수동

#--------------------------------------------------------------------------------------------#
# 모듈화

# 통신중인 값 파싱해서 받기 

#--------------------------------------------------------------------------------------------#
try:
    while True:
        try:
            req_control = urllib.request.urlopen(control_Url)
            req_IDS = urllib.request.urlopen(IDS_Url)
            req_op = urllib.request.urlopen(auto_Url)
            req_temp = urllib.request.urlopen(testtemp_Url)
            req_set = urllib.request.urlopen(app_Setting_Url)

            res_control = req_control.readline()
            res_IDS = req_IDS.readline()
            res_op = req_op.readline()
            res_temp = req_temp.readline()
            res_set = req_set.readline()

            j_control = json.loads(res_control)
            j_IDS = json.loads(res_IDS)
            j_op = json.loads(res_op)
            j_temp = json.loads(res_temp)
            j_set = json.loads(res_set)

            time.sleep(0.01)
            print('통신이 연결되었습니다')

            # 제어값 모음 control
            data_wm = j_control["rows"][0]["wm"]
            data_led = j_control["rows"][0]["led"]
            data_fan = j_control["rows"][0]["fan"]

            # 개폐기 제어 IDS
            data_IDS_Up = j_IDS["rowf"][0]["up"]
            data_IDS_Down = j_IDS["rowf"][0]["down"]

            # 자동 수동 op
            data_op = j_op["rowe"][0]["auto"]

            # 센서 모음 temp
            data_temp = j_temp["rowd"][0]["temp"]
            data_hum = j_temp["rowd"][0]["hum"]
            data_soilhum = j_temp["rowd"][0]["soilhum"]

            # 어플 세팅 값 모음
            data_set_temp = j_set["rowx"][0]["set_temp"]
            data_set_hum = j_set["rowx"][0]["set_hum"]
            data_set_wind = j_set["rowx"][0]["set_wind"]
            data_set_sun = j_set["rowx"][0]["set_sun"]
            data_set_soilhum = j_set["rowx"][0]["set_soilhum"]
            data_set_co2 = j_set["rowx"][0]["set_co2"]

            # 실시간 센서 값 모음 
            #data_co2 = 
            #data_sun
 #---------------------------------------------------------------------------------------------#
        except Exception as ex:
            print('에러가 발생 했습니다.', ex)

        if data_IDS_Up == '1':
            IDS_manual_Up = 1
        elif data_IDS_Up == '0':
            IDS_manual_Up = 0

        if data_IDS_Down == '1':
            IDS_manual_Down = 1
        elif data_IDS_Down == '0':
            IDS_manual_Down = 0
            
        if data_fan == '1':
            fan_manual = 1
        elif data_fan == '0':
            fan_manual = 0
        
        if data_led == '1':
            led_manual = 1
        elif data_led == '0':
            led_manual = 0
        
        if data_wm == '1':
            wm_manual = 1
        elif data_wm == '0':
            wm_manual = 0

        if data_op == '1':
            op = 1
        elif data_op == '0':
            op = 0
            
         #땅의 습도 체크
        if float(data_soilhum) > float(data_set_soilhum):
            soilHum_1 = 1
        elif float(data_soilhum) < float(data_set_soilhum):
            soilHum_1 = 0
         #이산화탄소 체크
        if float(data_co2) > float(data_set_co2):
            co2_1 = 1
        elif float(data_co2) < float(data_set_co2): 
            co2_1 = 0
         #조도 체크
        if float(data_sun) > float(data_set_sun):
            sunShine_1 = 1 
        elif float(data_sun) > float(data_set_sun):
            sunShine_1 = 0

    #--------------------------------------------------------------------------------------------------#
    # 개폐기 작동 알고리즘 

    # AUTO_AUTO
    # 개폐기
        if op == 1:
            if ws_1 == 1 and rain_1 == 1 and IDS_1 == 1 :
                pass
            elif ws_1 == 1 and rain_1 == 1 and IDS_1 == 0 :
                GPIO.output(GPIO_IDS_Down, False)
                GPIO.output(GPIO_IDS_Down2, False)
                IDS_1 = 1

            if ws_1 == 1 and rain_1 == 0 and IDS_1 == 1 :
                pass

            elif ws_1 == 1 and rain_1 == 0 and IDS_1 == 0 :
                GPIO.output(GPIO_IDS_Down, False)
                GPIO.output(GPIO_IDS_Down2, False)
                IDS_1 = 1

            if ws_1 == 0 and rain_1 == 1 and IDS_1 == 1 :
                pass 

            elif ws_1 == 0 and rain_1 == 1 and IDS_1 == 0 :
                GPIO.output(GPIO_IDS_Down, False)
                GPIO.output(GPIO_IDS_Down2, False)
                IDS_1 = 1
            
            if ws_1 == 0 and rain_1 == 0 and IDS_1 == 1 : 
                pass

            elif ws_1 == 0 and rain_1 == 0 and IDS_1 == 0 :
                GPIO.output(GPIO_IDS_Up, False)
                GPIO.output(GPIO_IDS_Up2, False)
                IDS_1 = 1
    #------------------------------------------------------
    # LED 
            if sunShine_1 == 0 :
                GPIO.output(GPIO_LED, True)
            elif sunShine_1 == 1 :
                GPIO.output(GPIO_LED, False)
    #------------------------------------------------------            
    # 환풍기 
            if Co2_1 == 0:
                GPIO.output(GPIO_FAN, True)
            elif Co2_1 == 1:
                GPIO.output(GPIO_FAN, False)
    #------------------------------------------------------        
    # 워터모터
            if soilHum_1 == 0:
                GPIO.output(GPIO_WATER, True)
            elif soilHum_1 == 1:
                GPIo.output(GPIO_WATER, False)
    
    # 열풍기 
            
    # Auto_manual
        if op == 0:
           #-----------------------------------------
           # 수동_개폐기
            if IDS_manual_Up == 1 and IDS_manual_Down == 0 and IDS_1 == 0:
                GPIO.output(GPIO_IDS_Up, True)
                GPIO.output(GPIO_IDS_Up2, False)
                GPIO.output(GPIO_IDS_Down, True)
                GPIO.output(GPIO_IDS_Down2, True)
            if IDS_manual_Up == 0 and IDS_manual_Down == 1 and IDS_1 == 0:
                GPIO.output(GPIO_IDS_Up, False)
                GPIO.output(GPIO_IDS_Up2, True)
                GPIO.output(GPIO_IDS_Down, False)
                GPIO.output(GPIO_IDS_Down2, False)
            if IDS_manual_Up == 0 and IDS_manual_Down == 0 and IDS_1 == 0:
                GPIO.output(GPIO_IDS_Up, False) # 3번
                GPIO.output(GPIO_IDS_Up2, True) # 1번
                GPIO.output(GPIO_IDS_Down, True) # 4번
                GPIO.output(GPIO_IDS_Down2, True) # 2번

                
           #----------------------------------------- 
           # 수동_LED
            if led_manual == 1 and LED_1 == 0:
                GPIO.output(GPIO_LED, False)

            if led_manual == 0 and LED_1 == 0:
                GPIO.output(GPIO_LED, True)
           #-----------------------------------------
           # 수동_fan
            if fan_manual ==  1 and FAN_1 == 0:
                GPIO.output(GPIO_FAN, False)

            if fan_manual ==  0 and FAN_1 == 0:
                GPIO.output(GPIO_FAN, True)
            
            # 수동_wm 
            if wm_manual == 1 and wm_1 == 0:
                GPIO.output(GPIO_WATER, False)
            
            if wm_manual == 0 and wm_1 == 0:
                GPIO.output(GPIO_WATER, True)
except KeyboardInterrupt:
    GPIO.cleanup()
    print('비상종료')
    print(KeyboardInterrupt)