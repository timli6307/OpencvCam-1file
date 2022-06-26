from collections import  deque
import numpy as np
import time
import cv2

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)

mybuffer = 16
pts = deque(maxlen=mybuffer)

lower_red_T = np.array([0, 70, 0]) 
upper_red_T = np.array([5, 255, 255])
lower_red_2 = np.array([175, 70, 0]) 
upper_red_2 = np.array([180, 255, 255])

lower_red_0 = np.array([0, 70, 0]) 
upper_red_0 = np.array([5, 255, 255])
lower_red_1 = np.array([175, 70, 0]) 
upper_red_1 = np.array([180, 255, 255])

while(True):
    ret,frame = cap.read()
    # gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    red_mask0 = cv2.inRange(hsv, lower_red_0, upper_red_0)
    red_mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    red_mask = cv2.bitwise_or(red_mask0, red_mask1) 


    red_maskR1 = cv2.inRange(frame, lower_red_T, upper_red_T)
    red_maskR2 = cv2.inRange(frame, lower_red_2, upper_red_2)
    red_maskR = cv2.bitwise_or(red_maskR1, red_maskR2)




    
    


    cv2.imshow('red mask',red_mask)
    # cv2.imshow('hsv',hsv)
    # cv2.imshow('rgb',frame)
    # if cv2.waitKey(1) & 0xFF ==ord('q'):
    #     break
    k = cv2.waitKey(1)&0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()