#coding: utf-8
import socket

class ClientThread():
    def __init__(self):
        self.serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def connect(self, ip, port):
        self.serverSocket.connect((ip,port))
        print("Connection to %s on port %s" %(ip,port))

    def receive(self, buff_size):
        res=self.serverSocket.recv(buff_size)

    def send(self, data):
        self.serverSocket.send(data)
    

TCP_IP = "127.0.0.1"
TCP_PORT = 5555
BUFFER_SIZE = 1024
