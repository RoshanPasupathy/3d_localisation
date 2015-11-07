import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import time
from LUTptr2 import bgrhsvarray2 

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
i = 0
xaxis = np.arange(0,256,1)
hueaxis = np.zeros(256)
saturationaxis = np.zeros(256)
valueaxis = np.zeros(256)
roi = np.array([[80,180,160,260],[40,140,100,200],[370,440,530,600],[150,230,300,380]])

start = time.time()
while (True) & ( i < 4):
	ret,frame = cap.read()
	l +=1
	cv2.rectangle(frame,(roi[i,2],roi[i,0]),(roi[i,3],roi[i,1]),(0,0,255),2)
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('c'):
		filteraxis = np.asarray(bgrhsvarray2(frame,roi[i,0],roi[i,1],roi[i,2],roi[i,3]))
		hueaxis += filteraxis[0,:]
		saturationaxis += filteraxis[1,:]
		valueaxis += filteraxis[2,:]
#		stringval = 'img' + str(i) +'.bmp'
#		cv2.imwrite(stringval,frame)
		i += 1
#		print stringval + ' taken'
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


sortedh = np.sort(hueaxis)
huevals = np.array(np.where(hueaxis >= sortedh[-3])).tolist() #list with double bracket
print 'hue values of ball =  %s. Please refer to plot' %(', '.join(str(it) for it in huevals[0]))
plt.figure(0)
plt.plot(xaxis,hueaxis,'ro')
plt.ylabel('Hue')

plt.figure(1)
plt.plot(xaxis,saturationaxis,'bo')
plt.ylabel('Saturation')

plt.figure(2)
plt.plot(xaxis,valueaxis,'go')
plt.ylabel('Value')

plt.show()
end = time.time()
print 'time elapsed = %f s' %(end - start)
print 'frame rate = %f' %(l/(end - start))
cap.release()
cv2.destroyAllWindows()
