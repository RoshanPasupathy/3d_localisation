Readme file

binarytester.py 
"""creates a thresholded image based on given parameters"""
modules: LUTptrallr - bgrhsv, matplotlib, os, time,cv2, numpy
comments: quite obsolete used for checking if ranges are correct and detect specs in background

calibcap.py
"""capture images"""
modules: numpy, cv2, os, time
comments: Use for intrinsic calibration. Can capture images from three hundred loops. adjust camera parameters to obtain clearer image

calibhue.py
"""plots hue,saturation and value for objects present in the rectangle in the frame"""
modules: LUTptrallr - bgrhsvarray2, matplotlib, os, time,cv2, numpy
comments: press c to capture. calibhuemouse is better

calibhuemouse1.py
"""plots hue,saturation and value for 3 selected objects"""
modules: LUTptrallr - bgrhsvarray2, matplotlib, os, time,cv2, numpy
comments: press s to select

calibhuemouselaserex.py
"""plots hue,saturation and value for scene and laser dot"""
modules: LUTptr3 - bgrhsvarray3, bgrhsvarrayl, bgrhsvarraylc, matplotlib, os, time,cv2, numpy
comments: Press s to gather scene data. Press b to store a background image for comparison. Press o to select laser dot region.
	  Plot m1,m2,c1,c2 values from graph
	  PROBLEMS: SEGMENTATION ERROR WHEN S IS PRESSED,CHECK LUTPTR3 

LUTptr2.pyx
"""Old Cython file. does all the heavylifting"""
modules: cython,numpy
comments: slight changes to LUTptr in oldfiles.
	  Change parameters in tablegen function to adjust hue,saturation and value limits respectively 
	  Use squarelut 5 to detect object
	  Use bgrhsvarray2 to plot hue,satuartion and value

LUTptr3.pyx
"""New Cython file. does all the heavylifting"""
modules: cython,numpy
comments: Latest file, slight changes to LUTptr in oldfiles.
	  Dynamic thresholding in tablegen. High saturation ->> low value 
	  Use squarelut6 to detect object
	  Use bgrhsvarray3 to obtain a frequency array for hue, saturation, value of the scene
	  Use bgrhsvarrayl to obtain a diff image (binary) 
	  Use bgrhsvarraylc to obtain a frequency array for hue, saturation, value of True pixels 

setuplutptr2.py
"""build file for LUTptr2"""
comments: use command >> python setuplutptr2.py build_ext --inplace

setuplutptr3.py
"""build file for LUTptr3"""
comments: use command >> python setuplutptr3.py build_ext --inplace
	  
pose_calibrationt.py
"""returns rotation matrix and tranbslation vector i.e. poise of camera"""
modules: numpy, cv2, os, time
comments: Adjust cornersubpix - not as accurate as expected
	  Show chessboard pattern

realtime2.py
"""shows detected object"""
modules: LUTptr3 (changed from LUTptralls) - squarelut5, matplotlib, os, time,cv2, numpy
comments: comment out rectangle and imshow for speed

undistort.py
"""Caculates undistorted position"""
modules: numpy, undistortcython
comments: works well.

undistortcython.pyx
"""creates look up table to convert distorted psotions to undistorted positions"""
modules: Cython

vectorcalc.py
"""get from macbook. Calculates 3d postion"""
comments: not here