import numpy as np

mtx = np.array([[614.77666,0,316.92032],[0,615.67564,245.62514],[0,0,1]])
dist = np.array([0.10428,-0.18237,-0.00004,0.00167,0.00000])
def matrixcoeff(rmat, tvec, mtx, ppos):
	Q = np.dot(mtx,rmat)
	q = np.dot(mtx,tvec)
	Qinv = np.linalg.inv(Q)
	_Qinv = -1.0*Qinv
	c = np.dot(_Qinv,q)
	u = np.dot(Qinv,ppos)
	return c,u

def undistort(pts,dst):
	x1 = pts[0,0]
	y1 = pts[1,0]
	r = (x1**2 + y1**2)**0.5
	x2 = x1*(1 + dst[0]*r**2 + dst[1]*r**4 + dst[4]*r**6)
	xout = x2 + (2*dst[2]*x1*y1) + (dst[3]*(r**2 + 2*x1**2))
	y2 = y1*(1 + dst[0]*r**2 + dst[1]*r**4 + dst[4]*r**6)
	yout = y2 +  (2*dst[3]*x1*y1) + (dst[2]*(r**2 + 2*y1**2))
	return xout,yout
#part1 
#Rmat1 =np.array([[-0.10272235, -0.90512793,  0.41254279],[ 0.91509693,  0.07658829,  0.39589373],[-0.38993042,  0.41818378,  0.82041245]])
Rmat1 = np.array([[-0.10035968, -0.89909819,  0.42608729],[ 0.91567436,  0.084051  ,  0.39303422],[-0.38918942,  0.42960199,  0.81484583]])
#tvec1 = np.array([[  13.00241571],[-181.81332118],[ 571.25818342]])
tvec1 = np.array([[12.36737851],[-167.93518658],[ 649.63721379]])
#img1 = np.array([[ 322.65859985] ,[119.39465332],[1]])    #],[[ 257.91699219,64.93361664,1]],[[ 293.56796265,-15.79598808,1]]])
img1 = np.array([[321.46273804 ] ,[ 149.43701172],[1]])
c1,u1 = matrixcoeff(Rmat1, tvec1, mtx, img1)
print c1
print u1
print "-----------"	
#part2
#Rmat2=np.array([[ 0.13295929, -0.91547402, -0.37977512],[ 0.91115477, -0.03788472,  0.41031907],[-0.39002412, -0.40058964,  0.82910139]])
Rmat2=np.array([[ 0.12082783, -0.92990539, -0.34738538],[ 0.91335122, -0.03293256,  0.40583863],[-0.38883181, -0.36632146,  0.84535106]])
#tvec2 = np.array([[  -9.03438133],[-169.31072922],[ 614.54359952]])
tvec2 = np.array([[  48.8105872 ],[-173.48142889],[ 601.47818776]])
#img2= np.array([ [318.35992432],[141.78431702],[1]])  #],[[ 231.51911926,62.2338829,1]],[[ 340.3291626,17.75098419,1]]])
img2= np.array([ [379.92642212],[134.92285156],[1]])
c2,u2 = matrixcoeff(Rmat2, tvec2, mtx, img2)
print c2.T
print u2.T
print "-----------"

m = np.cross(u2.T.ravel(),u1.T.ravel())
p21 = c2.T.ravel() - c1.T.ravel()

lmda1 = np.dot(np.cross(p21,m),u2)/float(np.dot(m,m))
print "lambda 1 = %f"%(lmda1)
lmda2 = np.dot(np.cross(p21,m),u1)/float(np.dot(m,m))
print "lambda 2 = %f"%(lmda2)

pos1 = c1 + lmda1*u1
pos2 = c2 + lmda2*u2

print "pos1"
print pos1 

print "pos2"
print pos2

imgp = np.array([[50],[20],[90],[1]])
Rmatp = np.array([[ 0.12082783, -0.92990539, -0.34738538,48.8105872],[ 0.91335122, -0.03293256,  0.40583863,-173.48142889],[-0.38883181, -0.36632146,  0.84535106,601.47818776]])
proj1 = np.dot(mtx,np.dot(Rmatp,imgp))
proj1 = proj1/float(proj1[2,0]) 
print proj1
print"---------"
print undistort(img2,dist)
