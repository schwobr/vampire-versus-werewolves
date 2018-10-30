#!/usr/bin/env python3
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
        self.MAP=np.zeros(N,M)
        self.UpdateTray(self,Map)
        self.Type=self.CheckPlayer(self,Map,x,y)
        
        
        
    def UpdateTray(self,liste):
        for element in liste:
            if element[2]!=0:
                self.MAP[element[0],element[1]]=(1,element[2])
            elif element[3]!=0:
                self.MAP[element[0],element[1]]=(2,element[3])
            else:
                self.MAP[element[0],element[1]]=(3,element[4])
        
        
    def CheckPlayer(self,liste, x, y):
        for el in liste:
            if el[0]==x and el[1]==y:
                if el[3]!=0:
                    return 2
                elif el[4]!=0:
                    return 3
    
    
    