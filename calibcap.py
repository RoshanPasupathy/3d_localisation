import numpy as np
import cv2
import os
import time 

os.system('v4l2-ctl -d 0 -c focus_auto=0')
os.system('v4l2-ctl -d 0 -c focus_absolute=0')
os.system('v4l2-ctl -d 0 -c zoom_absolute=100')
os.system('v4l2-ctl -d 0 -c exposure_auto=3')
#os.system('v4l2-ctl -d 0 -c exposure_absolute=120')
os.system('v4l2-ctl -d 0 -c contrast=128')
os.system('v4l2-ctl -d 0 -c brightness=128')
os.system('v4l2-ctl -d 0 -c white_balance_temperature_auto=1')
#os.system('v4l2-ctl -d 0 -c white_balance_temperature=6500')
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 30)
#a = cap.get(cv2.cv.CV_CAP_PROP_FPS)
b = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
c = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
print b,c
l = 1 
i = 1
start = time.time()
while (True) & ( i < 11):
	ret,frame = cap.read()
	cv2.imshow('frame',frame)
	l +=1
	if cv2.waitKey(1) & 0xFF == ord('c'):
		if i < 6:
			stringval = '/home/pi/camera3/calibrationimages1/img' + str(i) +'.bmp'
			cv2.imwrite(stringval,frame)
			print 'img' + str(i) + ' taken and saved to camera 3 calibrationimages1'
		else:
			stringval = '/home/pi/camera3/calibrationimages2/img' + str(i-5) +'.bmp'
			cv2.imwrite(stringval,frame)
			print 'img' + str(i-5) + ' taken and saved to camera 3 calibrationimages2' 
		i += 1
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
end = time.time()
print end - start
print l/(end - start)
cap.release()
cv2.destroyAllWindows()
