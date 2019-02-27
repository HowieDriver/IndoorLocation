#!/usr/bin/python
from socket import *
import threading
def trans(sock1, BUFSIZ):
    while True:
        try:
            data = sock1.recv(BUFSIZ)
	    print data
        except OSError:
            break
        if not data:
            sock1.close()
    sock1.close()
	


if __name__ == '__main__':
    HOST = '192.168.1.111'
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
    Ser.close()
