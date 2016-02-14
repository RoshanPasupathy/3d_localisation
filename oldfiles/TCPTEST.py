import numpy as np
import TCPSOCK as tcps

u1 = np.zeros((3),dtype=np.int32)
u2 = np.zeros((3),dtype=np.int32)

running1 = True
running2 = True
fr1 = 0
fr2 = 0
loop_count = 0 
def socket_cb(socket,val):
	global u2,running1,fr1
	if val[0] == 's':
		u2 = np.loads(val[1:])
		fr1 += 1
	elif val[0] == 'e':
		running1 = False
		
def socket_cb2(socket,val):
	global u1,running2,fr2
	if val[0] == 's':
		u1 = np.loads(val[1:])
		fr2 += 1
	elif val[0] == 'e':
		running2 = False
			

tcps.add_tcp_callback(8000,socket_cb,threaded_callback =True)
tcps.add_tcp_callback(8080,socket_cb2,threaded_callback =True)
tcps.wait_for_interrupts(threaded=True)

while running1 or running2:
	p1 = u1.copy()
	p2 = u2.copy()
	m1 = np.cross(p1,p2)
	m2 = np.cross(p1,p2)
	m3 = np.dot(m1,m2)
	print p1 + p2
	#print m3
	#print fr2 ': received', p2
	loop_count += 1

print fr1
print fr2
print 'loop count',loop_count
tcps.cleanup()
