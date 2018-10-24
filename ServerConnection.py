#coding: utf-8
import socket

class ClientThread():
    def __init__(self, buff_size):
        self.serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.buff_size=buff_size

    def connect(self, ip, port):
        self.serverSocket.connect((ip,port))
        print("Connection to %s on port %s" %(ip,port))
        data=input("Choose your name : ")
        self.send("NME "+data.length+" "+data)    

    def receive(self):
        return self.serverSocket.recv(self.buff_size)

    def send(self, data):
        self.serverSocket.send(data)
        parsedData=data.split(" ")
        if parsedData[0]=="NME":
            self.receive()

    

TCP_IP = "127.0.0.1"
TCP_PORT = 5555
BUFFER_SIZE = 1024
