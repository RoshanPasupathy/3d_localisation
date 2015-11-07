cimport cython
import numpy as np
cimport numpy as np
ctypedef np.float_t FTYPE_t
ctypedef np.uint8_t CTYPE_t
ctypedef np.int64_t LTYPE_t
ctypedef np.uint32_t DTYPE_t
import cv2

dst = np.array([0.10428,-0.18237,-0.00004,0.00167,0.0])
mtx = np.array([[614.77666,0.0,316.92032],[0.0,615.67564,245.62514],[0.0,0.0,1.0]])
testpoints = np.array([[[321.46273804,149.43701172],[379.92642212,134.92285156]]])
cdef double[:,::1] result = cv2.undistortPoints(testpoints,mtx,dst,R = None,P= mtx)[0]
cdef double* resptr = &result[0,0]
#result = cv2.undistortPoints(testpoints,mtx,dst,R = None,P= mtx)
val = resptr[0],resptr[1]
