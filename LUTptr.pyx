cimport cython
import numpy as np
cimport numpy as np
ctypedef np.float_t FTYPE_t
ctypedef np.uint8_t CTYPE_t
ctypedef np.int64_t LTYPE_t
ctypedef np.uint32_t DTYPE_t


@cython.boundscheck(False)
@cython.cdivision(True)
@cython.wraparound(False)
cdef unsigned char[:,:,::1] tablegen(long hmin,long hmax,long smin, long smax, long v, long vmax):
    cdef:
        unsigned char[:,:,::1] table = np.zeros((256,256,256),dtype = np.uint8)
        long x0,y0,z0
        double b,g,r
        int K
        double chroma
        long hue
        long saturation
        unsigned char* table_ptr = &table[0,0,0]        
    for x0 in range(256):
        for y0 in range(256):
            for z0 in range(256):
                b,g,r = x0,y0,z0
                K = 0
                if g < b:
                    g,b = b,g
                    K = -6
                if r < g:
                    r,g = g,r
                    K =  -K - 2
                chroma = r - min(g,b)
                if r != 0:
                    saturation = int(255 * chroma/(r * 1.0))
                else:
                    saturation = 0
                if chroma != 0:
                    hue = int(30 * abs(K +((g-b)/(chroma))))
                    if (hue>= hmin) & (hue <= hmax) & (r >=v) & (r <= vmax) & (saturation >= smin) & (saturation <= smax):
                        table_ptr[(256*256*x0) + (256*y0)+z0] = 1
    return table

cdef unsigned char[:,:,::1] tablelut = tablegen(89,100,50,255,200,255)
cdef unsigned char* tablelut_ptr = &tablelut[0,0,0]
cdef long[::1] x_out = np.zeros((480*640), dtype = np.int32)
#cdef long* x_outptr = &x_out[0]
cdef long[::1] y_out = np.zeros((640), dtype = np.int32)
#cdef long* y_outptr = &y_out[0]

@cython.boundscheck(False)
@cython.cdivision(True)
@cython.wraparound(False)
def squarelut5(long[::1] input,long x, long y,unsigned char v,unsigned char[:,:,::1] image):
    cdef:
        long* inputptr = &input[0]
        long xminscan = (inputptr[2]< inputptr[3])*((v+1)*inputptr[2] > (v*inputptr[3]))*((v + 1)*inputptr[2] - (v*inputptr[3]))
        long yminscan = (inputptr[0]< inputptr[1])*((v+1)*inputptr[0] > (v*inputptr[1]))*((v + 1)*inputptr[0] - (v*inputptr[1]))
        long xmaxscan = (inputptr[2]< inputptr[3])*((v+1)*inputptr[3] < x + (v*inputptr[2]))*(((v+1)*inputptr[3]) - (v*inputptr[2]) - x) + x
        long ymaxscan = (inputptr[0]< inputptr[1])*((v+1)*inputptr[1] < x + (v*inputptr[0]))*(((v+1)*inputptr[1]) - (v*inputptr[0]) - y) + y
        long deltax = xmaxscan - xminscan
        long deltay = ymaxscan - yminscan
        unsigned char* img_ptr = &image[0,0,0]
        unsigned char inc
        #long[::1] x_out = np.zeros((deltax*deltay), dtype = np.int32)
        long* x_outptr = &x_out[0]
        #long[::1] y_out = np.zeros((deltay), dtype = np.int32)
        long* y_outptr = &y_out[0]
        long[::1] output = np.array([y,0,0,0], dtype = np.int32)
        long* outputptr = &output[0]
        long x0,y0,i0
        long i = 0
    y_outptr[1] = y
    for x0 in range(deltax):
        i0 = i
        for y0 in range(deltay):
            inc = tablelut_ptr[256*256*img_ptr[3*((xminscan + x0)*y + y0 + yminscan)] + 256*img_ptr[3*((xminscan + x0)*y + y0 + yminscan) +1] + img_ptr[3*((xminscan + x0)*y + y0 + yminscan) + 2]]
            i += inc
            y_outptr[inc*(i - i0)] = y0 + yminscan
            x_outptr[inc*i] = x0 + xminscan
        y_outptr[0] = 0
        outputptr[0] += (y_outptr[1] - outputptr[0])*(outputptr[0] > y_outptr[1])
        outputptr[1] += (y_outptr[i-i0] - outputptr[1])*(outputptr[1] < y_outptr[i - i0])
    outputptr[2] = x_outptr[1]
    outputptr[3] = x_outptr[i]
    return output

