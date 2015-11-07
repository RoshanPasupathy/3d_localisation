Readme file

binarytester.py 
"""creates a thresholded image based on given parameters"""
modules: LUTptr2 - bgrhsv, matplotlib, os, time,cv2, numpy
comments: quite obsolete used for checking if ranges are correct and detect specs in background

calibcap.py
"""capture images"""
modules: numpy, cv2, os, time
comments: Use for intrinsic calibration. Can capture images from three hundred loops. adjust camera parameters to obtain clearer image

calibhue.py
"""plots hue,saturation and value for objects present in the rectangle in the frame"""
modules: LUTptr2 - bgrhsvarray2, matplotlib, os, time,cv2, numpy
comments: press c to capture. calibhuemouse is better

calibhuemouse1.py
"""plots hue,saturation and value for 3 selected objects"""
modules: LUTptr2 - bgrhsvarray2, matplotlib, os, time,cv2, numpy
comments: press s to select

LUTptr2.pyx
"""Cython file. does all the heavylifting"""
modules: cython,numpy
comments: Latest file, slight changes to LUTptr in oldfiles.
	  Change parameters in tablegen function to adjust hue,saturation and value limits respectively 
	  Use squarelut 5 to detect object
	  Use bgrhsvarray2 to plot hue,satuartion and value 

setuplutptr2.py
"""build file for LUTptr2"""
comments: use command >> python setuplutptr2.py build_ext --inplace
	  
pose_calibrationt.py
"""returns rotation matrix and tranbslation vector i.e. poise of camera"""
modules: numpy, cv2, os, time
comments: Adjust cornersubpix - not as accurate as expected
	  Show chessboard pattern

realtime2.py
"""shows detected object"""
modules: LUTptr2 - squarelut5, matplotlib, os, time,cv2, numpy
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