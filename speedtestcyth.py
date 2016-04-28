import numpy as np
import cv2
import time
from LUTptralltest import squarelut8
from LUTptralltest import cleanupf
iterations = 1

img = cv2.imread('/home/pi/ip/report/readimg1.bmp')
output = np.array([0,640,0,480,0,480])

start = time.clock()
while iterations <= 300:
	output = squarelut8(output,480,640,10,img[output[4]:output[5],:,:])
	iterations += 1
timetaken = time.clock() - start

print '*' * 80
print 'Number of frames: 300'
print 'Time taken: %.4f seconds'%(timetaken)
print 'Number of frames processed per second: %.2f frames'%(300/timetaken)
print '*' * 80
cleanupf()
