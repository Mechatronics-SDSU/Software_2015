'''
Created on Jun 11, 2015

@author: Jard
'''
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind(("", 5006))

while 1:
    data, addr = sock.recvfrom(1024)
    print data