################## IMPORT LIBRARIES ##################
import socket
import select
import os.path
import numpy as np
import cv2
import os
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
    def __init__(self, sockobj,dat_size,pipecal):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.arr = np.array([0,0,0],dtype=np.float64)
        self.flag = 1

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        self.trash = ''
        self.sock =sockobj
        self.pipe = pipecal
        self.dat_size = dat_size

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
            content = self.sock.recv(self.dat_size)
            if len(content) == self.dat_size:
                if (content[0] == 'u') and (content[-1] == 'l'): #valid data
                    self.arr = np.loads(content[1:self.dat_size-1]).ravel()
                    self.flag = 2
                elif content[0] == 'd': #invalid data
                    self.flag = 1
                elif content[0] == 'c': #calibration
                    self.pipe.send(np.loads(content[1:self.dat_size-1]).ravel())
                elif content[0] == 'e': #loop stop
                    self.flag = 0
                    self.stopped = True
            else:
                self.trash = sockobj.recv(self.dat_size - len(content)) #send truncated data to trash
    def read(self):
        return self.flag,self.arr

    # def readflag(self):
    #     return self.flag

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True



################## FUNCTION DEFINITIONS ##################

def socketcomm(port,pipec, flags,uarr,dat_size = 155):
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
    flag = 1
    arr = np.array([0,0,0],dtype=np.float64)
    #initialise socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((_TCP_SOCKET_HOST, port))
    serversocket.listen(1)
    serversocket.setblocking(1)
    #add server socket to list of sockets
    sockets.append(serversocket)
    #create epoll object
    #_epoll = select.epoll()
    #register interest in read events on the server socket
    #_epoll.register(serversocket.fileno(), select.EPOLLIN)
    #content = ''
    clientsocket,clientaddr = serversocket.accept()
    clientsocket.setblocking(1)
    sockets.append(clientsocket)
    sockr = SocketReader(clientsocket,dat_size=dat_size,pipecal=pipec).start()
    while (flag != 0):
    	flag,arr =  sockr.read()
    	with uarr.get_lock():
                    uarr.get_obj()[:3] = arr
        flags.value = flag
        #events = _epoll.poll(1)
        #for fileno, event in events:
            #if fileno == serversocket.fileno():
                #initialise client socket object
                #clientsocket.setblocking(1)
                ##register client socket on epoll
                #_epoll.register(clientsocket.fileno(),select.EPOLLIN)
        
            #elif event & select.EPOLLIN:
                #read event  on client socket
                #while (len(content) < dat_size):
                     #content += clientsocket.recv(dat_size-len(content))
                
                #with uarr.get_lock():
                #    uarr.get_obj()[:3] = arr
                #flags.value = flag

                # if (content[0] == 'u') and (content[-1] == 'l'):
                #     #pipeu.send((True,True,np.loads(content[1:157])))
                #                 with uarr.get_lock():
                #                     uarr.get_obj()[:3] = np.loads(content[1:157]).ravel()
                #     flags.value = 2
                # elif content[0] == 'd':
                #     #pipeu.send((False,True))
                #     flags.value = 1
                # elif content[0] == 'c':
                #     pipec.send(np.loads(content[1:]))
                # elif content[0] == 'e':
                #     #pipeu.send((False,False))
                #     flags.value = 0
                #     waiting_for_data = False
                #     for i in sockets:
                #         _epoll.unregister(i.fileno())
                # content = ''

            #elif event & select.EPOLLHUP:
                #for i in sockets:
                    #_epoll.unregister(i.fileno())
                    #i.close()
    for i in sockets:
        #_epoll.unregister(i.fileno())
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
pipecl1, pipecf1 = Pipe(False)
#pipes for uarr
#pipeuf1, pipeul1 = Pipe()
#pipes for socket objects
#pipesockf1, pipesockl1 = Pipe()
#set process
arr1 = np.array([0,0,0],dtype=np.float64)
uarray1 = Array('d',3)
#uarray1 = sharedctypes.synchronized(arr1)

uflag1 = Value('B',1)
proc1 = Process(target=socketcomm,args=(port1,pipecf1,uflag1,uarray1))

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
uarray2 = Array('d',3)
uflag2 = Value('B',1)
proc2 = Process(target=socketcomm,args=(port2,pipecf2,uflag2,uarray2))

################## START PROCESSES ##################

proc1.start()
proc2.start()
# uncomment nextline for testing
vs = WebcamVideoStream(src=0).start()

################## BEGIN MAIN LOOP ##################

print "Udating c..."
c1 = pipecl1.recv() #Blocking
c2 = pipecl2.recv() #Blocking
update_c(c1.ravel(),c2.ravel()) #########

print "Running main loop..."
while runflag:
    #print uflag1.value
    #print uflag2.value
    dat1 = uflag1.value
    dat2 = uflag2.value
    frame = vs.read() #for testing
    #datrecv1 = pipeul1.recv() #Blocking
    #datrecv2 = pipeul2.recv() #Blocking
    #if datrecv1[0] and datrecv2[0]:
    if (dat1 == 2) and (dat2 ==2):
        #pos3d =  calc3d(datrecv2[2].ravel(),datrecv1[2].ravel()) ########
        with uarray1.get_lock():
            arr1 = np.frombuffer(uarray1.get_obj())
        with uarray2.get_lock():
            arr2 = np.frombuffer(uarray2.get_obj())
        pos3d =  calc3d(arr1,arr2)
        #print np.asarray(pos3d)
        imgpts, jac = cv2.projectPoints(np.float32([np.asarray(pos3d)]).reshape(-1,3), rvecs, tvecs, mtx, dist)
        cv2.rectangle(frame,(int(imgpts[0,0,0]) - 2,int(imgpts[0,0,1]) - 2),(int(imgpts[0,0,0]) + 2 ,int(imgpts[0,0,1]) + 2),(255,0,0),1)
    #elif not datrecv1[1] or not datrecv2[1]:
    elif (dat1 == 0) or (dat2 ==0):
        runflag = False
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
    	break

print "Waiting for both processes to stop..."
#while pipeul1.poll(0.5) or pipeul2.poll(0.5):
while (uflag1.value != 0) or (uflag2.value != 0):
    continue

print "Cleaning up......"
#sockets1 = pipesockl1.recv()
#sockets2 = pipesockl2.recv()
#for socs in sockets1 + sockets2:
#   socs.close()
proc1.join()
proc2.join()
vs.stop() #uncomment for testing
cv2.destroyAllWindows()