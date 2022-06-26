from collections import  deque
import serial
from time import sleep
import sys

COM_PORT = 'COM11'  # 請自行修改序列埠名稱
BAUD_RATES = 9600
ser = serial.Serial(COM_PORT, BAUD_RATES)
w="wee"
while(True):
    ser.write(b'weee\n',)  # 訊息必須是位元組類型
    sleep(0.5)
    