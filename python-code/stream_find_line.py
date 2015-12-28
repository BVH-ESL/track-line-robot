import cv2, argparse
import numpy as np
import time

time_start = time.time()
cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

while(cam.isOpened()):
	ret, stream = cam.read()
	#print "read cam" + str(time.clock()-time_start
	#time_start = time.clolck()
	
	image = cv2.resize(stream, (160, 120), interpolation = cv2.INTER_AREA)
	#print "resize cam" + str(time.clock()-time_start
	#time_start = time.clolck()
	
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
	
	#time_start = time.time()
	contours, hiearchy = cv2.findContours(roi_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours2, hiearchy = cv2.findContours(roi_img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours3, hiearchy = cv2.findContours(roi_img3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#print "find contours cam" + str(time.time()-time_start)
	#time_start = time.time()
	
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
					#cv2.circle(image, (cx+20, cy+100), 8, (0, 255, 0), 0)
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
					#cv2.circle(image, (cx+20, cy+80), 8, (0, 255, 0), 0)
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
					#cv2.circle(image, (cx+20, cy+60), 8, (0, 255, 0), 0)
					#print "a3 : " + str(cx)
	print "final cam" + str(time.time()-time_start)
	time_start = time.time()
	
	cv2.imshow('image', image)
	#cv2.imshow('gray', gray)
	#cv2.imshow('roi_img', roi_img	)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break
