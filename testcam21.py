from collections import  deque
import numpy as np
import cv2
import serial
from time import sleep
import sys


cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

mybuffer = 16
pts = deque(maxlen=mybuffer)

redLower = np.array([0, 43, 46])
redUpper = np.array([10, 255, 255])

blueLower = np.array([100, 43, 46])
blueUpper = np.array([124, 255, 179])

greenLower = np.array([35, 43, 46])#綠
greenUpper = np.array([77, 255, 255])

purpleLower = np.array([122, 43, 46])#紫
purpleUpper = np.array([155, 255, 255])

# q = None


while(True):
    retX,frameX = cap2.read()
    ret,frame = cap1.read()
    # gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsvX = cv2.cvtColor(frameX, cv2.COLOR_BGR2HSV)

    maskR = cv2.inRange(hsv, redLower, redUpper)#根據閾值構建掩膜
    maskR = cv2.erode(maskR, None, iterations=2)#腐蝕操作
    maskR = cv2.dilate(maskR, None, iterations=2)#膨脹操作，其實先腐蝕再膨脹的效果是開運算，去除噪點

####################
    maskRX = cv2.inRange(hsvX, redLower, redUpper)#根據閾值構建掩膜
    maskRX = cv2.erode(maskRX, None, iterations=2)#腐蝕操作
    maskRX = cv2.dilate(maskRX, None, iterations=2)#膨脹操作，其實先腐蝕再膨脹的效果是開運算，去除噪點

####################
    cnts1 = cv2.findContours(maskR.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    cnts1X = cv2.findContours(maskRX.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    center1 = None
    center2 = None
    centerX = None
    reset = (500,300)
    cv2.circle(frame, reset, 10, (0, 0, 0), -1)

    if len(cnts1 and cnts1X) != 0:
        
        c1 = max(cnts1, key = cv2.contourArea)#找到面積最大的輪廓
        c1X = max(cnts1, key = cv2.contourArea)#找到面積最大的輪廓

        M1 = cv2.moments(c1)
        M1X = cv2.moments(c1X)

        center1 = (int(M1["m10"]/M1["m00"]), int(M1["m01"]/M1["m00"]))#計算質心
        centerX = (int(M1X["m10"]/M1X["m00"]), int(M1X["m01"]/M1X["m00"]))#計算質心
        
        pointAx = int(M1["m10"]/M1["m00"])#(Ax,Ay)Redpoint
        pointAy = int(M1["m01"]/M1["m00"])

        pointBx = int(M1X["m10"]/M1X["m00"])#(Ax,Ay)Redpoint
        pointBy = int(M1X["m01"]/M1X["m00"])

        pointCx = 500
        pointCy = 300
        
        cv2.circle(frame, center1, 10, (0, 0, 255), -1)#Redpoint
        cv2.circle(frameX, centerX, 10, (255, 0, 0), -1)#Bluepoint

        # print(center1)
        




    hsv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
    cv2.imshow('cam',frame)
    cv2.imshow('another cam',frameX)
    # cv2.imshow('hsv',hsv)
    # cv2.imshow('rgb',frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
    
    k = cv2.waitKey(1)&0xFF
    if k == 27:
        break


cap1.release()
cap2.release()
cv2.destroyAllWindows()
sys.exit()
