cimport cython
import numpy as np
cimport numpy as np
#from cpython cimport array

# cdef double[::1] cross(double* arr1,double* arr2):
# 	cdef:
# 		double[::1] outarr = np.array([(arr1[1] * arr2[2]),(arr1[2] * arr2[0]),(arr1[0] * arr2[1])],dtype=np.float64)
# 		double* outptr =  &outarr[0]
# 	# outptr[0]  =  (arr1[1] * arr2[2])
# 	outptr[0] -= (arr1[2] * arr2[1])
# 	# outptr[1]  =  (arr1[2] * arr2[0])
# 	outptr[1] -= (arr1[0] * arr2[2])
# 	# outptr[2]  =  (arr1[0] * arr2[1])
# 	outptr[2] -= (arr1[1] * arr2[0])
# 	return outarr

cdef double[::1] marr= np.array([0.0,0.0,0.0],dtype=np.float64)
cdef double* m =  &marr[0]

cdef double[::1] basevalarr= np.array([0.0,0.0,0.0],dtype=np.float64)
cdef double* baseval =  &basevalarr[0]

c1 = np.array([12.45,610.34,74.10],dtype=np.float64)
c2 = np.array([80.45,12.34,56.78],dtype=np.float64)
cdef double[::1] p21 = c2 - c1
cdef double* c21ptr =  &p21[0]

cdef double[::1] c2p1harr = (c2 + c1)/2.0
cdef double* c2p1h = &c2p1harr[0]

cdef double[::1] outarr= np.array([0.0,0.0,0.0],dtype=np.float64)
cdef double* outptr =  &outarr[0]

# def def_c21(double[:] c21):
# 	global

@cython.boundscheck(False)
@cython.cdivision(True)
@cython.wraparound(False)
def update_c(double[::1] c1,double[::1] c2):
	c2p1h[0] = (c2[0] + c1[0])/2.0
	c2p1h[1] = (c2[1] + c1[1])/2.0
	c2p1h[2] = (c2[2] + c1[2])/2.0
	c21ptr[0] = c2[0] - c1[0]
	c21ptr[1] = c2[1] - c1[1]
	c21ptr[2] = c2[2] - c1[2]

@cython.boundscheck(False)
@cython.cdivision(True)
@cython.wraparound(False)
cdef void crossm(double* arr1,double* arr2):
	"""returns a pointer doesnt make sense. why ?
	--> pointer points to object in local scope
	--> can pass to another function which now points to this memory"""
	global m
	# cdef:
	# 	double[::1] outarr = np.array([0.0,0.0,0.0],dtype=np.float64) #local object closed on function exit hence pointer points to garbage
	# 	# double[::1] outarr = np.array([(arr1[1] * arr2[2]),(arr1[2] * arr2[0]),(arr1[0] * arr2[1])],dtype=np.float64)
	# 	double* outptr =  &outarr[0]
	# outptr[0]  =  (arr1[1] * arr2[2])
	m[0] =  (arr1[1] * arr2[2]) - (arr1[2] * arr2[1])
	# outptr[1]  =  (arr1[2] * arr2[0])
	m[1] = (arr1[2] * arr2[0])-(arr1[0] * arr2[2])
	# outptr[2]  =  (arr1[0] * arr2[1])
	m[2] = (arr1[0] * arr2[1])-(arr1[1] * arr2[0])
	# return outptr

@cython.boundscheck(False)
@cython.cdivision(True)
@cython.wraparound(False)
cdef void crossbv(double* arr1):
	"""returns a pointer doesnt make sense. why ?
	--> pointer points to object in local scope
	--> can pass to another function which now points to this memory"""
	global baseval
	# cdef:
	# 	double[::1] outarr = np.array([0.0,0.0,0.0],dtype=np.float64) #local object closed on function exit hence pointer points to garbage
	# 	# double[::1] outarr = np.array([(arr1[1] * arr2[2]),(arr1[2] * arr2[0]),(arr1[0] * arr2[1])],dtype=np.float64)
	# 	double* outptr =  &outarr[0]
	# outptr[0]  =  (arr1[1] * arr2[2])
	baseval[0] =   (arr1[1] * m[2]) - (arr1[2] * m[1])
	# outptr[1]  =  (arr1[2] * arr2[0])
	baseval[1] = (arr1[2] * m[0])-(arr1[0] * m[2])
	# outptr[2]  =  (arr1[0] * arr2[1])
	baseval[2] = (arr1[0] * m[1])-(arr1[1] * m[0])
	# return outptr

# cdef double[::1] crossmv(double* arr1,double* arr2):
# 	cdef:
# 		double[::1] outarr = np.array([(arr1[1] * arr2[2]),(arr1[2] * arr2[0]),(arr1[0] * arr2[1])],dtype=np.float64)
# 		double* outptr =  &outarr[0]
# 	# outptr[0]  =  (arr1[1] * arr2[2])
# 	outptr[0] -= (arr1[2] * arr2[1])
# 	# outptr[1]  =  (arr1[2] * arr2[0])
# 	outptr[1] -= (arr1[0] * arr2[2])
# 	# outptr[2]  =  (arr1[0] * arr2[1])
# 	outptr[2] -= (arr1[1] * arr2[0])
# 	return outarr

