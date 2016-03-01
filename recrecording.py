import numpy as np
#import TCPSOCK as tcps
from TCPSOCK import Interruptor
from threading import Thread
import cv2
import os
import time

####### camera parameters #####################################
os.system('v4l2-ctl -d 0 -c focus_auto=0')
os.system('v4l2-ctl -d 0 -c focus_absolute=0')
os.system('v4l2-ctl -d 0 -c zoom_absolute=100')
os.system('v4l2-ctl -d 0 -c exposure_auto=3')
#os.system('v4l2-ctl -d 0 -c exposure_absolute=120')
os.system('v4l2-ctl -d 0 -c contrast=128')
os.system('v4l2-ctl -d 0 -c brightness=128')
os.system('v4l2-ctl -d 0 -c white_balance_temperature_auto=1')
#os.system('v4l2-ctl -d 0 -c white_balance_temperature=6500')

# Initialise class #
tcps1 = Interruptor()
#tcps2 = Interruptor()

#functions needed ##############################################
def wait_for_interrupts(classinit,threaded=False, epoll_timeout=1):
    """
    Blocking loop to listen for GPIO interrupts and distribute them to
    associated callbacks. epoll_timeout is an easy way to shutdown the
    blocking function. Per default the timeout is set to 1 second; if
    `_is_waiting_for_interrupts` is set to False the loop will exit.
    If an exception occurs while waiting for interrupts, the interrupt
    gpio interfaces will be cleaned up (/sys/class/gpio unexports). In
    this case all interrupts will be reset and you'd need to add the
    callbacks again before using `wait_for_interrupts(..)` again.
    If the argument `threaded` is True, wait_for_interrupts will be
    started in a daemon Thread. To quit it, call
    `RPIO.stop_waiting_for_interrupts()`.
    """
    if threaded:
        t = Thread(target=classinit.wait_for_interrupts, args=(epoll_timeout,))
        t.daemon = True
        t.start()
    else:
        classinit.wait_for_interrupts(epoll_timeout)

def cleanup(classinit):
    """
    Clean up by resetting all GPIO channels that have been used by this
    program to INPUT with no pullup/pulldown and no event detection. Also
    unexports the interrupt interfaces and callback bindings. You'll need
    to add the interrupt callbacks again before waiting for interrupts again.
    """
    classinit.cleanup_interrupts()
    classinit.stop_waiting_for_interrupts()
###############################################################

u1 = np.zeros((3,1),dtype=np.float64)
u2 = np.zeros((3,1),dtype=np.float64)
c1 = np.zeros((3,1),dtype=np.float64)
c2 = np.zeros((3,1),dtype=np.float64)

running1 = True
running2 = True
dat1 = False
dat2 = False
fr1 = 0
fr2 = 0
loop_count = 0

########### callbacks ######################################## 
def socket_cb1(socket,val):
    global u1,c1, running1,fr1,dat1
    if val[0] == 'u':
        u1 = np.loads(val[1:])
        fr1 += 1
        dat1 = True
    elif val[0] == 'c':
        c1 = np.loads(val[1:])
    elif val[0] == 'd':
        dat1 = False
    elif val[0] == 'e':
    	dat1 = False
        running1 = False
		
def socket_cb2(socket,val):
    global u2,c2, running2,fr2,dat2
    if val[0] == 'u':
        u2 = np.loads(val[1:])
        fr2 += 1
        dat2 = True
    elif val[0] == 'c':
        c2 = np.loads(val[1:])
    elif val[0] == 'd':
        dat2 = False
    elif val[0] == 'e':
    	dat2 = False
        running2 = False
	
##########set callbacks #####################################
tcps1.add_tcp_callback(8000,socket_cb1,threaded_callback = True)
tcps1.add_tcp_callback(8080,socket_cb2,threaded_callback = True)
wait_for_interrupts(tcps1,threaded=True)
#wait_for_interrupts(tcps2,threaded=True)

##########videostream class################################

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

#########Videorecording ####################################
#out=cv2.VideoWriter('/home/pi/video/output.avi',cv2.cv.CV_FOURCC('X','V','I','D'),25.0,(640,480))

########## camera properties ###############################

mtx = np.array([[  509.39049,0, 312.71212],[0,510.01682,269.33614],[0,0,1]],dtype=np.float64)
dist = np.array([0.07151,-0.15763,0.00257,-0.00169,0.0000],dtype=np.float64)
rvecs = np.array([[-0.33025405],[-0.25113913],[-1.52710343]])
tvecs = np.array([[-33.85189337],[189.50452354],[ 609.96533569]])

##########   main loop #####################################
vs = WebcamVideoStream(src=0).start()
#openflag = out.open('/home/pi/video/output.avi',cv2.cv.CV_FOURCC('X','V','I','D'),25.0,(640,480))
#print "Video writer running", openflag

while running1 or running2:
    frame = vs.read()
    if dat1 and dat2:
        ul1 = u1.copy()
        ul2 = u2.copy()
        m = np.cross(ul2.ravel(),ul1.ravel())
        p21 = c2.ravel() - c1.ravel()
        baseval = np.cross(p21,m)/float(np.dot(m,m))
        lmda1 = np.dot(baseval,ul2)
        lmda2 = np.dot(baseval,ul1)
        #print "lambda 1 = %f"%(lmda1)
        #print "lambda 2 = %f"%(lmda2)
        #pos1 = c1 + lmda1*ul1
        #pos2 = c2 + lmda2*ul2
        out3d =  (c1 + c2 + (lmda1*ul1) + (lmda2*ul2))/2.0 #3d output
        #print "3d position", out3d
        imgpts, jac = cv2.projectPoints(np.float32([out3d.ravel()]).reshape(-1,3), rvecs, tvecs, mtx, dist)
        #print imgpts
        cv2.rectangle(frame,(int(imgpts[0,0,0]) - 2,int(imgpts[0,0,1]) - 2),(int(imgpts[0,0,0]) + 2 ,int(imgpts[0,0,1]) + 2),(255,0,0),1)
        if (fr1 > 0) * (fr2 > 0):
        	loop_count += 1
    #writeflag = out.write(frame)
    #print "frame written",writeflag
    os.system("avconv -f video4linux2 -input_format mjpeg -i /dev/video0 /home/pi/video/output.avi")
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
    	break

print fr1
print fr2
print 'loop count',loop_count
cleanup(tcps1)
#out.release()
#cleanup(tcps2)
cv2.destroyAllWindows()
vs.stop()