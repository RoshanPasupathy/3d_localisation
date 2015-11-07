import numpy as np
import cv2
import os
from LUTptr2 import squarelut5
import time

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
output = np.array([0,640,0,480])

l = 1
i = 1
start = time.time()
while (True) & ( l < 450):
	ret,frame = cap.read()
	#frame1 = frame.copy()
	output = squarelut5(output,480,640,3,frame)
	if output[0] < output[1]:
		cv2.rectangle(frame,(output[0],output[2]),(output[1],output[3]),(0,255,0),2)
		print np.asarray(output)
	else:
		print "Ball Not detected"
	l += 1
	cv2.imshow('frame',frame)
	#if cv2.waitKey(1) & 0xFF == ord('c'):
	#	stringval = 'img' + str(i) +'.bmp'
	#	cv2.imwrite(stringval,frame1)
	#	i += 1
	#	print stringval + ' taken'
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
end = time.time()
print end - start
print l/(end-start)

cap.release()
cv2.destroyAllWindows()
