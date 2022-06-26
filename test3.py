from collections import  deque
import numpy as np
import time
import cv2

redLower = np.array([200, 0, 0])
redUpper = np.array([210, 255, 255])

redLower = np.array([170, 100, 100])
redUpper = np.array([179, 255, 255])
#初始化追蹤點的列表
mybuffer = 16
pts = deque(maxlen=mybuffer)
counter = 0

camera = cv2.VideoCapture(1)



while True:
    #讀取幀
    (ret, frame) = camera.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, redLower, redUpper)#根據閾值構建掩膜
    mask = cv2.erode(mask, None, iterations=2)#腐蝕操作
    mask = cv2.dilate(mask, None, iterations=2)#膨脹操作，其實先腐蝕再膨脹的效果是開運算，去除噪點
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    #初始化瓶蓋圓形輪廓質心
    center = None
    #如果存在輪廓
    if len(cnts) > 0:
        
        c = max(cnts, key = cv2.contourArea)#找到面積最大的輪廓
        ((x, y), radius) = cv2.minEnclosingCircle(c)#確定面積最大的輪廓的外接圓
        M = cv2.moments(c)#計算輪廓的矩
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))#計算質心
        #只有當半徑大於10時，才執行畫圖
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #把質心新增到pts中，並且是新增到列表左側
            pts.appendleft(center)

    else:#如果影象中沒有檢測到瓶蓋，則清空pts，影象上不顯示軌跡。
        pts.clear()
    
    
            
    cv2.imshow('Frame', frame)
    #鍵盤檢測，檢測到esc鍵退出
    k = cv2.waitKey(1)&0xFF
    counter += 1
    if k == 27:
        break
#攝像頭釋放
camera.release()
#銷燬所有視窗
cv2.destroyAllWindows()