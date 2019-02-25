#!/usr/bin/python
from socket import *
import threading
import time
from time import ctime


def recv(sock, BUFSIZ):
    while True:
        try:
            data = sock.recv(BUFSIZ)
	    print "From server:",data
	    time.sleep(1)
        except OSError:
            return  # find it was close, then close it
    sock.close()


if __name__ == '__main__':
    HOST = '192.168.1.125'
    POST = 21567
    ADDR = (HOST, POST)
    tcpCli = socket(AF_INET, SOCK_STREAM)

    tcpCli.connect(ADDR)

    threadrev = threading.Thread(target=recv, args=(tcpCli, 1024))
    threadrev.start()
    while True:
	data = "Hi, Server!\n"
        if not data:
            break
        tcpCli.send(data)
	time.sleep(1)
    tcpCli.close()
