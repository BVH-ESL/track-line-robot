import cv2, argparse
import numpy as np

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
roi = image[60:80, 0:100]
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
ret, roi_img = cv2.threshold(gray, 75, 255, 0)
cv2.bitwise_not(roi_img, roi_img)
erodeElmt = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
dilateElmt = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
#cv2.erode(roi_img, erodeElmt)
cv2.dilate(roi_img, dilateElmt)
contours, hiearchy = cv2.findContours(roi_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for i in contours:
	moments = cv2.moments(i)
	
	if moments['m00']!=0.0 :
		if moments['m01'] != 0.0:
			cx = int(moments['m10']/moments['m00'])
			cy = int(moments['m01']/moments['m00'])
			cv2.circle(image, (cx, cy+60), 8, (0, 255, 0), 0)
			print cx
while(1):
	cv2.imshow('image', image)
	cv2.imshow('gray', gray)
	cv2.imshow('roi_img', roi_img	)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break
