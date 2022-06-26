from collections import  deque
import numpy as np
import time
import cv2

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

mybuffer = 16
pts = deque(maxlen=mybuffer)

redLower = np.array([170, 100, 100])
redUpper = np.array([179, 255, 255])

blueLower = np.array([100, 100, 170])
blueUpper = np.array([255, 255, 179])

q = None


while(True):
    ret,frame = cap.read()
    # gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    maskR = cv2.inRange(hsv, redLower, redUpper)#根據閾值構建掩膜
    maskR = cv2.erode(maskR, None, iterations=2)#腐蝕操作
    maskR = cv2.dilate(maskR, None, iterations=2)#膨脹操作，其實先腐蝕再膨脹的效果是開運算，去除噪點

    maskB = cv2.inRange(hsv, blueLower, blueUpper)#根據閾值構建掩膜
    maskB = cv2.erode(maskB, None, iterations=2)#腐蝕操作
    maskB = cv2.dilate(maskB, None, iterations=2)#膨脹操作，其實先腐蝕再膨脹的效果是開運算，去除噪點

    cnts1 = cv2.findContours(maskR.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts2 = cv2.findContours(maskB.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    center1 = None
    center2 = None
    center3 = None
    
    if len(cnts1 and cnts2) != 0:
        
        c1 = max(cnts1, key = cv2.contourArea)#找到面積最大的輪廓
        c2 = min(cnts2, key = cv2.contourArea)#找到面積最小的輪廓

        M1 = cv2.moments(c1)#計算輪廓的矩
        M2 = cv2.moments(c2)#計算輪廓的矩

        center1 = (int(M1["m10"]/M1["m00"]), int(M1["m01"]/M1["m00"]))#計算質心
        center2 = (int(M2["m10"]/M2["m00"]), int(M2["m01"]/M2["m00"]))#計算質心
        
        cv2.circle(frame, center1, 10, (0, 0, 255), -1)
        cv2.circle(frame, center2, 10, (255, 0, 0), -1)

        # print(center1)
        



    cv2.imshow('dectect point',frame)
    # cv2.imshow('hsv',hsv)
    # cv2.imshow('rgb',frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
    k = cv2.waitKey(1)&0xFF
    if k == 27:
        break



cap.release()
cv2.destroyAllWindows()

