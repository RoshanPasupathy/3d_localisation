# -*- coding: utf-8 -*-
#
# This file is part of RPIO.
#
# Copyright
#
#     Copyright (C) 2013 Chris Hager <chris@linuxuser.at>
#
# License
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Lesser General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details at
#     <http://www.gnu.org/licenses/lgpl-3.0-standalone.html>
#
# Documentation
#
#     http://pythonhosted.org/RPIO
#
import socket
import select
import os.path
import time
import atexit

from logging import debug, info, warn, error
from threading import Thread
from functools import partial

_TCP_SOCKET_HOST = "192.168.42.1"

def _threaded_callback(callback, *args):
    """
    Internal wrapper to start a callback in threaded mode. Using the
    daemon mode to not block the main thread from exiting.
    """
    t = Thread(target=callback, args=args)
    t.daemon = True
    t.start()


#def exit_handler():
#    """ Auto-cleanup on exit """
#    RPIO.stop_waiting_for_interrupts()
#    RPIO.cleanup_interrupts()

#atexit.register(exit_handler)

###################################start class######################################################

class Interruptor:
    """
    Object-based wrapper for interrupt management.
    """
    _epoll = select.epoll()
    _show_warnings = True


    # TCP socket stuff
    _tcp_client_sockets = {}  # { fileno: (socket, cb) }
    _tcp_server_sockets = {}  # { fileno: (socket, cb) }

    # Whether to continue the epoll loop or quit at next chance. You
    # can manually set this to False to stop `wait_for_interrupts()`.
    _is_waiting_for_interrupts = False

    def add_tcp_callback(self, port, callback, threaded_callback=False):
        """
        Adds a unix socket server callback, which will be invoked when values
        arrive from a connected socket client. The callback must accept two
        parameters, eg. ``def callback(socket, msg)``.
        """
        if not callback:
            raise AttributeError("No callback")

        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind((_TCP_SOCKET_HOST, port))
        serversocket.listen(1)
        serversocket.setblocking(0)
        self._epoll.register(serversocket.fileno(), select.EPOLLIN)

        # Prepare the callback (wrap in Thread if needed)
        cb = callback if not threaded_callback else \
                partial(_threaded_callback, callback)

        self._tcp_server_sockets[serversocket.fileno()] = (serversocket, cb)
        debug("Socket server started at port %s and callback added." % port)

    def close_tcp_client(self, fileno):
        debug("closing client socket fd %s" % fileno)
        self._epoll.unregister(fileno)
        socket, cb = self._tcp_client_sockets[fileno]
        socket.close()
        del self._tcp_client_sockets[fileno]

    def wait_for_interrupts(self, epoll_timeout=1):
        """
        Blocking loop to listen for GPIO interrupts and distribute them to
        associated callbacks. epoll_timeout is an easy way to shutdown the
        blocking function. Per default the timeout is set to 1 second; if
        `_is_waiting_for_interrupts` is set to False the loop will exit.
        If an exception occurs while waiting for interrupts, the interrupt
        gpio interfaces will be cleaned up (/sys/class/gpio unexports). In
        this case all interrupts will be reset and you'd need to add the
        callbacks again before using `wait_for_interrupts(..)` again.
        """
        self._is_waiting_for_interrupts = True
        while self._is_waiting_for_interrupts:
            events = self._epoll.poll(epoll_timeout)
            for fileno, event in events:
                debug("- epoll event on fd %s: %s" % (fileno, event))
                if event & select.EPOLLIN:
                    # Input from TCP socket
                    socket, cb = self._tcp_client_sockets[fileno]
                    content = socket.recv(142)
                    if not content or not content.strip():
                        # No content means quitting
                        self.close_tcp_client(fileno)
                    else:
                        sock, cb = self._tcp_client_sockets[fileno]
                        cb(self._tcp_client_sockets[fileno][0], \
                                content.strip())
                elif fileno in self._tcp_server_sockets:
                    # New client connection to socket server
                    serversocket, cb = self._tcp_server_sockets[fileno]
                    connection, address = serversocket.accept()
                    connection.setblocking(0)
                    f = connection.fileno()
                    self._epoll.register(f, select.EPOLLIN)
                    self._tcp_client_sockets[f] = (connection, cb)

                elif event & select.EPOLLHUP:
                    # TCP Socket Hangup
                    self.close_tcp_client(fileno)


    def stop_waiting_for_interrupts(self):
        """
        Ends the blocking `wait_for_interrupts()` loop the next time it can,
        which depends on the `epoll_timeout` (per default its 1 second).
        """
        self._is_waiting_for_interrupts = False


    def cleanup_tcpsockets(self):
        """
        Closes all TCP connections and then the socket servers
        """
        for fileno in self._tcp_client_sockets.keys():
            self.close_tcp_client(fileno)
        for fileno, items in self._tcp_server_sockets.items():
            socket, cb = items
            debug("- _cleanup server socket connection (fd %s)" % fileno)
            self._epoll.unregister(fileno)
            socket.close()
        self._tcp_server_sockets = {}

    def cleanup_interrupts(self):
        """
        Clean up all interrupt-related sockets and interfaces. Recommended to
        use before exiting your program! After this you'll need to re-add the
        interrupt callbacks before waiting for interrupts again.
        """
        self.cleanup_tcpsockets()
        # self.cleanup_interfaces()

#####################################end class######################################################
# Initialse interruptor class
_rpio = Interruptor()

def add_tcp_callback(port, callback, threaded_callback=False):
    """
    Adds a unix socket server callback, which will be invoked when values
    arrive from a connected socket client. The callback must accept two
    parameters, eg. ``def callback(socket, msg)``.
    """
    _rpio.add_tcp_callback(port, callback, threaded_callback)

def close_tcp_client(fileno):
    """ Closes TCP connection to a client and removes client from epoll """
    _rpio.close_tcp_client(fileno)


def wait_for_interrupts(threaded=False, epoll_timeout=1):
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
        t = Thread(target=_rpio.wait_for_interrupts, args=(epoll_timeout,))
        t.daemon = True
        t.start()
    else:
        _rpio.wait_for_interrupts(epoll_timeout)

def stop_waiting_for_interrupts():
    """
    Ends the blocking `wait_for_interrupts()` loop the next time it can,
    which depends on the `epoll_timeout` (per default its 1 second).
    """
    _rpio.stop_waiting_for_interrupts()


def cleanup_interrupts():
    """
    Removes all callbacks and closes used GPIO interfaces and sockets. After
    this you'll need to re-add the interrupt callbacks before waiting for
    interrupts again. Since RPIO v0.10.1 this is done automatically on exit.
    """
    _rpio.cleanup_interrupts()


def cleanup():
    """
    Clean up by resetting all GPIO channels that have been used by this
    program to INPUT with no pullup/pulldown and no event detection. Also
    unexports the interrupt interfaces and callback bindings. You'll need
    to add the interrupt callbacks again before waiting for interrupts again.
    """
    cleanup_interrupts()
    stop_waiting_for_interrupts()
    # _GPIO.cleanup()

