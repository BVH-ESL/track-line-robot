#!/usr/bin/env python

import cv2, time, os
import serial

#cv2.namedWindow("lll")
i = 0
cam = cv2.VideoCapture(0)
while( cam.isOpened() ) :
    ret,img = cam.read()
    dim = (400, 300) #width, high
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow("lll",resized)

    #cv2.waitKey(0)
    #print "hey"
    k = cv2.waitKey(5) & 0xFF
    if k == 120: #press x to exit
        break
    if k == 121: #press spacebar to save file
        print time.time()
        cv2.imwrite('{0:04d}cam.png'.format(i), resized)
        i += 1	
