# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 13:16:07 2015

@author: Roshan
"""
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

picturestaken = 0
calibdone = False
xaxis = np.arange(0,256,1)
hueaxis = np.zeros(256)
saturationaxis = np.zeros(256)
valueaxis = np.zeros(256)
#roi = np.array([[80,180,160,260],[40,140,100,200],[370,440,530,600],[150,230,300,380]])
rect = (0,0,1,1)
rectangle = False
rect_over = False  
def onmouse(event,x,y,flags,params):
    global sceneImg,rectangle,rect,ix,iy,rect_over, hueaxis,saturationaxis,valueaxis,picturestaken,scene
    #print "onmouse called"
    # Draw Rectangle
    if event == cv2.EVENT_LBUTTONDOWN:
        rectangle = True
        ix,iy = x,y
        #print "lbuttondown"

    elif event == cv2.EVENT_MOUSEMOVE:
        if rectangle == True:
#            cv2.rectangle(sceneCopy,(ix,iy),(x,y),(0,255,0),1)
            rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))

    elif event == cv2.EVENT_LBUTTONUP:
        rectangle = False
        rect_over = True
        #print "lbuttonup"

        sceneCopy = sceneImg.copy()
        #cv2.rectangle(sceneImg,(ix,iy),(x,y),(0,255,0),1)
        cv2.rectangle(sceneCopy,(ix,iy),(x,y),(0,255,0),1)
        
        
        rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))       
        #roi = sceneCopy[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
        filteraxis = np.asarray(bgrhsvarray2(sceneImg,rect[1],rect[1]+rect[3],rect[0],rect[0]+rect[2]))
        hueaxis += filteraxis[0,:]
        saturationaxis += filteraxis[1,:]
        valueaxis += filteraxis[2,:]
        cv2.imshow('mouse input', sceneCopy)
        cv2.waitKey(1000)
        
        picturestaken += 1
        
        #cv2.imwrite('roi.jpg', roi)
        print "%d picturestaken"%(picturestaken)
        scene = False
        cv2.destroyWindow('mouse input')
        

# Named window and mouse callback
#cv2.namedWindow('mouse input')
#cv2.setMouseCallback('mouse input',onmouse)
cv2.namedWindow('video')
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 30)
keyPressed = None
running = True
scene = False
# Start video stream
while running:
    readOK, frame = cap.read()
    print "press i to initialise and reset mouse input window"
    print "print s to select region. *Warning: do not press s if mouse input window not present"
    calibdone = False	
    keyPressed = cv2.waitKey(5)
    if keyPressed == ord('s'):
    	
    	#while calibdone == False:
        scene = True
        cv2.destroyWindow('video')
        print "draw a box"

        	#cv2.imwrite('sceneImg.jpg',frame)
        sceneImg = frame.copy() #cv2.imread('sceneImg.jpg')

        cv2.imshow('mouse input', sceneImg)
	
    elif keyPressed == ord('i'):
    	cv2.namedWindow('mouse input')
    	cv2.setMouseCallback('mouse input',onmouse)

    #elif keyPressed == ord('q'):
    #    running = False

    if not scene:
        cv2.imshow('video', frame)
    if picturestaken == 3:
    	running = False
    
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
#print 'time elapsed = %f s' %(end - start)
#print 'frame rate = %f' %(l/(end - start))

cv2.destroyAllWindows()
cap.release()
