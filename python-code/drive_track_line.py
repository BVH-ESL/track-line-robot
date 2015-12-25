import cv2, argparse
import numpy as np
import serial
from time import sleep

max_speed = 50

speed_a = max_speed
speed_b = max_speed
dir_a = 0
dir_b = 0

cx1 = 0  
cx2 = 0
cx3 = 0

drive_command = "("+str(speed_a*dir_a)+","+str(speed_b*dir_b)+"):"

ser = serial.Serial('/dev/ttyACM0', 
					baudrate = 9600,
					bytesize=serial.EIGHTBITS,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					timeout=0.1)
sleep(1.0)
while ser.read():
	pass
sleep(1.0)
ser.write("(0,0):")

cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

while(cam.isOpened()):
	ret, stream = cam.read()
	image = cv2.resize(stream, (160, 120), interpolation = cv2.INTER_AREA)
	
	roi = image[100:120, 20:140]
	roi2 = image[80:100, 20:140]
	roi3 = image[60:80, 20:140]
	
	gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	gray2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
	gray3 = cv2.cvtColor(roi3, cv2.COLOR_BGR2GRAY)
	
	ret, roi_img = cv2.threshold(gray, 75, 255, 0)
	cv2.bitwise_not(roi_img, roi_img)
	ret, roi_img2 = cv2.threshold(gray2, 75, 255, 0)
	cv2.bitwise_not(roi_img2, roi_img2)
	ret, roi_img3 = cv2.threshold(gray3, 75, 255, 0)
	cv2.bitwise_not(roi_img3, roi_img3)
	
	erodeElmt = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
	dilateElmt = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
	cv2.erode(roi_img, erodeElmt)
	cv2.dilate(roi_img, dilateElmt)
	cv2.erode(roi_img2, erodeElmt)
	cv2.dilate(roi_img2, dilateElmt)
	cv2.erode(roi_img3, erodeElmt)
	cv2.dilate(roi_img3, dilateElmt)
	
	contours, hiearchy = cv2.findContours(roi_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours2, hiearchy = cv2.findContours(roi_img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours3, hiearchy = cv2.findContours(roi_img3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#print len(contours)
	for i in contours:
		moments = cv2.moments(i)
		area = cv2.contourArea(i)
		#print area
		if area > 100 and area < 450:
			if moments['m00']!=0.0 :
				if moments['m01'] != 0.0:
					cx = int(moments['m10']/moments['m00'])
					cy = int(moments['m01']/moments['m00'])
					cv2.circle(image, (cx+20, cy+100), 8, (0, 255, 0), 0)
					cx1 = cx+20
					#print "a : " + str(cx)
	
	for i in contours2:
		moments = cv2.moments(i)
		area = cv2.contourArea(i)
		#print are
		if area > 100 and area < 450:
			if moments['m00']!=0.0 :
				if moments['m01'] != 0.0:
					cx = int(moments['m10']/moments['m00'])
					cy = int(moments['m01']/moments['m00'])
					cv2.circle(image, (cx+20, cy+80), 8, (0, 255, 0), 0)
					cx2 = cx+20
					#print "a2 : "+ str(cx)

	for i in contours3:
		moments = cv2.moments(i)
		area = cv2.contourArea(i)
		#print area
		if area > 100 and area < 450:
			if moments['m00']!=0.0 :
				if moments['m01'] != 0.0:
					cx = int(moments['m10']/moments['m00'])
					cy = int(moments['m01']/moments['m00'])
					cv2.circle(image, (cx+20, cy+60), 8, (0, 255, 0), 0)
					#print "a3 : " + str(cx)
					cx3 = cx+20

	avg_cx = (cx1+cx2+cx3)/3
	#print avg_cx
	if avg_cx == 0:
		dir_a = 0
		dir_b = 0
		print "stop"
	elif avg_cx > 80:
		dir_a = 1
		dir_b = 1
		speed_a = max_speed
		speed_b = 20
		print "left"
	elif avg_cx > 40 or avg_cx < 20:
		dir_a = 1
		dir_b = 1
		speed_a = max_speed
		speed_b = max_speed
		print "forward"
	else:
		dir_a = 1
		dir_b = 1
		speed_a = 20
		speed_b = max_speed
		print "right"
	
	drive_command = "("+str(speed_a*dir_a)+","+str(speed_b*dir_b)+"):"
	ser.write(drive_command)
	
	cv2.imshow('image', image)
	#ser.write("(0,0):")
	cx1 = 0
	cx2 = 0
	cx3 = 0
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		dir_a = 0
		dir_b = 0
		drive_command = "("+str(speed_a*dir_a)+","+str(speed_b*dir_b)+"):"
		ser.write(drive_command)
		break
