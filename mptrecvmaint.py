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

################## OBJECT DECLARATIONS ##################
port1 = 8000
port2 = 8080
#Host address
_TCP_SOCKET_HOST = "192.168.42.1"

################## FOR TESTING ##################
mtx = np.array([[  509.39049,0, 312.71212],[0,510.01682,269.33614],[0,0,1]],dtype=np.float64)
dist = np.array([0.07151,-0.15763,0.00257,-0.00169,0.0000],dtype=np.float64)
rvecs = np.array([[-0.33025405],[-0.25113913],[-1.52710343]])
tvecs = np.array([[-33.85189337],[189.50452354],[ 609.96533569]])
################## SOCKET READER CLASS ##################
class SocketReader:
    def __init__(self, port,dat_size,pipecal):
        #create array object which is updated
        self.arr = np.array([0,0,0],dtype=np.float64)
        #create flag object which is updated
        self.flag = 1

        #socket objects
        self.sockets = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((_TCP_SOCKET_HOST, port))
        self.server.listen(1)
        self.server.setblocking(0)
        self.sockets.append(self.server)

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        # initialize the variable used to indicate if the listening thread should
        # be stopped
        self.listening = True
        #trash collector for truncated data
        #self.trash = ''

        #self.port = port
        #pipe to send caldata
        self.pipe = pipecal
        self.dat_size = dat_size

        #register server on epoll
        self._epoll = select.epoll()
        self._epoll.register(self.server.fileno(), select.EPOLLIN)

    def start(self):
        t = Thread(target=self.threadedloop,args=())
        t.daemon = True
        t.start()
        return self

    def threadedloop(self):
        """this function runs in a parallel thread"""
        #loop to create client socket
        while self.listening:
            for fileno, event in self._epoll.poll(1):
                if fileno == self.server.fileno():
                    #create client socket
                    self.client, self.caddr = self.server.accept()
                    #Blocking client
                    self.client.setblocking(1)
                    #add client to socket list
                    self.sockets.append(self.client)
                    #unregister server from epoll list
                    self._epoll.unregister(self.server.fileno())
                    self.listening = False #exit loop once client socket created
        #loop to update flag and arrays
        while True:
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            content = self.client.recv(self.dat_size)
            while len(content) < self.dat_size:
                content += self.client.recv(self.dat_size - len(content)) #add truncated data
                #self.trash = self.client.recv(self.dat_size - len(content))
            #if len(content) == self.dat_size:
            if (content[0] == 'u') and (content[-1] == 'l'): #valid data
                self.arr = np.loads(content[1:self.dat_size-1])
                self.flag = 2
            elif content[0] == 'd': #invalid data
                self.flag = 1
            elif content[0] == 'c': #calibration
                self.pipe.send(np.loads(content[1:self.dat_size-1]))
            elif content[0] == 'e': #loop stop
                self.flag = 0
                self.stopped = True


    def read(self):
        return self.flag,self.arr

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        for i in self.sockets:
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
runflag = True
#f is for function and l is for loop
#pipes for carr
pipecl1, pipecf1 = Pipe(False)
#set process
arr1 = np.array([0,0,0],dtype=np.float64)
#uarray1 = Array('d',3)
#uarray1 = sharedctypes.synchronized(arr1)

#uflag1 = Value('B',1)
#Process(target=socketcomm,args=(port1,pipecf1,uflag1,uarray1))

#f is for function and l is for loop
#pipes for carr
pipecl2, pipecf2 = Pipe(False)
#pipes for uarr
#pipeuf2, pipeul2 = Pipe()
#pipes for socket objects
#pipesockf2, pipesockl2 = Pipe()
#set process

arr2 = np.array([0,0,0],dtype=np.float64)
#uarray2 = sharedctypes.synchronized(arr2)
#uarray2 = Array('d',3)
#uflag2 = Value('B',1)
#proc2 = Process(target=socketcomm,args=(port2,pipecf2,uflag2,uarray2))

################## START PROCESSES ##################
try:
	#proc1.start()
	proc1 = SocketReader(port=8000,dat_size=155,pipecal=pipecf1).start()
	#proc2.start()
	proc2 = SocketReader(port=8080,dat_size=155,pipecal=pipecf2).start()
	# uncomment nextline for testing
	vs = WebcamVideoStream(src=0).start()
	
	################## BEGIN MAIN LOOP ##################
	
	print "Udating c..."
	c1 = pipecl1.recv() #Blocking
	c2 = pipecl2.recv() #Blocking
	update_c(c1,c2) #########
	
	print "Running main loop..."
	while runflag:
	    flag1,arr1 = proc1.read()
	    flag2,arr2 = proc2.read()
	    # dat1 = uflag1.value
	    # dat2 = uflag2.value
	    #frame = vs.read() #for testing
	    #datrecv1 = pipeul1.recv() #Blocking
	    #datrecv2 = pipeul2.recv() #Blocking
	    #if datrecv1[0] and datrecv2[0]:
	    if (flag1 == 2) and (flag2 ==2):
	        #pos3d =  calc3d(datrecv2[2].ravel(),datrecv1[2].ravel()) ########
	        # with uarray1.get_lock():
	        #     arr1 = np.frombuffer(uarray1.get_obj())
	        # with uarray2.get_lock():
	        #     arr2 = np.frombuffer(uarray2.get_obj())
	        pos3d =  calc3d(arr1,arr2)
	        print np.asarray(pos3d)
	        #imgpts, jac = cv2.projectPoints(np.float32([np.asarray(pos3d)]).reshape(-1,3), rvecs, tvecs, mtx, dist)
	        #cv2.rectangle(frame,(int(imgpts[0,0,0]) - 2,int(imgpts[0,0,1]) - 2),(int(imgpts[0,0,0]) + 2 ,int(imgpts[0,0,1]) + 2),(255,0,0),1)
	    #elif not datrecv1[1] or not datrecv2[1]:
	    elif (flag1 == 0) or (flag2 ==0):
	        runflag = False
	    #cv2.imshow('frame',frame)
	    #if cv2.waitKey(1) & 0xFF == ord('q'):
	    #    break
	
	print "Waiting for both processes to stop..."
	#while pipeul1.poll(0.5) or pipeul2.poll(0.5):
	while (proc1.read()[0] != 0) or (proc2.read()[0] != 0):
	    continue
	
	print "Script executed without issue"

except:
	typ,value,tb = sys.exc_info()
	traceback.print_exception(typ,value,tb)

finally:
	print "Cleaning up......"
	# proc1.join()
	# proc2.join()
	proc1.stop()
	proc2.stop()
	vs.stop() #uncomment for testing
	cv2.destroyAllWindows()
	
