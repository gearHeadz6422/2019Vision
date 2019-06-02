#!/usr/bin/env python3
# import cv2
# import numpy as np
# import math
# import random
import json
import time
import sys
import cv2
import numpy as np
import math
import random
import threading
import time
from cscore import CameraServer, VideoSource
from networktables import NetworkTables
from networktables import NetworkTablesInstance

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

def processCameraStream(stream):
    coordinates = []
    avgX = 0

    ret,img = stream.read()

    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,thresh = cv2.threshold(gray,grayThresh,255,cv2.THRESH_BINARY)

    test,contours,h = cv2.findContours(thresh,1,2)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)

        if len(approx) == 4:
            x1 = approx[0][0][0]
            y1 = approx[0][0][1]
            x2 = approx[1][0][0]
            y2 = approx[1][0][1]
            x3 = approx[2][0][0]
            y3 = approx[2][0][1]
            x4 = approx[3][0][0]
            y4 = approx[3][0][1]
            
            area = abs(((x1 * y2 - y1 * x2) + (x2 * y3 - y2 * x3) + (x3 * y4 - y3 * x4) + (x4 * y1 - y4 * x1)) / 2)
            
            if area > 300:
                red = random.random() * 255
                green = random.random() * 255
                blue = random.random() * 255
                cv2.drawContours(img,[cnt],0, (red, green , blue),-1)

                coordinates.append(
                    [
                        (approx[0][0][0], approx[0][0][1]),
                        (approx[1][0][0], approx[1][0][1]),
                        (approx[2][0][0], approx[2][0][1]),
                        (approx[3][0][0], approx[3][0][1])
                    ]
                )
                
    if len(coordinates) == 1:
        avgX = ((coordinates[0][0][0] + coordinates[0][1][0] + coordinates[0][2][0] + coordinates[0][3][0])/4)

    return [len(coordinates), avgX]

# Network table setup
cond = threading.Condition()
notified = [False]
NetworkTables.initialize(server='10.64.22.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
table = NetworkTables.getTable('SmartDashboard')

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

# stream0 = cv2.VideoCapture(2)
# stream0.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
# stream0.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

# stream1 = cv2.VideoCapture(3)
# stream1.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
# stream1.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

grayThresh = 160 #float(input("Enter Minimum Grayscale Value (Integer): "))
width = 160
frameReadTimer = 0;

CameraServer.getInstance().startAutomaticCapture(name = "Front Camera", path = "/dev/video0")
CameraServer.getInstance().startAutomaticCapture(name = "Rear Camera", path = "/dev/video1")

while(True):
    pass
    # if frameReadTimer < 2:
    #     frameReadTimer += 1
    
    # else:
    #     cameraOut = processCameraStream(stream0)
    #     if cameraOut[0] == 1:
    #         table.putNumber("Front camera out", width/2 - cameraOut[1])
    #         table.putBoolean("Front camera ready", True)

    #     cameraOut = processCameraStream(stream1)
    #     if not cameraOut[0] == 0:
    #         table.putNumber("Rear camera out", width/2 - cameraOut[1])
    #         table.putBoolean("Rear camera ready", True)


cap.release()
cv2.destroyAllWindows()
