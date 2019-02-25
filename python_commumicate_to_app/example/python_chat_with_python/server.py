#!/usr/bin/python
from socket import *
import threading
import time
def trans(sock1, BUFSIZ):
    while True:
        try:
            data = sock1.recv(BUFSIZ)
	    if data:
	    	print "From app:",data
		time.sleep(1)
        except OSError:
            break       
    sock1.close()


if __name__ == '__main__':
    HOST = '192.168.1.125'
    POST = 21567
    ADDR = (HOST, POST)
    Ser = socket(AF_INET, SOCK_STREAM)
    Ser.bind(ADDR)
    Ser.listen(3)

    tcpCli, addr = Ser.accept()
    trans1 = threading.Thread(target=trans, args=(tcpCli, 1024))
    trans1.start()

    while True:
	tcpCli.send("Hi, Client!\n")
	time.sleep(1)
    Ser.close()
