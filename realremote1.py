#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import irlib as ir
import gpioControl
import requests
import subprocess
import json
import os
import time
import RPi.GPIO as GPIO
import urllib.request


#--------------통신하는 부분 ------------------
url_b = 'http://34.64.175.201:3000/'
# ---------url 주소-------------------------
Air_url = url_b + 'remote'
Air_on_url = url_b + 'on_off'
Air_sw_url = url_b + 'strong'
Air_timer_url = url_b + 'timer'
Air_turn_url = url_b + 'turn'
Air_tempD_url = url_b + 'temp_down'
Air_tempU_url = url_b + 'temp_up'
# ------------ Device Name -----------------
AIRCON = 'Aircon'
# ------------------IR BUTTON(추가된 부분)----------------------
IR_BUTTON_FILE = "ir-codes"
hot_Air_on = 1
hot_Air_sw = 2
hot_Air_timer = 3
hot_Air_turn = 4
hot_Air_Tempdown = 5
hot_Air_TempUp = 6
# TV control 추가된 부분----------------------

#-------------통신하는 방식 --------------------
while True:
    
    u_Air_ON = urllib.request.urlopen(Air_url) 
    u_Air_ON2 = u_Air_ON.readline()
    u_Air_ON3 = json.loads(u_Air_ON2)
    time.sleep(0.5)

    u_Air_ON4 = u_Air_ON3['rowc'][0]['on_off'] 
    u_sw_ON4 = u_Air_ON3['rowc'][0]['strong'] 
    u_timer_ON4 = u_Air_ON3['rowc'][0]['timer']
    u_turn_ON4 = u_Air_ON3['rowc'][0]['turn']
    u_tempD_ON4 = u_Air_ON3['rowc'][0]['temp_down']
    u_tempU_ON4 = u_Air_ON3['rowc'][0]['temp_up']
    
    """
        u_sw_ON = urllib.request.urlopen(Air_url) 
        u_sw_ON2 = u_sw_ON.readline()
        u_sw_ON3 = json.loads(u_sw_ON2)
        time.sleep(0.5)
        u_sw_ON4 = u_sw_ON3['rowc'][0]['strong'] 

        u_timer_ON = urllib.request.urlopen(Air_url) 
        u_timer_ON2 = u_timer_ON.readline()
        u_timer_ON3 = json.loads(u_timer_ON2)
        time.sleep(0.5)
        u_timer_ON4 = u_timer_ON3['rowc'][0]['timer']

        u_turn_ON = urllib.request.urlopen(Air_url) 
        u_turn_ON2 = u_turn_ON.readline()
        u_turn_ON3 = json.loads(u_turn_ON2)
        time.sleep(0.5)
        u_turn_ON4 = u_turn_ON3['rowc'][0]['turn']

        u_turn_ON = urllib.request.urlopen(Air_url) 
        u_turn_ON2 = u_turn_ON.readline()
        u_turn_ON3 = json.loads(u_turn_ON2)
        time.sleep(0.5)
        u_turn_ON4 = u_turn_ON3['rowc'][0]['turn']
    """
    if u_Air_ON4 == '1':
        ir.sendIRSignal(IR_BUTTON_FILE, hot_Air_on)
        ON_data = {'on_off':'0'}
        enrollr = requests.put(Air_on_url, data = ON_data)

    elif u_sw_ON4 == '1':
        ir.sendIRSignal(IR_BUTTON_FILE, hot_Air_sw)
        SW_data = {'strong':'0'}
        enroll2r = requests.put(Air_sw_url, data = SW_data)

    elif u_timer_ON4 == '1':
        ir.sendIRSignal(IR_BUTTON_FILE, hot_Air_timer)
        timer_data = {'timer':'0'}
        enroll3r = requests.put(Air_timer_url, data = timer_data)

    elif u_turn_ON4 == '1':
        ir.sendIRSignal(IR_BUTTON_FILE, hot_Air_turn)
        turn_data = {'turn':'0'}
        enroll4r = requests.put(Air_turn_url, data = turn_data) 
        
    elif u_tempD_ON4 == '1':
        ir.sendIRSignal(IR_BUTTON_FILE, hot_Air_Tempdown)
        tempD_data = {'temp_down':'0'}
        enroll5r = requests.put(Air_tempD_url, data = tempD_data) 
        
    elif u_tempU_ON4 == '1':
        ir.sendIRSignal(IR_BUTTON_FILE, hot_Air_TempUp)
        tempU_data = {'temp_up':'0'}
        enroll6r = requests.put(Air_tempU_url, data = tempU_data)

        print('remote server communication')
        #elif state == False:
        # ir.sendIRSignal(IR_BUTTON_FILE, TV_UP)

        #elif state == 
            #ir.sendIRSignal(IR_BUTTON_FILE, TV_DOWN)

        #elif state == 
            #ir.sendIRSignal(IR_BUTTON_FILE, TV_OK)