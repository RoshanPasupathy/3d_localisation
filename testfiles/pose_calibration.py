# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 19:27:52 2015

@author: Roshan
"""

import numpy as np
import cv2
import os
import time 

os.system('v4l2-ctl -d 0 -c focus_auto=0')
os.system('v4l2-ctl -d 0 -c focus_absolute=0')
os.system('v4l2-ctl -d 0 -c exposure_auto=1')
os.system('v4l2-ctl -d 0 -c exposure_absolute=250')
os.system('v4l2-ctl -d 0 -c contrast=100')
os.system('v4l2-ctl -d 0 -c brightness=128')
os.system('v4l2-ctl -d 0 -c white_balance_temperature_auto=1')
#os.system('v4l2-ctl -d 0 -c white_balance_temperature=6500')

def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img

mtx = np.array([[614.77666,0,316.92032],[0,615.67564,245.62514],[0,0,1]])
dist = np.array([0.10428,-0.18237,-0.00004,0.00167,0.00000])
		
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
objp = 26.0 * objp
axis = np.float32([[78,0,0], [0,78,0], [0,0,-78.0]]).reshape(-1,3)

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 30)
#a = cap.get(cv2.cv.CV_CAP_PROP_FPS)
b = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
c = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
print b,c
l = 0 
start = time.time()
while (True) & ( l < 1):
	ret,frame = cap.read()
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('p'):
		print "stopped"
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
		if ret == True:
			print "ret true"
			corners2 = cv2.cornerSubPix(gray,corners,(5,5),(-1,-1),criteria)
			print corners2
			print corners
			#rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)
			#imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
			#frame = draw(frame,corners2,imgpts)
			#cv2.imwrite('posecalibrate.bmp',frame)
			l = 1
			print 'image taken and saved'
		else:
			"nope"
        if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.imshow('result',frame)
end = time.time()
print end - start
print l/(end - start)
cap.release()
cv2.destroyAllWindows()