@cython.boundscheck(False)
@cython.cdivision(True)
@cython.wraparound(False)
cdef void crossc(double* arr1,double* arr2):
	"""returns a pointer doesnt make sense. why ?
	--> pointer points to object in local scope
	--> can pass to another function which now points to this memory"""
	global m,baseval
	# cdef:
	# 	double[::1] outarr = np.array([0.0,0.0,0.0],dtype=np.float64) #local object closed on function exit hence pointer points to garbage
	# 	# double[::1] outarr = np.array([(arr1[1] * arr2[2]),(arr1[2] * arr2[0]),(arr1[0] * arr2[1])],dtype=np.float64)
	# 	double* outptr =  &outarr[0]
	# outptr[0]  =  (arr1[1] * arr2[2])
	m[0] =   (arr1[1] * arr2[2]) - (arr1[2] * arr2[1])
	# outptr[1]  =  (arr1[2] * arr2[0])
	m[1] = (arr1[2] * arr2[0])-(arr1[0] * arr2[2])
	# outptr[2]  =  (arr1[0] * arr2[1])
	m[2] = (arr1[0] * arr2[1])-(arr1[1] * arr2[0])

	cdef double m2 = (m[0] * m[0]) + (m[1] * m[1]) + (m[2] * m[2])

	baseval[0] =   ((c21ptr[1] * m[2]) - (c21ptr[2] * m[1]))/m2
	# outptr[1]  =  (arr1[2] * arr2[0])
	baseval[1] = ((c21ptr[2] * m[0])-(c21ptr[0] * m[2]))/m2
	# outptr[2]  =  (arr1[0] * arr2[1])
	baseval[2] = ((c21ptr[0] * m[1])-(c21ptr[1] * m[0]))/m2


@cython.boundscheck(False)
@cython.cdivision(True)
@cython.wraparound(False)
cdef void cross(double* arr1,double* arr2):
	"""returns a pointer doesnt make sense. why ?
	--> pointer points to object in local scope
	--> can pass to another function which now points to this memory"""
	global m,outptr
	m[0] =   (arr1[1] * arr2[2]) - (arr1[2] * arr2[1])
	m[1] = (arr1[2] * arr2[0])-(arr1[0] * arr2[2])
	m[2] = (arr1[0] * arr2[1])-(arr1[1] * arr2[0])

	cdef double m2 = (m[0] * m[0]) + (m[1] * m[1]) + (m[2] * m[2])

	m[0] =   ((c21ptr[1] * m[2]) - (c21ptr[2] * m[1]))/m2
	# outptr[1]  =  (arr1[2] * arr2[0])
	m[1] = ((c21ptr[2] * m[0])-(c21ptr[0] * m[2]))/m2
	# outptr[2]  =  (arr1[0] * arr2[1])
	m[2] = ((c21ptr[0] * m[1])-(c21ptr[1] * m[0]))/m2

	cdef:
		double lmda1 = (((m[0] * arr1[0])  +   (m[1] * arr1[1]) + (m[2] * arr1[2])))/2.0
		double lmda2 = (((m[0] * arr2[0])  +   (m[1] * arr2[1]) + (m[2] * arr2[2])))/2.0
	outptr[0] = c2p1h[0] + (arr2[0] * lmda1) + (arr1[0] * lmda2)
	outptr[1] = c2p1h[1] + (arr2[1] * lmda1) + (arr1[1] * lmda2)
	outptr[2] = c2p1h[2] + (arr2[2] * lmda1) + (arr1[2] * lmda2)


#fastest
@cython.boundscheck(False)
@cython.cdivision(True)
@cython.wraparound(False)
def calc3d(double[::1] u1ptr,double[::1] u2ptr):
	crossc(&u2ptr[0],&u1ptr[0]) #update m and baseval
	cdef:
		# double m2 = (m[0] * m[0]) + (m[1] * m[1]) + (m[2] * m[2])
		double lmda1 = ((baseval[0] * u2ptr[0])  +   (baseval[1] * u2ptr[1]) + (baseval[2] * u2ptr[2]))#/(m2)
		double lmda2 = ((baseval[0] * u1ptr[0])  +   (baseval[1] * u1ptr[1]) + (baseval[2] * u1ptr[2]))#/(m2)
	outptr[0] = c2p1h[0] + ((u1ptr[0] * lmda1) + (u2ptr[0] * lmda2))/2.0
	outptr[1] = c2p1h[1] +((u1ptr[1] * lmda1) + (u2ptr[1] * lmda2))/2.0
	outptr[2] = c2p1h[2] +((u1ptr[2] * lmda1) + (u2ptr[2] * lmda2))/2.0
	return outarr

