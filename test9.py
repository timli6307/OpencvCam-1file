from collections import  deque
import numpy as np
import cv2
import serial
from time import sleep
import sys
import os
import time
import re

COM_PORT = 'COM17'  # 請自行修改序列埠名稱
BAUD_RATES = 9600

ser = serial.Serial(COM_PORT, BAUD_RATES)

upcap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
sidecap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

upcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
upcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)
sidecap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
sidecap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

mybuffer = 16
pts = deque(maxlen=mybuffer)

redLower = np.array([0, 43, 46])
redUpper = np.array([10, 255, 255])

blueLower = np.array([100, 43, 46])
blueUpper = np.array([124, 255, 255])

greenLower = np.array([35, 43, 46])#綠
greenUpper = np.array([77, 255, 255])

purpleLower = np.array([122, 43, 46])#紫
purpleUpper = np.array([155, 255, 255])

whiteLower = np.array([0, 0, 46])#white
whiteUpper = np.array([180, 43, 220])

orangeLower = np.array([11, 43, 46])#orange
orangeUpper = np.array([25, 255, 255])

yellowLower = np.array([26, 43, 46])#orange
yellowUpper = np.array([34, 255, 255])

q = None


while(True):
    up_ret,up_frame = upcap.read()
    side_ret,side_frame = sidecap.read()
    # gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    up_hsv = cv2.cvtColor(up_frame, cv2.COLOR_BGR2HSV)
    side_hsv = cv2.cvtColor(side_frame, cv2.COLOR_BGR2HSV)

    mask1R = cv2.inRange(up_hsv, redLower, redUpper)
    mask1R = cv2.erode(mask1R, None, iterations=2)
    mask1R = cv2.dilate(mask1R, None, iterations=2)
    mask1Y = cv2.inRange(up_hsv, purpleLower, purpleUpper)
    mask1Y = cv2.erode(mask1Y, None, iterations=2)
    mask1Y = cv2.dilate(mask1Y, None, iterations=2)

    

    cnts_up1 = cv2.findContours(mask1R.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts_up2 = cv2.findContours(mask1Y.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    cnts_side1 = cv2.findContours(mask1R.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts_side2 = cv2.findContours(mask1Y.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    centerup_1 = None
    centerup_2 = None
    centerside_1 = None
    centerside_2 = None
    reset_up = (900,480)
    reset_side = (900,600)
    cv2.circle(up_frame, reset_up, 10, (0, 0, 255), -1)
    cv2.circle(side_frame, reset_side, 10, (0, 0, 255), -1)

    if len(cnts_up1 and cnts_up2 and cnts_side1 and cnts_side2) != 0:
        key = cv2.contourArea

        c1 = max(cnts_up1, key = cv2.contourArea)#找到面積最大的輪廓
        c2 = min(cnts_up2, key = cv2.contourArea)#找到面積最小的輪廓

        c3 = max(cnts_side1, key = cv2.contourArea)#找到面積最大的輪廓
        c4 = min(cnts_side2, key = cv2.contourArea)#找到面積最小的輪廓

        UP1 = cv2.moments(c1)
        UP2 = cv2.moments(c2)
        SIDE1 = cv2.moments(c3)
        SIDE2 = cv2.moments(c4)

        center_up_1 = (int(UP1["m10"]/UP1["m00"]), int(UP1["m01"]/UP1["m00"]))#計算質心
        center_up_2 = (int(UP2["m10"]/UP2["m00"]), int(UP2["m01"]/UP2["m00"]))#計算質心

        center_side_1 = (int(SIDE1["m10"]/SIDE1["m00"]), int(SIDE1["m01"]/SIDE1["m00"]))#計算質心
        center_side_2 = (int(SIDE2["m10"]/SIDE2["m00"]), int(SIDE2["m01"]/SIDE2["m00"]))#計算質心
        
        pointAx = int(UP1["m10"]/UP1["m00"])#(Ax,Ay)Redpoint
        pointAy = int(UP1["m01"]/UP1["m00"])
        pointBx = int(UP2["m10"]/UP2["m00"])#(Bx,By)Yellowpoint
        pointBy = int(UP2["m01"]/UP2["m00"])
        
        pointAx = int(SIDE1["m10"]/SIDE1["m00"])#(Ax,Ay)Redpoint
        pointAy = int(SIDE1["m01"]/SIDE1["m00"])
        pointBx = int(SIDE2["m10"]/SIDE2["m00"])#(Bx,By)Yellowpoint
        pointBy = int(SIDE2["m01"]/SIDE2["m00"])
        
        
        cv2.circle(up_frame, center_up_1, 10, (0, 0, 255), -1)#Redpoint
        cv2.circle(up_frame, center_up_2, 10, (255, 0, 0), -1)#Bluepoint

        cv2.circle(side_frame, center_side_1, 10, (0, 0, 255), -1)#Redpoint
        cv2.circle(side_frame, center_side_2, 10, (255, 0, 0), -1)#Bluepoint


        cv2.line(up_frame,reset_up,center_up_1,(0, 0, 255),1,4)
        cv2.line(up_frame,reset_up,center_up_2,(0, 0, 255),1,4)
        cv2.line(side_frame,reset_side,center_side_1,(0, 0, 255),1,4)
        cv2.line(side_frame,reset_side,center_side_2,(0, 0, 255),1,4)
        


    # hsv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
    cv2.imshow('UPframe',up_frame)
    cv2.imshow('sideframe',side_frame)
    # cv2.imshow('hsv',hsv)
    # cv2.imshow('rgb',frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
    
    k = cv2.waitKey(1)&0xFF
    if k == 27:
        break


ser.close()
upcap.release()
sidecap.release()
cv2.destroyAllWindows()
sys.exit()
