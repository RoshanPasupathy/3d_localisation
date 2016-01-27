import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import time
from LUTptrallr import bgrhsv
from LUTptrallr import cleanupf

os.system('v4l2-ctl -d 0 -c focus_auto=0')
os.system('v4l2-ctl -d 0 -c focus_absolute=0')
os.system('v4l2-ctl -d 0 -c exposure_auto=1')
os.system('v4l2-ctl -d 0 -c exposure_absolute=3')
os.system('v4l2-ctl -d 0 -c contrast=100')
os.system('v4l2-ctl -d 0 -c brightness=100')
os.system('v4l2-ctl -d 0 -c white_balance_temperature_auto=0')
os.system('v4l2-ctl -d 0 -c white_balance_temperature=6500')
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 30)
#a = cap.get(cv2.cv.CV_CAP_PROP_FPS)
b = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
c = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
print b,c
l = 1 
i = 1
colorlow = np.array([60,225,15])
colorhigh = np.array([63,255,50])
start = time.time()
while (True) & ( i < 2):
	ret,frame = cap.read()
	hsv2 = np.asarray(bgrhsv(frame,480,640))
	binary4 = cv2.inRange(hsv2,colorlow,colorhigh)
	cv2.imshow('bin',binary4)
	l +=1
#	if cv2.waitKey(1) & 0xFF == ord('c'):
#		hsv2 = np.asarray(bgrhsv(frame,480,640))
#		
#		i += 1
#		print stringval + ' taken'
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
end = time.time()
print 'time elapsed = %f s' %(end - start)
print 'frame rate = %f' %(l/(end - start))

cleanupf()
cap.release()
cv2.destroyAllWindows()
