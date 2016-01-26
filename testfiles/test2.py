import numpy as np
from pointaddress import pointerfirstreturn
a = np.array([2,3,4,6],dtype=np.uint8)
pointadd = pointerfirstreturn(a)
hexid = hex(id(a))
hexid0 = hex(id(a[0]))
afc = hex(a.__array_interface__['data'][0])
print ' pointadd', pointadd
print ' hexid', type(hexid)
print ' hexid0', hexid0
print 'array interface data',afc