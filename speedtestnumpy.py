import numpy as np
import cv2
import time
iterations = 1

img = cv2.imread('/home/pi/ip/report/readimg1.bmp')
output = np.zeros(4)

start = time.clock()
while iterations <= 300:
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	ind = np.where((hsv[:,:,0] >= 100) * (hsv[:,:,0] <= 140) * (hsv[:,:,1] >= 20) * (hsv[:,:,2] >= 70))
	output[0] = min(ind[0])
	output[1] = max(ind[0])
	output[2] = min(ind[1])
	output[3] = max(ind[1])
	iterations += 1
timetaken = time.clock() - start

print '*' * 80
print 'Number of frames: 300'
print 'Time taken: %.4f seconds'%(timetaken)
print 'Number of frames processed per second: %.2f frames'%(300/timetaken)
print '*' * 80
