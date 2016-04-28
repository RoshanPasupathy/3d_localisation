################## IMPORT LIBRARIES ##################
import socket
import select
import os.path
import numpy as np
import cv2
import os
import sys,traceback
# import time
from multiprocessing import Pipe,Process,Array,Value,sharedctypes
from threading import Thread
# from logging import debug, info, warn, error
from arryop import calc3d,update_c #*******************
from LUTptralltest import squarelut8
from LUTptralltest import cleanupf
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

################## CAMERA SETTINGS ##################
os.system('v4l2-ctl -d 0 -c focus_auto=0')
os.system('v4l2-ctl -d 0 -c focus_absolute=0')
os.system('v4l2-ctl -d 0 -c exposure_auto=1')
os.system('v4l2-ctl -d 0 -c exposure_absolute=3')
os.system('v4l2-ctl -d 0 -c contrast=100')
os.system('v4l2-ctl -d 0 -c brightness=100')
os.system('v4l2-ctl -d 0 -c white_balance_temperature_auto=0')
os.system('v4l2-ctl -d 0 -c white_balance_temperature=6500')
################## OBJECT DECLARATIONS ##################
port1 = 8000
port2 = 8080
#Host address
_TCP_SOCKET_HOST = "192.168.42.1"

################## FOR TESTING ##################
mtx = np.array([[  509.39049,0, 312.71212],[0,510.01682,269.33614],[0,0,1]],dtype=np.float64)
dist = np.array([0.07151,-0.15763,0.00257,-0.00169,0.0000],dtype=np.float64)
pose = np.load('/home/pi/ip/pose.npz')
rvecs = pose['rvecs']
tvecs = pose['tvecs']
R = pose['R']


Q = np.dot(mtx,R)
q = np.dot(mtx,tvecs)
Qinv = np.linalg.inv(Q)
_Qinv = -1.0 * Qinv
c = np.dot(_Qinv,q).ravel()

#rvecs = np.array([[-0.33025405],[-0.25113913],[-1.52710343]])
#tvecs = np.array([[-33.85189337],[189.50452354],[ 609.96533569]])
################## SOCKET READER CLASS ##################
class SocketReader:
    def __init__(self, sock,dat_size,pipecal):
        #create array object which is updated
        self.arr = np.array([0,0,0],dtype=np.float64)
        #create flag object which is updated
        self.flag = 1
        #create client socket object
        self.client = sock

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.running = True
        
        #pipe to send caldata
        self.pipe = pipecal
        self.read_size = dat_size


    def start(self):
        t = Thread(target=self.threadedloop,args=())
        t.daemon = True
        t.start()
        return self

    def threadedloop(self):
        """this function runs in a parallel thread"""
        #loop to update flag and arrays
        while self.running:
            # otherwise, read the next frame from the stream
            content = self.client.recv(self.read_size)
            while len(content) < (self.read_size):
                content += self.client.recv(self.read_size - len(content)) #add truncated data
                #self.trash = self.client.recv(self.dat_size - len(content))
            #if len(content) == self.dat_size:
            if (content[0] == 'u') and (content[-1] == 'l'): #valid data
                self.arr = np.fromstring(content[1:25],np.float64)#np.loads(''.join([self.encstr,content[1:self.read_size-1]))
                self.flag = 2
            elif content[0] == 'd': #invalid data
                self.flag = 1
            elif content[0] == 'c': #calibration
                self.pipe.send(np.fromstring(content[1:25],np.float64))
            elif content[0] == 'e': #loop stop
                self.flag = 0
                self.running = False
        return

    def read(self):
        return (self.flag,self.arr)

    def stop(self):
        # indicate that the thread should be stopped
        self.running = False

################## PROCESS DEFINTION ##################
def socketcomm(port,pipec, flags,uarr,dat_size = 26):
	"""Callback function to deal with incoming tcp communication.
	pipec,pipeu and pipesoc are pipe objects
	pipec: describes position of camera
	pipeu: describes orientation of camera.
		sends (True, data) for good data
		sends (False,.......) for bad data or loop not running
	pipesoc: fill socket objects and send to __main__
	"""
	#Flags
	sockets = []
	arr = np.array([0,0,0],dtype=np.float64) 
	#initialise socket object
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serversocket.bind((_TCP_SOCKET_HOST, port))
	serversocket.listen(1)
    
	#add server socket to list of sockets
	sockets.append(serversocket)
    
    #client socket creator
	clientsocket,clientaddr = serversocket.accept()
	sockets.append(clientsocket)
    
	#start thread which reads sockstream
	sockr = SocketReader(clientsocket,dat_size=dat_size,pipecal=pipec).start()
	datr = (1,arr)
	#run loop
	while datr[0]:
		datr =  sockr.read()
		with uarr.get_lock():
			uarr.get_obj()[:3] = datr[1]
		flags.value = datr[0]
	for i in sockets:
		i.close()

