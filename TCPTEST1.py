import numpy as np
#import TCPSOCK as tcps
from TCPSOCK import Interruptor
from threading import Thread

# Initialise class #
tcps = Interruptor()

#functions needed ##############################################
def wait_for_interrupts(classinit,threaded=False, epoll_timeout=1):
    """
    Blocking loop to listen for GPIO interrupts and distribute them to
    associated callbacks. epoll_timeout is an easy way to shutdown the
    blocking function. Per default the timeout is set to 1 second; if
    `_is_waiting_for_interrupts` is set to False the loop will exit.
    If an exception occurs while waiting for interrupts, the interrupt
    gpio interfaces will be cleaned up (/sys/class/gpio unexports). In
    this case all interrupts will be reset and you'd need to add the
    callbacks again before using `wait_for_interrupts(..)` again.
    If the argument `threaded` is True, wait_for_interrupts will be
    started in a daemon Thread. To quit it, call
    `RPIO.stop_waiting_for_interrupts()`.
    """
    if threaded:
        t = Thread(target=classinit.wait_for_interrupts, args=(epoll_timeout,))
        t.daemon = True
        t.start()
    else:
        classinit.wait_for_interrupts(epoll_timeout)

def cleanup(classinit):
    """
    Clean up by resetting all GPIO channels that have been used by this
    program to INPUT with no pullup/pulldown and no event detection. Also
    unexports the interrupt interfaces and callback bindings. You'll need
    to add the interrupt callbacks again before waiting for interrupts again.
    """
    classinit.cleanup_interrupts()
    classinit.stop_waiting_for_interrupts()
###############################################################

u1 = np.zeros((3),dtype=np.int32)
u2 = np.zeros((3),dtype=np.int32)

running1 = True
running2 = True
fr1 = 0
fr2 = 0
loop_count = 0

########### callbacks ######################################## 
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
			
##########set callbacks #####################################
tcps.add_tcp_callback(8000,socket_cb,threaded_callback =True)
tcps.add_tcp_callback(8080,socket_cb2,threaded_callback =True)
wait_for_interrupts(tcps,threaded=True)

##########   main loop #####################################

while running1 or running2:
	p1 = u1.copy()
	p2 = u2.copy()
	m1 = np.cross(p1,p2)
	m2 = np.cross(p1,p2)
	m3 = np.dot(m1,m2)
	print p1 + p2
	#print m3
	#print fr2 ': received', p2
	if (fr1 > 0) * (fr2 > 0):
		loop_count += 1

print fr1
print fr2
print 'loop count',loop_count
cleanup(tcps)
