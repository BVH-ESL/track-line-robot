#!/usr/bin/env python

import cv2, time, os
import serial

start_time = time.time()
current_time = time.time()
path = "bvh-github/track-line-robot/drive_pic_4_find_line/"
path += time.ctime()
os.makedirs(path)

speed_a = 75
speed_b = 75
ser = serial.Serial('/dev/ttyACM0', 
					baudrate = 9600,
					bytesize=serial.EIGHTBITS,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					timeout=0.1)
					
dir_a = 1
dir_b = 1
drive_command = "("+str(speed_a*dir_a)+","+str(speed_b*dir_b)+"):"

time.sleep(1.0)
while ser.read():
	pass
	
ser.write(drive_command)

print drive_command
#cv2.namedWindow("lll")
i = 0
cam = cv2.VideoCapture(0)

while( cam.isOpened() ) :
	ser.write(drive_command)
	ret,img = cam.read()
	dim = (100, 100) #width, high
	resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
	cv2.imshow("lll",resized)
	
	if time.time()-start_time > 15:
		dir_a = 0
		dir_b = 0
		drive_command = "("+str(speed_a*dir_a)+","+str(speed_b*dir_b)+"):"
		ser.write(drive_command)
		break
	elif time.time()-current_time > 1: 
		#print time.ctime()
		name = time.ctime()+".jpg"
		#print name
		cv2.imwrite(path+"/"+name, resized)
		current_time = time.time()