# not working. do not use
@cython.cdivision(True)
@cython.wraparound(False)
def mainrecvmv(double[::1] u1ptr,double[::1] u2ptr):
	cross(&u2ptr[0],&u1ptr[0]) #update m and baseval
	return outarr

# @cython.boundscheck(False)
# @cython.cdivision(True)
# @cython.wraparound(False)
# def mainrecv(double[::1] c2p1h,double[::1] u1,double[::1] u2):
# 	crossc(&u2[0],&u1[0]) #double* m
# 	# crossbv(&c2_1[0]) #double* baseval
# 	cdef:
# 		# double[::1] outarr = np.array([0.0,0.0,0.0],dtype=np.float64)
# 		double* outptr =  &c2p1h[0]
# 		double m2 = (m[0] * m[0]) + (m[1] * m[1]) + (m[2] * m[2])
# 		double lmda1 = ((baseval[0] * u2[0])  +   (baseval[1] * u2[1]) + (baseval[2] * u2[2]))/(m2)
# 		double lmda2 = ((baseval[0] * u1[0])  +   (baseval[1] * u1[1]) + (baseval[2] * u1[2]))/(m2)
# 		# double[::1] q1 = cymult(u1,lmda1)
# 		# double[::1] q2 = cymult(u2,lmda2)
# 	for i in range(3):
# 		u1[i] = u1[i] * lmda1
# 		u2[i] = u2[i] * lmda2
# 		outptr[i] += ((u1[i] + u2[i])/2.0)
# 	# outptr[1] = c2p1h[1] + ((u1[1] + u2[1])/2.0)
# 	# outptr[2] = c2p1h[2] + ((u1[2] + u2[2])/2.0)
# 	# return outarr
# 	# outptr[0] = m[0]
# 	# outptr[1] = m[1]
# 	# outptr[2] = m[2]
# 	return c2p1h

# def mainrecv(double[::1] c2_1,  double[::1] c2p1h,double[::1] u1,double[::1] u2):
# 	crossm(&u2[0],&u1[0]) #double* m
# 	crossbv(&c2_1[0]) #double* baseval
# 	cdef:
# 		# double[::1] outarr = np.array([0.0,0.0,0.0],dtype=np.float64)
# 		double* outptr =  &c2_1[0]
# 		double m2 = (m[0] * m[0]) + (m[1] * m[1]) + (m[2] * m[2])
# 		double lmda1 = ((baseval[0] * u2[0])  +   (baseval[1] * u2[1]) + (baseval[2] * u2[2]))/(m2)
# 		double lmda2 = ((baseval[0] * u1[0])  +   (baseval[1] * u1[1]) + (baseval[2] * u1[2]))/(m2)
# 		# double[::1] q1 = cymult(u1,lmda1)
# 		# double[::1] q2 = cymult(u2,lmda2)
# 	for i in range(3):
# 		u1[i] = u1[i] * lmda1
# 		u2[i] = u2[i] * lmda2
# 		outptr[i] = c2p1h[i] + ((u1[i] + u2[i])/2.0)
# 	# outptr[1] = c2p1h[1] + ((u1[1] + u2[1])/2.0)
# 	# outptr[2] = c2p1h[2] + ((u1[2] + u2[2])/2.0)
# 	# return outarr
# 	# outptr[0] = m[0]
# 	# outptr[1] = m[1]
# 	# outptr[2] = m[2]
# 	return c2_1

# def mainrecvmv(double[::1] c2_1,  double[::1] c2p1h,double[::1] u1,double[::1] u2):
# 	cdef:
# 		double[::1] outarr = np.array([0.0,0.0,0.0],dtype=np.float64)
# 		double* outptr =  &outarr[0]
# 		double[::1] m = crossmv(&u2[0],&u1[0])
# 		double[::1] baseval = crossmv(&c2_1[0],&m[0])
# 		double m2 = (m[0] * m[0]) + (m[1] * m[1]) + (m[2] * m[2])
# 		double lmda1 = ((baseval[0] * u2[0])  +   (baseval[1] * u2[1]) + (baseval[2] * u2[2]))/(m2)
# 		double lmda2 = ((baseval[0] * u1[0])  +   (baseval[1] * u1[1]) + (baseval[2] * u1[2]))/(m2)
# 	for i in range(3):
# 		u1[i] = u1[i] * lmda1
# 		u2[i] = u2[i] * lmda2
# 	outptr[0] = c2p1h[0] + ((u1[0] + u2[0])/2.0)
# 	outptr[1] = c2p1h[1] + ((u1[1] + u2[1])/2.0)
# 	outptr[2] = c2p1h[2] + ((u1[2] + u2[2])/2.0)
# 	# return outarr
# 	# outptr[0] = m[0]
# 	# outptr[1] = m[1]
# 	# outptr[2] = m[2]
# 	return outarr