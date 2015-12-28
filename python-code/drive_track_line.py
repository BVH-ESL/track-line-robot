import cv2, argparse
import numpy as np
import serial
from time import sleep

max_speed = 50
min_speed = 35
max_area = 550
min_area = 250

speed_a = max_speed
speed_b = max_speed
dir_a = 0
dir_b = 0
width = 160
stop_dir = False

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

def forward():
	dir_a = 1
	dir_b = 1
	speed_a = max_speed
	speed_b = max_speed
	print "forward"
	drive_command = "("+str(speed_a*dir_a)+","+str(speed_b*dir_b)+"):"
	ser.write(drive_command)
	
def stop():
	dir_a = 0
	dir_b = 0
	speed_a = max_speed
	speed_b = max_speed
	print "stop"
	drive_command = "("+str(speed_a*dir_a)+","+str(speed_b*dir_b)+"):"
	ser.write(drive_command)
	
def left():
	dir_a = 1
	dir_b = 0
	speed_a = min_speed
	speed_b = min_speed
	print "left"
	drive_command = "("+str(speed_a*dir_a)+","+str(speed_b*dir_b)+"):"
	ser.write(drive_command)
	
def right():
	dir_a = 0
	dir_b = 1
	speed_a = min_speed
	speed_b = min_speed
	print "right"
	drive_command = "("+str(speed_a*dir_a)+","+str(speed_b*dir_b)+"):"
	ser.write(drive_command)
	
def back():
	dir_a = -1
	dir_b = -1
	speed_a = max_speed
	speed_b = max_speed
	print "back"
	drive_command = "("+str(speed_a*dir_a)+","+str(speed_b*dir_b)+"):"
	ser.write(drive_command)

def check_dir(cx1, cx2, cx3):
	area_right = 160*2/3
	area_foward = 160/3
	area_left = 0
	if (cx1 > area_right) or (cx2 > area_right) or(cx3 > area_right) :
		right()
	elif (cx1 > area_foward ) or (cx2 > area_foward) or(cx3 > area_foward) :
		forward()
	elif (cx1 > area_left) or (cx2 > area_left) or(cx3 > area_left) :
		left()
	else:
		stop()
	'''
	if (cx1 > area_right and cx2 > area_right and cx3 > area_right) or (cx1 > area_right and cx2 > area_right) or(cx1 > area_right and cx3 > area_right) or (cx2 > area_right and cx3 > area_right) :
		right()
	elif (cx1 > area_foward and cx2 > area_foward and cx3 > area_foward) or (cx1 > area_foward and cx2 > area_foward) or(cx1 > area_foward and cx3 > area_foward) or (cx2 > area_foward and cx3 > area_foward) :
		forward()
	elif (cx1 > area_left and cx2 > area_left and cx3 > area_left) or (cx1 > area_left and cx2 > area_left) or(cx1 > area_left and cx3 > area_left) or (cx2 > area_left and cx3 > area_left) :
		left()
	else:
		stop()
		'''

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
	
	roi  = image[60:80, 0:160]
	roi2 = image[80:100, 0:160]
	roi3 = image[100:120, 0:160]
	
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
		#print "a1"
		#print area
		if area > min_area and area < max_area:
			#print "len cx1" + str(len(contours))
			if moments['m00']!=0.0 :
				if moments['m01'] != 0.0:
					cx = int(moments['m10']/moments['m00'])
					cy = int(moments['m01']/moments['m00'])
					cv2.circle(image, (cx, cy+80), 2, (255, 0, 0), 0)
					cx1 = cx
					#print "a : " + str(cx)
	
	for i in contours2:
		moments = cv2.moments(i)
		area = cv2.contourArea(i)
		#print "a2"
		#print area
		#print "len cx2" + str(len(moments))
		if area > min_area and area < max_area:
			#print "len cx2" + str(len(contours2))
			if moments['m00']!=0.0 :
				if moments['m01'] != 0.0:
					cx = int(moments['m10']/moments['m00'])
					cy = int(moments['m01']/moments['m00'])
					cv2.circle(image, (cx, cy+100), 2, (0, 255, 0), 0)
					cx2 = cx
					#print "a2 : "+ str(cx)

	for i in contours3:
		moments = cv2.moments(i)
		area = cv2.contourArea(i)
		#print "a3"
		#print area
		#print "len cx3" + str(len(moments))
		if area > min_area and area < max_area:
			#print "len cx3" + str(len(contours3))
			if moments['m00']!=0.0 :
				if moments['m01'] != 0.0:
					cx = int(moments['m10']/moments['m00'])
					cy = int(moments['m01']/moments['m00'])
					cv2.circle(image, (cx, cy+120), 2, (0, 0, 255), 0)
					#print "a3 : " + str(cx)
					cx3 = cx

	
	check_dir(cx1, cx2, cx3)
	
	#drive_command = "("+str(speed_a*dir_a)+","+str(speed_b*dir_b)+"):"
	#ser.write(drive_command)
	#cv2.imshow('gray1', gray)
	#cv2.imshow('gray2', gray2)
	#cv2.imshow('gray3', gray3)
	cv2.imshow('image', image)
	#ser.write("(0,0):")
	cx1 = 0
	cx2 = 0
	cx3 = 0
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		stop()
		break
