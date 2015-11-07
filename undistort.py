# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 01:10:39 2015

@author: Roshan
"""
import cv2
import numpy as np

import numpy, pyximport
pyximport.install(setup_args={"script_args":["--compiler=mingw32"], "include_dirs":numpy.get_include()}, reload_support=True)
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True
import undistortc2

a = np.mgrid[:640,:480].T
img = np.ones((480,640,3))
img[:,:,:2] = a
img = 1.00 * img
dst = np.array([0.10428,-0.18237,-0.00004,0.00167,0.0])
mtx = np.array([[614.77666,0.0,316.92032],[0.0,615.67564,245.62514],[0.0,0.0,1.0]])
R = np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
_A,opt = cv2.getOptimalNewCameraMatrix(mtx,dst,(480,640),0)
map1,map2 = cv2.initUndistortRectifyMap(mtx,dst,R,_A,(480,640),cv2.CV_32FC1)
mapx = np.around(map1)
mapy = np.around(map2)
testpoints1 = np.array([[[321.46273804,149.43701172]]])
testpoints2 = np.array([[[379.92642212,134.92285156]]])
result1 = cv2.undistortPoints(testpoints1,mtx,dst,R = None,P= mtx)
result2 = cv2.undistortPoints(testpoints2,mtx,dst,R = None,P= mtx)

print undistortc2.val
#result = np.zeros((641))
#for i in mapy.T[0]:
#    result[i] += 1


    