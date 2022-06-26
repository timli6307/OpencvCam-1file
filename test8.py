from collections import  deque
import numpy as np
import cv2
import serial
from time import sleep
import sys
import os
import time
import re
upcap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
up_ret,up_frame = upcap.read()
while(1):
    gray = cv2.cvtColor(upcap, cv2.COLOR_BGR2GRAY)
    (_, cnts, _) = cv2.findContours(gray.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    clone = upcap.copy()
    cv2.drawContours(clone, cnts, -1, (0, 255, 0), 2)


upcap.release()
cv2.destroyAllWindows()
sys.exit()
