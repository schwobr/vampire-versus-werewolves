# -*- coding: UTF-8 -*-
import socket
import argparse
import struct


class ClientThread():
    def __init__(self, buff_size):
        self.serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.buff_size=buff_size

    def connect(self, ip, port):
        self.serverSocket.connect((ip,port))
        print("Connection to %s on port %s" %(ip,port))
        data=input("Choose your name : ")
        self.send(["NME",len(data),data])    

    def receive_data(self, size, fmt):
    data = bytes()
    while len(data) < size:
        data += self.serverSocket.recv(size - len(data))
    return struct.unpack(fmt, data)

    def receive(self, expected):
        received = self.serverSocket.recv(3).decode("ascii") 
        if received==expected:  
            if received=="SET":
                data=bytes()
                n,m=self.receive_data(2,"2B")
                return [(n,m)]+self.receive("HUM")
            elif received=="HUM":
                res=[]
                n= self.receive_data(1,"1B")[0]
                homes= self.receive_data(2*n,"{}B".format(2*n))
                count=0
                prev=0
                for h in homes:
                    if count%2==0:
                        prev=h
                    else:
                        res.append((prev,h))
                    count++
                return res+self.receive("HME")
            elif received=="HME":
                start_pos=tuple(self.receive_data(2,"2B"))
                return [start_pos]
        else:
            print("Error at "+expected)

    def send(self, data):
        if data[0]=="NME":
            self.serverSocket.send(data[0].encode("ascii"))
            self.serverSocket.send(struct.pack("1B",6))
            name=input("Write your name here: ")
            self.serverSocket.send(name.encode("ascii")) 
            return self.receive("SET")
        elif data[0]=="MOV":
            return self.receive("UPD")






    


