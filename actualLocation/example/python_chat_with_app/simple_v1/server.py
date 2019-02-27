#!/usr/bin/python
import socket

try:
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    sock.bind(('192.168.1.125',21567))
    sock.listen(5)
except:
    print("init socket error!")

while True:
    conn,addr=sock.accept()
    conn.settimeout(30)
    szBuf=conn.recv(1024)
    print "From app:", szBuf

    if "0"==szBuf:
        conn.send(b"exit")
    else:
        conn.send(b"welcome client")

    conn.close()

