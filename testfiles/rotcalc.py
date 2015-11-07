import numpy as np
import cv2

mtx = np.array([[1,0,0],[0,1,0],[0,0,1]])
dist = np.array([0,0,0,0,0])
tvec = np.array([0.0,0.0,0.0])
rvec = np.array([[-0.40620642],[0.08767342],[1.51987908]])

axis2 = np.float32([[1,0,0], [0,1,0], [0,0,1]]).reshape(-1,3)
imgpts2, jac2 = cv2.projectPoints(1.0 * axis2, 1.0 * rvec, 1.0 * tvec, 1.0 *mtx,1.0* dist)
print imgpts2