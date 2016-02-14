import numpy as np
import cv2
import os
from LUTptralltest import squarelut8
from LUTptralltest import cleanupf
import time
from threading import Thread

os.system('v4l2-ctl -d 0 -c focus_auto=0')
os.system('v4l2-ctl -d 0 -c focus_absolute=0')
os.system('v4l2-ctl -d 0 -c exposure_auto=1')
os.system('v4l2-ctl -d 0 -c exposure_absolute=3')
os.system('v4l2-ctl -d 0 -c contrast=100')
os.system('v4l2-ctl -d 0 -c brightness=100')
os.system('v4l2-ctl -d 0 -c white_balance_temperature_auto=0')
os.system('v4l2-ctl -d 0 -c white_balance_temperature=6500')
#cap = cv2.VideoCapture(0)
#cap.set(cv2.cv.CV_CAP_PROP_FPS, 30)
#a = cap.get(cv2.cv.CV_CAP_PROP_FPS)
#b = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
#c = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
#print b,c
output = np.array([0,640,0,480,0,480])


class WebcamVideoStream:
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

vs = WebcamVideoStream(src=0).start()
l = 1
i = 1
start = time.clock()
while (True) & ( l < 400):
	#ret,frame = cap.read()
	frame = vs.read()
	output = squarelut8(output,480,640,10,frame[output[4]:output[5],:,:])
	if output[0] <= output[1]:
		#cv2.rectangle(frame,(output[0],output[2]),(output[1],output[3]),(255,0,0),2)
		print np.asarray(output)[0:4]
	else:
		print "Ball Not detected"
	l += 1
	#cv2.imshow('frame',frame)
	#if cv2.waitKey(1) & 0xFF == ord('c'):
	#	stringval = 'img' + str(i) +'.bmp'
	#	cv2.imwrite(stringval,frame1)
	#	i += 1
	#	print stringval + ' taken'
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
end = time.clock()
print 'time taken =',end - start,'seconds'
print 'frame rate =',l/(end-start)

cleanupf()
#cap.release()
cv2.destroyAllWindows()
vs.stop()
