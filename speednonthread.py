import numpy as np
import cv2
import os
from LUTptralltest import squarelut8
from LUTptralltest import cleanupf
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
output = np.array([0,640,0,480,0,480])
l = 1
i = 1
capture = 1 
start = time.clock()
while (True) & (l <= 500):
	ret,frame = cap.read()
	#frame1 = frame.copy()
	output = squarelut8(output,480,640,10,frame[output[4]:output[5],:,:])
	#if output[0] <= output[1]:
		#cv2.rectangle(frame1,(output[0],output[2]),(output[1],output[3]),(255,0,0),2)
		#a = np.asarray(output,dtype=np.int32)[0:4]
		#print len(a.dumps())
		


		#if cv2.waitKey(1) & 0xFF == ord('c'):
			#xcropmin = int(output[2] - (0.2*(output[2] - 0)))
			#xcropmax = int(output[3] + (0.2*(480 - output[3])))
			#ycropmin = int(output[0] - (0.2*(output[0] - 0)))
			#ycropmax = int(output[1] + (0.2*(640 - output[1])))
			#stringvaln = '/home/pi/ip/report/LED/notdetLED' + str(capture) + '.png'
			#stringvald = '/home/pi/ip/report/LED/detLED' + str(capture) + '.png' 
			#cv2.imwrite(stringvaln, frame[xcropmin:xcropmax,ycropmin:ycropmax,:])
			#cv2.imwrite(stringvald, frame1[xcropmin:xcropmax,ycropmin:ycropmax,:])
			#capture += 1
			#print ' number of images captured ', capture
	#else:
		#print "Ball Not detected"
	l += 1
	#cv2.imshow('frame',frame1)
	#if cv2.waitKey(1) & 0xFF == ord('q'):
		#break
end = time.clock()
print '*' * 80
print 'Number of frames: 500'
print 'Time taken: %.4f seconds'%(end - start)
print 'Number of frames processed per second: %.2f frames'%(500/(end-start))
print '*' * 80

cleanupf()
cap.release()
cv2.destroyAllWindows()
