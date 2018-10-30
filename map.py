# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 10:10:20 2018

@author: hassenzarrouk
"""
import numpy as np


class Tray():
    
    def __init__(self, N, M, x, y, Map):        
        self.N=N
        self.M=M
        self.N_humans=0
        self.N_vampires=0
        self.N_werewolves=0
        self.humans=[]
        self.vampires=[]
        self.werewolves=[]
        self.MAP=np.zeros((N,M,2),int)
        self.UpdateTray(Map)
        self.Type=self.CheckPlayer(Map,x,y)


       
        
    def UpdateTray(self,liste):
        for element in liste:
            if element[2]!=0:
                self.MAP[element[1],element[0],0]=1
                self.MAP[element[1],element[0],1]=element[2]
            elif element[3]!=0:
                self.MAP[element[1],element[0],0]=2
                self.MAP[element[1],element[0],1]=element[3]
            else:
                self.MAP[element[1],element[0],0]=3
                self.MAP[element[1],element[0],1]=element[4]
            self.updateLists()
            self.count()
        
    def CheckPlayer(self,liste, x, y):
        for el in liste:
            if el[0]==x and el[1]==y:
                if el[3]!=0:
                    return 2
                elif el[4]!=0:
                    return 3
    
    def count(self):
        self.N_humans=0
        self.N_vampires=0
        self.N_werewolves=0
        for x in range(self.N):
            for y in range(self.M):
                if self.MAP[x,y,0]!=0:
                    i=self.MAP[x,y,0]
                    if i==1:
                        self.N_humans+=1
                    elif i==2:
                        self.N_vampires+=1
                    elif i==3:
                        self.N_werewolves+=1

    def updateLists(self):
        self.humans=[]
        self.vampires=[]
        self.werewolves=[]
        for x in range(self.N):
            for y in range(self.M):
                if self.MAP[x,y,0]!=0:
                    i=self.MAP[x,y,0]
                    j=self.MAP[x,y,1]
                    if i==1:
                        self.humans.append((y,x,j))
                    elif i==2:
                        self.vampires.append((y,x,j))
                    elif i==3:
                        self.werewolves.append((y,x,j))