################## WEBCAM CLASS ##################
# uncomment for testing
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

################## SET THREAD PARAMETERS ##################
output = np.array([0,640,0,480,0,480])
#f is for function and l is for loop
#pipes for carr
pipecl1, pipecf1 = Pipe(False)
#set process
uarray1 = Array('d',3)
uflag1 = Value('B',1)

#create process instance which updates uarray1,uflag1, pipecf1 at port 8000
proc1 = Process(target=socketcomm,args=(port1,pipecf1,uflag1,uarray1))

#f is for function and l is for loop
#pipes for carr
pipecl2, pipecf2 = Pipe(False)
#set process
uarray2 = Array('d',3)
uflag2 = Value('B',1)

#create process instance which updates uarray2,uflag2, pipecf2 at port 8080
proc2 = Process(target=socketcomm,args=(port2,pipecf2,uflag2,uarray2))
reprojectx = []
reprojecty = []
reprojectz = []
################## START PROCESSES ##################
try:
	runflag = True
	proc1.start()
	#proc1 = SocketReader(port=8000,dat_size=26,pipecal=pipecf1).start()
	proc2.start()
	#proc2 = SocketReader(port=8080,dat_size=26,pipecal=pipecf2).start()
	#uncomment nextline for testing
	vs = WebcamVideoStream(src=0).start()
	
	################## BEGIN MAIN LOOP ##################
	
	print "Udating c..."
	c1 = pipecl1.recv() #Blocking
	c2 = pipecl2.recv() #Blocking
	update_c(c1,c2) #########
	
	print "Running main loop..."
	while runflag:
		dat1 = uflag1.value
		dat2 = uflag2.value
		frame = vs.read() #for testing
		if (dat1 == 2) and (dat2 ==2):
			with uarray1.get_lock():
				arr1 = np.frombuffer(uarray1.get_obj())
			with uarray2.get_lock():
				arr2 = np.frombuffer(uarray2.get_obj())
			pos3d =  calc3d(arr1,arr2)
	        #print np.asarray(pos3d)
			imgpts, jac = cv2.projectPoints(np.float32([np.asarray(pos3d)]).reshape(-1,3), rvecs, tvecs, mtx, dist)
			cv2.rectangle(frame,(int(imgpts[0,0,0]) - 2,int(imgpts[0,0,1]) - 2),(int(imgpts[0,0,0]) + 2 ,int(imgpts[0,0,1]) + 2),(255,0,0),1)
			output = squarelut8(output,480,640,10,frame[output[4]:output[5],:,:])
			if (output[0] <= output[1]) * (output[3] - output[2] < 2 * (output[1] - output[0])):
				cv2.rectangle(frame,(output[0],output[2]),(output[1],output[3]),(0,0,255),2)
				reprojectx.append(((output[0] + output[1])/2.00) - imgpts[0,0,0])
				reprojecty.append(((output[2] + output[3])/2.00) - imgpts[0,0,1])
				pos3da = np.asarray(pos3d)
				reprojectz.append(np.linalg.norm(pos3da - c))
		elif not dat1 or not dat2:
			runflag = False
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	print "Waiting for both processes to stop..."
	while uflag1.value or uflag2.value:
		continue
	
	print "Script executed without issue"

	fig1 = plt.figure(1)
	ax1 = fig1.add_subplot(111)
	ax1.grid(True)
	colours1 = cm.brg(reprojectz/max(reprojectz))
	colmap1 = cm.ScalarMappable(cmap = cm.brg)
	colmap1.set_array(reprojectz)
	
	ax1.scatter(reprojectx,reprojecty, c=colours1,marker='+')
	cb1 = fig1.colorbar(colmap1,shrink=0.75)
	ax1.set_title('Reprojection Error') 
	cb1.set_label('Distance from Camera (mm)')
	ax1.axhline(color='k',ls='--')
	ax1.axvline(color='k',ls='--')
	ax1.set_xlabel('x (pixels)')
	ax1.set_ylabel('y (pixels)')
	np.savez('/home/pi/ip/reprojerrorLED5m.npz',x=reprojectx,y=reprojecty,z=reprojectz,c=c)
	plt.show()

except:
	typ,value,tb = sys.exc_info()
	traceback.print_exception(typ,value,tb)

finally:
	print "Cleaning up......"
	cleanupf()
	print 'memory cleared'
	proc1.join()
	proc2.join()
	print 'processes clossed'
	vs.stop() #uncomment for testing
	cv2.destroyAllWindows()
	
