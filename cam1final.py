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

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

mybuffer = 16
pts = deque(maxlen=mybuffer)

redLower = np.array([156, 43, 46])
redUpper = np.array([180, 255, 255])

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
    ret,frame = cap.read()
    # gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    maskR = cv2.inRange(hsv, redLower, redUpper)#根據閾值構建掩膜
    maskR = cv2.erode(maskR, None, iterations=2)#腐蝕操作
    maskR = cv2.dilate(maskR, None, iterations=2)#膨脹操作，其實先腐蝕再膨脹的效果是開運算，去除噪點

    maskB = cv2.inRange(hsv, yellowLower, yellowUpper)#根據閾值構建掩膜
    maskB = cv2.erode(maskB, None, iterations=2)#腐蝕操作
    maskB = cv2.dilate(maskB, None, iterations=2)#膨脹操作，其實先腐蝕再膨脹的效果是開運算，去除噪點

    cnts1 = cv2.findContours(maskR.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts2 = cv2.findContours(maskB.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    center1 = None
    center2 = None
    center3 = None
    reset = (900,480)
    cv2.circle(frame, reset, 10, (0, 0, 255), -1)

    if len(cnts1 and cnts2) != 0:
        
        c1 = max(cnts1, key = cv2.contourArea)#找到面積最大的輪廓
        c2 = min(cnts2, key = cv2.contourArea)#找到面積最小的輪廓

        M1 = cv2.moments(c1)#計算輪廓的矩
        M2 = cv2.moments(c2)#計算輪廓的矩

        center1 = (int(M1["m10"]/M1["m00"]), int(M1["m01"]/M1["m00"]))#計算質心
        center2 = (int(M2["m10"]/M2["m00"]), int(M2["m01"]/M2["m00"]))#計算質心
        
        pointAx = int(M1["m10"]/M1["m00"])#(Ax,Ay)Redpoint
        pointAy = int(M1["m01"]/M1["m00"])
        pointBx = int(M2["m10"]/M2["m00"])#(Bx,By)Bluepoint
        pointBy = int(M2["m01"]/M2["m00"])
        pointCx = 550
        pointCy = 280
        
        cv2.circle(frame, center1, 10, (0, 0, 255), -1)#Redpoint
        cv2.circle(frame, center2, 10, (255, 0, 0), -1)#Bluepoint


        cv2.line(frame,reset,center1,(0, 0, 255),1,4)
        cv2.line(frame,reset,center2,(0, 0, 255),1,4)
        # print(center1)
        
        #點斜式
        #y=ax+b a是斜率
        # m1=(pointAy-pointCy)/(pointAx-pointCx)#RC斜率
        # print(m1)
        # m2=(pointBy-pointCy)/(pointBx-pointCx)#BC斜率
        # print(m1,m2)
        t:float=0.05
        # m1=1
        # m2=1
        # y=np.str_(int(m2*1000))
        # x=np.str_(int(m1*1000))
        # if(abs(m1)-abs(m2)>t or abs(m2)-abs(m1)>t):

        #     if(m1<m2):
        #         print(x)
                
        #         ser.write(m1)
        #         ser.write(b'\n')
        #         # sleep(0.1)
        #     else:
        #         print(y)
                
        #         ser.write(m2)
        #         ser.write(b'\n')
        #         # sleep(0.1)
        # else:
        #     ser.write(b' \n')





    hsv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
    cv2.imshow('dectect point',frame)
    # cv2.imshow('hsv',hsv)
    # cv2.imshow('rgb',frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
    
    k = cv2.waitKey(1)&0xFF
    if k == 27:
        break


ser.close()
cap.release()
cv2.destroyAllWindows()
sys.exit()
