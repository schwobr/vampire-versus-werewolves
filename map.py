# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 10:10:20 2018

@author: hassenzarrouk
"""
import numpy as np

class Tray():
    
    def __init__(self, N, M, x, y, Map):        
        self.N = N
        self.M = M
        self.N_humans = 0
        self.N_vampires = 0
        self.N_werewolves = 0
        self.humans = []
        self.vampires = []
        self.werewolves = []
        self.MAP = np.zeros((N, M, 2), int)
        self.UpdateTray(Map)
        self.Type = self.CheckPlayer(Map, x, y)
     
        
    def UpdateTray(self, liste):
        for element in liste:
            if element[2] != 0:
                self.MAP[element[1], element[0], 0] = 1
                self.MAP[element[1], element[0], 1] = element[2]
            elif element[3] != 0:
                self.MAP[element[1], element[0], 0] = 2
                self.MAP[element[1] ,element[0], 1] = element[3]
            elif element[4] != 0:
                self.MAP[element[1], element[0], 0] = 3
                self.MAP[element[1], element[0], 1] = element[4]
            else:
                self.MAP[element[1], element[0], 0] = 0
                self.MAP[element[1], element[0], 1] = 0
            self.updateLists()
            self.count()
        
    def CheckPlayer(self, liste, x, y):
        for el in liste:
            if el[0] == x and el[1] == y:
                if el[3] != 0:
                    return 2
                elif el[4] != 0:
                    return 3
    
    def count(self):
        self.N_humans = 0
        self.N_vampires = 0
        self.N_werewolves = 0
        for x in range(self.N):
            for y in range(self.M):
                if self.MAP[x, y, 0] != 0:
                    i = self.MAP[x, y, 0]
                    if i == 1:
                        self.N_humans += 1
                    elif i == 2:
                        self.N_vampires += 1
                    elif i == 3:
                        self.N_werewolves += 1

    def updateLists(self):
        self.humans = []
        self.vampires = []
        self.werewolves = []
        for x in range(self.N):
            for y in range(self.M):
                if self.MAP[x, y, 0] != 0:
                    i = self.MAP[x, y, 0]
                    j = self.MAP[x, y, 1]
                    if i == 1:
                        self.humans.append((y, x, j))
                    elif i == 2:
                        self.vampires.append((y, x, j))
                    elif i == 3:
                        self.werewolves.append((y, x, j))

    def stupidAI(self):
        moves = []
        test = self.Type == 2
        us = self.vampires if test else self.werewolves
        them = self.werewolves if test else self.vampires
        n=0
        for u in us:
            x = 0
            y = 0
            mini = 100000
            if self.N_humans>0:
                for h in self.humans:
                    d = (h[0] - u[0])**2 + (h[1] - u[1])**2
                    if d < mini :
                        mini = d
                        x = h[0]
                        y = h[1]
            else :
                for t in them:
                    d = (t[0] - u[0])**2 + (t[1] - u[1])**2
                    if d < mini :
                        mini = d
                        x = t[0]
                        y = t[1]
            moves.append(u[0])
            moves.append(u[1])
            moves.append(u[2])
            moves.append(u[0] + np.sign(x - u[0]))
            moves.append(u[1] + np.sign(y - u[1]))
            n += 1
        print(moves)
        return ["MOV", n, moves]

    def IsTerminal(self):
        return self.N_vampires == 0 or self.N_werewolves == 0

    def GetChildren(self, maxSplit):
        res = []
        test = self.Type == 2
        us = self.vampires if test else self.werewolves
        them = self.werewolves if test else self.vampires        
        for u in us:
            moves = []
            n = u[2]
            x = u[0]
            y = u[1]
            for i in range(1, maxSplit+1):
                sums = SubSum(i, n)
                #for s in sums:


        return res

    def GetMoves(self, x, y):
        moves_x = [x]
        moves_y = [y]
        moves = []
        if x != 0:
            moves_x.append(x - 1)
        if x != self.M:
            moves_x.append(x + 1)
        if y != 0:
            moves_y.append(y - 1)
        if y != self.N:
            moves_y.append(y + 1)
        for m_x in moves[x]:
            for m_y in moves[y]:
                moves.append(m_x, m_y)
        return moves


def SubSum(splits, n):
    if splits == 1:
        return [np.array([n])]
    else:
        l = []
        for i in range(1, int(n/2)+1):
            prec = SubSum(splits - 1, n - i)
            for p in prec:
                res = np.zeros(splits, dtype = int)
                res[0] = i
                test = True
                for j in range(1, res.shape[0]):
                    test = res[j - 1] <= p[j - 1]
                    if test:
                        res[j] = p[j - 1]
                    else:
                        break
                if test:
                    l.append(res)
        return l

