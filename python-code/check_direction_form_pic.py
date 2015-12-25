import cv2, argparse
import numpy as np

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
(thresh, im_bw) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

detector = cv2.SimpleBlobDetector()

keypoints = detector.detect(im_bw)
x = keypoints[0].pt[0]
y = keypoints[0].pt[1]
print x, y
image_key = cv2.drawKeypoints(image, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


while(1):
	cv2.imshow('image', image)
	#cv2.imshow('gray', gray)
	cv2.imshow('im_bw', im_bw)
	cv2.imshow('image_key', image_key)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break
