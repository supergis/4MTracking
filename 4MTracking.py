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
import bge


cont = bge.logic.getCurrentController()
obj = cont.owner
sens=cont.sensors["Actuator"]


# Inputs: Data read in from IMU
#Outputs: Rotation matrices calculated from Yaw/Pitch/Roll Euler Angles
def process_data(data):

    roll=math.atan2(data[1],data[3])
    pitch=math.atan(-1*data[1]/(data[2]*math.sin(roll)+data[3]*math.cos(roll)))
    m_e=data[9]*math.sin(roll)-data[8]*math.cos(roll)
    m_n=data[7]*math.cos(pitch)+data[8]*math.sin(roll)*math.sin(pitch)+data[9]*math.cos(roll)*math.cos(pitch)
    yaw=math.atan2(m_e,m_n)
    #rot_D=matrix([[math.cos(yaw),math.sin(yaw),0],[-1*math.sin(yaw),math.cos(yaw),0],[0,0,1]])
    #rot_C=matrix([[1,0,0],[0,math.cos(pitch),math.sin(pitch)],[0,-1*math.sin(pitch),math.cos(pitch)]])
    #rot_B=matrix([[math.cos(roll),math.sin(roll),0],[-1*math.sin(roll),math.cos(roll),0],[0,0,1]])
    #ROT2=rot_B*rot_C
    #ROT=ROT2*rot_D
    ROT=[pitch,roll,yaw]
    return ROT



ser = serial.Serial(9,115200,timeout=None)
ser.io=io.TextIOWrapper(io.BufferedReader(ser,10),newline='\r',line_buffering=False)
#f=open('D:/GitHub/4MTrack/trackingdata2.txt','r')
i=0
# main() function
def serControl():

    try:
        if i==0:
            rotation=obj.worldOrientation.to_euler()
            #print(rotation)
            #print('here')
            # read each line from serial
            line = ser.io.readline()
            #line=f.readline()
            #check the length of the line (number of columns) should be fixed
            # split() returns a list of all words in a string, so here it
            # returns each value in line. float(val) turns each value into a
            # floating point
            data = [float(val) for val in line.split()]
            #print(len(data))
            if len(data)==10:
                #Transform data through transformation matrices
                #data=data-base_data
                TransData=process_data(data)
                #currentRot=motionAct.dRot
                #print(currentRot)
                #print(currentRot)
                #calib=currentRot-TransData
                #print(TransData)
                #Update Blender Model
                #print(TransData)
                obj.applyRotation([TransData[0],TransData[1],TransData[2]],0)
                #print('here2')
                #cont.deactivate("Motion")
                #print('here3')

            else:
                ser.close()
                ser.close()

    except:
        #f.close()
        # close
        ser.flush()
        ser.close()
        print('exit')

        #break



def serQuit():
    ser.flush()
    ser.close()

  # close
  #f.flush()
  #f.close()

  #ser.flush()
  #ser.close()

# call main
#if __name__ == '__main__':
#  main()


