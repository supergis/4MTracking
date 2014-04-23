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
import serial
import math
import time
import bge

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


def update_Data(ser,obj):
    try:
        line = ser.readline()
    except Exception as err:
        return

    line=line.strip('\r')
    data=[float(val) for val in line.split()]

    if len(data)==10:
        TransData=process_data(data)
        obj.applyRotation([TransData[0],TransData[1],TransData[2]],0)



# main() function
def serControl(cont):
    cont = bge.logic.getCurrentController()
    obj = cont.owner
    try:
        connect=obj['connect']
    except KeyError:
        serCon= serial.Serial('COM10',115200,timeout=0)
        connect=serCon.io=obj['connect']=io.TextIOWrapper(io.BufferedReader(serCon,500),newline='\r',line_buffering=False)

    update_Data(connect,obj)


def serQuit():
    print('here')
    ser.flush()
    ser.close()

