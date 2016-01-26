cimport cython

def pointerfirstreturn(unsigned char[::1] inarray):
        cdef unsigned char *inptr = &inarray[0]
        return &inarray[0]

#def pointerreturn(unsigned char[::1] inarray):
        #cdef unsigned char *inptr = &inarray
        #return &inarray