@cython.boundscheck(False)
@cython.cdivision(True)
@cython.wraparound(False)
def bgrhsv(unsigned char[:,:,::1] image,long x, long y):
    cdef:
        unsigned char[:,:,::1] output = np.zeros((x,y,3),dtype = np.uint8)
        long x0,y0
        double b,g,r
        double chroma
    for x0 in range(x):
        for y0 in range(y):
            b = image[x0,y0,0]
            g = image[x0,y0,1]
            r = image[x0,y0,2]
            K = 0
            if g < b:
                g,b = b,g
                K = -6
            if r < g:
                r,g = g,r
                K =  -K - 2
            chroma = r - min(g,b)
            if chroma != 0:
                output[x0,y0,0] = int(30 * abs(K +((g-b)/(chroma))))
            if r != 0:
                output[x0,y0,1] = int(255* chroma/(r * 1.0))
            output[x0,y0,2] = int(r)
    return output

@cython.boundscheck(False)
@cython.cdivision(True)
@cython.wraparound(False)
def bgrhsvarray(unsigned char[:,:,::1] image,long x, long y):
    cdef:
        unsigned char* img_ptr = &image[0,0,0]
        unsigned long[:,::1] yaxis = np.zeros((3,256),dtype = np.uint32)
        unsigned long* yaxisptr = &yaxis[0,0]
        long x0,y0
        double b,g,r
        long hue,saturation
        double chroma
    for x0 in range(x):
        for y0 in range(y):
            b = img_ptr[3*(x0*y + y0)]
            g = img_ptr[3*(x0*y + y0) + 1]
            r = img_ptr[3*(x0*y + y0) + 2]
            K = 0
            if g < b:
                g,b = b,g
                K = -6
            if r < g:
                r,g = g,r
                K =  -K - 2
            chroma = r - min(g,b)
            if chroma != 0:
                hue = int(30 * abs(K +((g-b)/(chroma))))
            if r != 0:
                saturation = int(255* chroma/(r * 1.0))
            else:
                saturation = 0
            yaxisptr[hue] += 1
            yaxisptr[256 + saturation] += 1
            yaxisptr[256*2 + int(r)] += 1
    return yaxis
    
@cython.boundscheck(False)
@cython.cdivision(True)
@cython.wraparound(False)
def bgrhsvarray2(unsigned char[:,:,::1] image,long xmin,long xmax,long ymin, long ymax):
    cdef:
        unsigned char* img_ptr = &image[0,0,0]
        unsigned long[:,::1] yaxis = np.zeros((3,256),dtype = np.uint32)
        unsigned long* yaxisptr = &yaxis[0,0]
        long x0,y0
        double b,g,r
        long hue,saturation
        double chroma
        long deltax = xmax - xmin
        long deltay = ymax - ymin
    for x0 in range(deltax):
        for y0 in range(deltay):
            b = img_ptr[3*((xmin +x0)* 640 + y0 + ymin)]
            g = img_ptr[3*((xmin +x0)* 640 + y0 + ymin) + 1]
            r = img_ptr[3*((xmin +x0)* 640 + y0 + ymin) + 2]
            K = 0
            if g < b:
                g,b = b,g
                K = -6
            if r < g:
                r,g = g,r
                K =  -K - 2
            chroma = r - min(g,b)
            if chroma != 0:
                hue = int(30 * abs(K +((g-b)/(chroma))))
            if r != 0:
                saturation = int(255* chroma/(r * 1.0))
            else:
                saturation = 0
            yaxisptr[hue] += 1
            yaxisptr[256 + saturation] += 1
            yaxisptr[256*2 + int(r)] += 1
    return yaxis