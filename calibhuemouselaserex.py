# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 13:16:07 2015

@author: Roshan
"""
#import modules
import numpy as np
#import matplotlib
#matplotlib.use('QT4Agg')
import cv2
import os
from LUTptrallr import bgrhsvarrayl
from LUTptrallr import bgrhsvarraylc
from LUTptrallr import bgrhsvarray3
from LUTptrallr import cleanupf
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
#plt.grid(True)

#set camera parameters
os.system('v4l2-ctl -d 0 -c focus_auto=0')
os.system('v4l2-ctl -d 0 -c focus_absolute=0')
os.system('v4l2-ctl -d 0 -c exposure_auto=1')
os.system('v4l2-ctl -d 0 -c exposure_absolute=3')
os.system('v4l2-ctl -d 0 -c contrast=100')
os.system('v4l2-ctl -d 0 -c brightness=100')
os.system('v4l2-ctl -d 0 -c white_balance_temperature_auto=0')
os.system('v4l2-ctl -d 0 -c white_balance_temperature=6500')

#decalre flags
picturestaken = 0 #checks number of pictures calibrated
calibdone = False #status of calibration per picture
calibwindowopen = False #status of calibration window
running = True # status of webcam loop. False = terminate
scene = False #Is the selection window being displayed or video window

#declare calibration parameters
colourfreq = np.zeros((256,256,256))
colourscene = np.zeros((256,256,256))

#region of interest parameters and flags
rect = (0,0,1,1) #coordinates of corners
rectangle = False
rect_over = False
  
def onmouse(event,x,y,flags,params):
    """this function is called on mouse click. it plots colour,saturation and intensity for slected region of interest"""
    # Declare global objects
    global sceneImg,backimage,rectangle,rect,ix,iy,rect_over, colourfreq,picturestaken,scene,calibwindowopen
    #Copy img
    sceneCopy = sceneImg.copy()
    # Draw Rectangle
    if event == cv2.EVENT_LBUTTONDOWN:
        rectangle = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if rectangle == True:
            cv2.rectangle(sceneCopy,(ix,iy),(x,y),(0,255,0),1)
            #rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))
            cv2.imshow('mouse input', sceneCopy)
            cv2.waitKey(1)

    elif event == cv2.EVENT_LBUTTONUP:
        rectangle = False
        rect_over = True
        
	
        #cv2.rectangle(sceneImg,(ix,iy),(x,y),(0,255,0),1)
        # Draw rectangle in copy
        cv2.rectangle(sceneCopy,(ix,iy),(x,y),(0,255,0),1)
        #cv2.imwrite('/home/pi/ip/report/selectionLaser.jpg',sceneCopy)
        
        
        rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))
        diffimage = np.asarray(bgrhsvarrayl(backimage,sceneImg,rect[1],rect[1]+rect[3],rect[0],rect[0]+rect[2],50.0))       
        ##filteraxis = np.asarray(bgrhsvarray3(sceneImg,rect[1],rect[1]+rect[3],rect[0],rect[0]+rect[2]))
        filteraxis = np.asarray(bgrhsvarraylc(diffimage,sceneImg,rect[1],rect[1]+rect[3],rect[0],rect[0]+rect[2],50.0))
        colourfreq += filteraxis
        #display copy with rectangle for 4 second
        #cv2.imwrite('/home/pi/ip/report/diffLaser.jpg',diffimage)
        cv2.imshow('mouse input', diffimage)
        cv2.waitKey(4000)
        
        picturestaken += 1
        print rect
        print "%d picturestaken"%(picturestaken)
        scene = False
        cv2.destroyWindow('mouse input')
        calibwindowopen = False
        

# Named window and mouse callback
#cv2.namedWindow('mouse input')
#cv2.setMouseCallback('mouse input',onmouse)
cv2.namedWindow('video')
cap = cv2.VideoCapture(0)
#cap.set(cv2.cv.CV_CAP_PROP_FPS, 30)
#cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,720)
#cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,920)
keyPressed = None

#print instructions
print "Press b to capture background. Press o to obtain laser colour val. Press s to obtain colours of background"
# Start video stream
while running:
    readOK, frame = cap.read()
    calibdone = False	
    keyPressed = cv2.waitKey(5)
    
    if keyPressed == ord('b'):
    	backimage = frame
    	#cv2.imwrite('/home/pi/ip/report/referenceLaser.jpg',frame)
    	print "Background image taken"
    
    if keyPressed == ord('o'):
        print "you pressed o. Please wait"
    	#while calibdone == False:
        scene = True
        cv2.destroyWindow('video')
        print "Select object of interest"
        sceneImg = frame.copy() 
        cv2.imshow('mouse input', sceneImg)
    
    if keyPressed == ord('s'):
        print "You pressed s. Please wait"
    	Backgroundval = frame.copy()
    	#h,w,c = Backgroundval.shape
    	#print w,h
    	filterscene = np.asarray(bgrhsvarray3(Backgroundval))
        colourscene += filterscene
        cv2.imshow('video', Backgroundval[0:480,0:640])
        cv2.waitKey(1000)
        print "background colours have been checked"
	
    if not calibwindowopen:
    	cv2.namedWindow('mouse input')
    	cv2.setMouseCallback('mouse input',onmouse)
    	calibwindowopen = True
    if not scene:
        cv2.imshow('video', frame)

    if picturestaken == 3:
    	running = False
    
#fig = plt.figure(figsize = (8,6))
#ax = fig.add_subplot(111,projection = '3d')
#ax.grid(True)
###sortedh = np.sort(hueaxis)
###huevals = np.array(np.where(hueaxis >= sortedh[-3])).tolist() #list with double bracket
###print 'hue values of ball =  %s. Please refer to plot' %(', '.join(str(it) for it in huevals[0]))

#interestpos = np.nonzero(colourfreq)
#xo = interestpos[0]
#yo = interestpos[1]
#zo = interestpos[2]
#colval = colourfreq[interestpos]
#colors = cm.winter(colval/max(colval))

#colmap = cm.ScalarMappable(cmap = cm.winter)
#colmap.set_array(colval/max(colval))
#scenepos = np.nonzero(colourscene)
#xs = scenepos[0]
#ys = scenepos[1]
#zs = scenepos[2]
#colvals = colourscene[scenepos]
#colours2 = cm.spring(colvals/max(colvals))

#colmap2 = cm.ScalarMappable(cmap = cm.spring)
#colmap2.set_array(colvals)

#ax.scatter(xo,yo,zo, c=colors, marker='o',label='Laser Dot ')
#ax.scatter(xs,ys,zs, c=colours2, marker='s',label='Background')

#cb = fig.colorbar(colmap,shrink=0.75)
#cb.set_label('Laser Dot')
#cb2 = fig.colorbar(colmap2,shrink=0.75)
#cb2.set_label('Background')

#ax.set_xlabel('Hue')
#ax.set_ylabel('Saturation')
#ax.set_zlabel('Intensity')

#########
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
#ax1.grid(True)

huefreq = np.sum(np.sum(colourfreq,axis=2),axis=1)
ax1.set_xlim([0,180])
ax1.set_ylim([0,max(huefreq) + 20])
ax1.bar(np.arange(256) - 0.5,huefreq, width=1.0, color='b')
ax1.set_xticks(np.arange(0,181,20))
ax1.set_title('Frequency of Occurence of Hues') 
ax1.set_xlabel('Hue (0-180)')
ax1.set_ylabel('Frequency (pixels)')

#plt.legend(loc='upper left')
#fig2 = plt.figure(2)
#ax2 = fig2.add_subplot(111)
#ax2.grid(True)
#hueaccept1 = colourfreq[40:80,:,:]
#hueaccept = np.nonzero(hueaccept1)
#satdata = hueaccept[1]
#valdata = hueaccept[2]
#densityfunc = hueaccept1[hueaccept]
#colours3 = cm.cool(densityfunc/max(densityfunc))

#colmap3 = cm.ScalarMappable(cmap = cm.cool)
#colmap3.set_array(densityfunc)

#ax2.scatter(satdata,valdata, c=colours3,marker='o')
#cb3 = fig2.colorbar(colmap3,shrink=0.75)
#ax2.set_title('Intenisty vs. Saturation') 
#cb3.set_label('frequency')
#ax2.set_xlabel('Saturation')
#ax2.set_ylabel('Intensity')
#######

#fig3 = plt.figure(3)
#ax3 = fig3.add_subplot(111)
#ax3.grid(True)
#hueaccept2 = colourscene[40:80,:,:]
#hueaccept3 = np.nonzero(hueaccept2)
#satdatas = hueaccept3[1]
#valdatas = hueaccept3[2]
#densityfuncs = hueaccept2[hueaccept3]
#if len(densityfuncs) != 0:
        #colours4 = cm.cool(densityfuncs/max(densityfuncs))
        #colmap4 = cm.ScalarMappable(cmap = cm.cool)
        #colmap4.set_array(densityfuncs/max(densityfuncs))

        #ax3.scatter(satdatas,valdatas, c=colours4,marker='o')
        #cb4 = fig3.colorbar(colmap4,shrink=0.75)
        #cb4.set_label('frequency')
        #ax3.set_title('Intenisty vs. Saturation') 
        #ax3.set_xlabel('Scene Saturation')
        #ax3.set_ylabel('Scene Value')
#else:
        #print 'No background pixels in the hue range 40 to 80' 
######

#fig4 = plt.figure(4)
##huefrequencies = colourfreq[0]
##freqhue = np.bincount(huefrequencies)
##huesxaxis = np.arange(len(freqhue))
#ax4 = fig4.add_subplot(111)
#ax4.grid(True)
#ax4.set_title('Frequency of Occurence vs. Hue')
#ax4.scatter(colorfreq[0],freqhue, marker='o')
#ax4.set_xlabel('Hue')
#ax4.set_ylabel('Frequency of Occurence')

#######
cleanupf()
cv2.destroyAllWindows()
cap.release()
plt.show()
