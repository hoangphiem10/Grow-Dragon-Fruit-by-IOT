import serial.tools.list_ports
# import random
import datetime
import time
import sys
from Adafruit_IO import MQTTClient, Client
import threading
AIO_FEED_IDS = ["land-moisture-sensor", "led", "light-sensor", "water-pumping-engine"]
AIO_USERNAME = "MTPQ"
AIO_KEY = "aio_FGXr42SA0z6ktdBqLEQJ32aqxV3b"

def connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_IDS:
        client.subscribe(feed)

def subscribe(client, userdata, mid, granted_qos):
    print("Subcribe thanh cong...")

def disconnected(client):
    print("Ngat ket noi...")
    sys.exit(1)


def  message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)
    if isMicrobitConnected:
        ser.write((str(payload) + "#").encode())

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    # try:
    #     if splitData[1] == "TEMP":
    #         if splitData[2]:
    #             client.publish("led", splitData[2])
    #     else:
    #         print("Invalid data. This data will be ignored\n")
    # except:
    #     print("Invalid data. This data will be ignored\n")
    #     pass

mess=""    
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end + 1:]
                
isMicrobitConnected = False
if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    isMicrobitConnected = True
    
client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

while True: 
    if isMicrobitConnected:
        readSerial()
    time.sleep(1)