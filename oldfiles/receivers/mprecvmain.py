################## IMPORT LIBRARIES ##################
import socket
import select
import os.path
import numpy as np
import cv2
import os
# import time
from multiprocessing import Pipe,Process
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

################## FUNCTION DEFINITIONS ##################

def socketcomm(port,pipec, pipeu,dat_size = 156):
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
	waiting_for_data = True
	#initialise socket object
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serversocket.bind((_TCP_SOCKET_HOST, port))
	serversocket.listen(1)
	serversocket.setblocking(0)
	#add server socket to list of sockets
	sockets.append(serversocket)
	#create epoll object
	_epoll = select.epoll()
	#register interest in read events on the server socket
	_epoll.register(serversocket.fileno(), select.EPOLLIN)

	while waiting_for_data:
		events = _epoll.poll(1)
		for fileno, event in events:
			if fileno == serversocket.fileno():
				#initialise client socket object
				clientsocket,clientaddr = serversocket.accept()
				clientsocket.setblocking(0)
				#register client socket on epoll
				_epoll.register(clientsocket.fileno(),select.EPOLLIN)
				sockets.append(clientsocket)
			elif event & select.EPOLLIN:
				#read event  on client socket
				content = clientsocket.recv(dat_size)
				if content[0] == 'u':
					pipeu.send((True,np.loads(content[1:])))
				elif content[0] == 'd':
					pipeu.send((False,True))
				elif content[0] == 'c':
					pipec.send(np.loads(content[1:]))
				elif content[0] == 'e':
					pipeu.send((False,False))
					waiting_for_data = False
					for i in sockets:
						_epoll.unregister(i.fileno())
			elif event & select.EPOLLHUP:
				for i in sockets:
					_epoll.unregister(i.fileno())
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

################## SET PROCESSES ##################
runflag = True
#f is for function and l is for loop
#pipes for carr
pipecf1, pipecl1 = Pipe()
#pipes for uarr
pipeuf1, pipeul1 = Pipe()
#pipes for socket objects
#pipesockf1, pipesockl1 = Pipe()
#set process
proc1 = Process(target=socketcomm,args=(port1,pipecf1,pipeuf1))

#f is for function and l is for loop
#pipes for carr
pipecf2, pipecl2 = Pipe()
#pipes for uarr
pipeuf2, pipeul2 = Pipe()
#pipes for socket objects
#pipesockf2, pipesockl2 = Pipe()
#set process
proc2 = Process(target=socketcomm,args=(port2,pipecf2,pipeuf2))

################## START PROCESSES ##################

proc1.start()
proc2.start()
# uncomment nextline for testing
vs = WebcamVideoStream(src=0).start()

################## BEGIN MAIN LOOP ##################

try:
	c1 = pipecl1.recv() #Blocking
	c2 = pipecl2.recv() #Blocking
	update_c(c1.ravel(),c2.ravel()) #########

	while runflag:
		frame = vs.read() #for testing
		datrecv1 = pipeul1.recv() #Blocking
		datrecv2 = pipeul2.recv() #Blocking
		if datrecv1[0] and datrecv2[0]:
			pos3d =  retfunc(datrecv2[1].ravel(),datrecv1[1].ravel()) ########
			imgpts, jac = cv2.projectPoints(np.float32([np.asarray(pos3d)]).reshape(-1,3), rvecs, tvecs, mtx, dist)
			cv2.rectangle(frame,(int(imgpts[0,0,0]) - 2,int(imgpts[0,0,1]) - 2),(int(imgpts[0,0,0]) + 2 ,int(imgpts[0,0,1]) + 2),(255,0,0),1)
		elif not datrecv1[1] or not datrecv2[1]:
			runflag = False
		cv2.imshow('frame',frame)
    		if cv2.waitKey(1) & 0xFF == ord('q'):
    			break

	while pipeul1.poll(0.5) or pipeul2.poll(0.5):
		continue

finally:
	print "Cleaning up......"
	#sockets1 = pipesockl1.recv()
	#sockets2 = pipesockl2.recv()
	#for socs in sockets1 + sockets2:
	#	socs.close()
	proc1.join()
	proc2.join()
	vs.stop() #uncomment for testing
	cv2.destroyAllWindows()








