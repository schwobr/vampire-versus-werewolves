# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 10:10:20 2018

@author: hassenzarrouk
"""
import numpy as np
import random as rd

class Tray():
    
    def __init__(self, N, M, Map, x = None, y = None, Type = None, ):        
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
        if Type == None:
            self.Type = self.CheckPlayer(Map, x, y)
        else:
            self.Type = Type

        
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
        test = self.Type == 2
        us = self.vampires if test else self.werewolves    
        all_moves = []  
        for u in us:
            n = u[2]
            x = u[0]
            y = u[1]
            moves = self.GetMoves(x, y)
            moves_u = []
            for i in range(1, maxSplit+1):
                sums = SubSum(i, n)
                for s in sums:
                    submoves = SubMoves(moves, s)
                    moves_u += submoves
            all_moves.append(moves_u)
        return self.GetUpdates(all_moves)

    def GetMoves(self, x, y):
        moves_x = [x]
        moves_y = [y]
        moves = []
        if x != 0:
            moves_x.append(x - 1)
        if x != self.M - 1:
            moves_x.append(x + 1)
        if y != 0:
            moves_y.append(y - 1)
        if y != self.N - 1:
            moves_y.append(y + 1)
        for m_x in moves_x:
            for m_y in moves_y:
                moves.append((x, y, m_x, m_y))
        return moves

    def GetUpdates(self, all_moves):
        if len(all_moves) == 1:
            updates = []
            moves = all_moves[0]
            for move in moves:
                n = 0
                upd = []
                for sub_move in move:
                    m = [sub_move[2], sub_move[3], 0, 0, 0]
                    if not(sub_move[3] == sub_move[1] and sub_move[2] == sub_move[0]):
                        n += sub_move[4]
                        if self.MAP[sub_move[3], sub_move[2], 0] == self.Type:
                            m[1 + self.Type] = self.MAP[sub_move[3], sub_move[2], 1] + sub_move[4]
                        elif self.MAP[sub_move[3], sub_move[2], 0] == 1:
                            if sub_move[4] >= self.MAP[sub_move[3], sub_move[2], 1]:
                                m[1 + self.Type] = self.MAP[sub_move[3], sub_move[2], 1] + sub_move[4]
                            else : 
                                (win, n1) = RandomBattle(sub_move[4], self.MAP[sub_move[3], sub_move[2], 1], True)
                                if win:
                                    m[1 + self.Type] = n1
                                else:
                                    m[2] = n1
                        else:
                            if sub_move[4] >= 1.5 * self.MAP[sub_move[3], sub_move[2], 1]:
                                m[1 + self.Type] = sub_move[4]
                            elif self.MAP[sub_move[3], sub_move[2], 1] < 1.5 * sub_move[4]:
                                (win, n1) = RandomBattle(sub_move[4], self.MAP[sub_move[3], sub_move[2], 1], False)
                                if win:
                                    m[1 + self.Type] = n1
                                else:
                                    m[6 - self.Type] = n1
                        upd.append(tuple(m))
                m = [sub_move[0], sub_move[1], 0, 0, 0]
                m[1 + self.Type] = self.MAP[sub_move[1], sub_move[0], 1] - n
                upd.append(tuple(m))
                updates.append(upd)
            return updates
        else:
            moves = all_moves.pop(0)
            updates = self.GetUpdates([moves])
            res = []
            for upd in updates:
                tray = Tray(self.N, self.M, [], Type = self.Type)
                tray.MAP = np.copy(self.MAP)
                tray.UpdateTray(upd)
                other_updates = tray.GetUpdates(all_moves)
                for other_upd in other_updates:
                    res.append(upd + other_upd)
            return res            
    
            
def Fusion(tray1 : Tray, tray2 : Tray):
    newTray = Tray(tray1.N, tray1.M, [], Type = tray1.Type)
    newTray.MAP = np.copy(tray1.MAP)
    for i in range(tray1.N):
        for j in range(tray1.M):
            if tray1.MAP[i, j, 0] != tray2.MAP[i, j, 0] or tray1.MAP[i, j, 1] != tray1.MAP[i, j, 1]:
                if tray1.MAP[i, j, 0] == tray1.Type and tray2.MAP[i, j , 0] == tray2.Type:
                    newTray.MAP[i, j, 1] = max(tray1.MAP[i, j , 1], tray2.MAP[i, j, 1])
                elif tray1.MAP[i, j, 0] != tray1.Type and tray2.MAP[i, j , 0] != tray2.Type:
                    newTray.MAP[i, j, 1] = min(tray1.MAP[i, j, 1], tray2.MAP[i, j, 1])
                elif tray2.MAP[i, j, 0] == tray2.Type:
                    newTray.MAP[i, j, 0] = tray2.MAP[i, j, 0]
                    newTray.MAP[i, j, 1] = tray2.MAP[i, j ,1]
    newTray.updateLists()
    return newTray 

def RandomBattle(attack, defend, humans):
    n = 0
    r = rd.random()
    p = attack / (2 * defend) if attack <= defend else attack / defend - 0.5
    if p >= r:
        for i in range(attack):
            r = rd.random()
            if p >= r:
                n += 1
        if humans:
            for i in range(defend):
                r = rd.random()
                if p >= r:
                    n += 1
        return (True, n)
    else:
        for i in range(defend):
            r = rd.random()
            if 1 - p >= r:
                n += 1
        return (False, n)


def SubMoves(moves, sum):
    if sum.shape[0] == 1:
        return [[(m[0], m[1], m[2], m[3], sum[0])] for m in moves]
    else:
        res = []
        for i in range(len(moves)):
            m = moves.pop(0)
            sum_b = sum[1:]
            submoves = SubMoves(moves, sum_b)
            for submove in submoves:
                res.append([(m[0], m[1], m[2], m[3], sum[0])] + submove)
            moves.append(m)
        return res

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

