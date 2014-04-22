#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Command Center
#
# Created:     20/04/2014
# Copyright:   (c) Command Center 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from numpy import*
import io
import sys, serial
import math
import time
from bge import logic
from bge import events



#cont = bge.logic.getCurrentController()
#obj = cont.owner
#sens=cont.sensors["Actuator"]


# Inputs: Data read in from IMU
#Outputs: Rotation matrices calculated from Yaw/Pitch/Roll Euler Angles
def process_data(data):

    roll=math.atan2(data[1],data[3])
    pitch=math.atan(-1*data[1]/(data[2]*math.sin(roll)+data[3]*math.cos(roll)))
    m_e=data[9]*math.sin(roll)-data[8]*math.cos(roll)
    m_n=data[7]*math.cos(pitch)+data[8]*math.sin(roll)*math.sin(pitch)+data[9]*math.cos(roll)*math.cos(pitch)
    yaw=math.atan2(m_e,m_n)
    ROT=[pitch,roll,yaw]
    return ROT



ser = serial.Serial(9,115200,timeout=None)
ser.io=io.TextIOWrapper(io.BufferedReader(ser,10),newline='\r',line_buffering=False)
#f=open('D:/GitHub/4MTrack/trackingdata2.txt','r')
i=0
# main() function
def serControl():
    try:



except:
        #f.close()
        # close
        ser.flush()
        ser.close()
        print('exit')

