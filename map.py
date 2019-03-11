# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 10:10:20 2018

@author: hassenzarrouk
"""
import numpy as np
from itertools import permutations

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

        
    def __eq__(self, tray):
        return self.humans == tray.humans and self.vampires == tray.vampires and self.werewolves == tray.werewolves

    def __ne__(self, tray):
        return not(self.__eq__(tray))

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
        
    def CheckPlayer(self, liste, x, y):
        for el in liste:
            if el[0] == x and el[1] == y:
                if el[3] != 0:
                    return 2
                elif el[4] != 0:
                    return 3
    
    def count(self):
        self.N_humans = np.sum([h[2] for h in self.humans])
        self.N_vampires = np.sum([v[2] for v in self.vampires])
        self.N_werewolves = np.sum([w[2] for w in self.werewolves])

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
        self.count()

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


    def GetChildren(self, maxSplit : int):
        """Returns the list of all possible children of the tray as lists of updates and moves
        
        :param maxSplit: maximum number of subgroups that can be present on the board
        :type maxSplit: int
        :return: List of all possible children. Each child is represented by a list of dictionnaries that contain a MOV 5-uplet and a UPD 5-uplet
        :rtype: list[list[dict, tuple[int, int, int , int]]
        """
        test = self.Type == 2
        us = self.vampires if test else self.werewolves   
        moves_groups = [self.GetMoves(u[0], u[1]) for u in us]
        all_moves = []  
        n_groups = len(us)
        divisions = SubSum(n_groups, maxSplit)
        for div in divisions:
            possible = set(permutations(div))
            for p in possible:
                div_moves = []
                for k, u in enumerate(us):
                    n = u[2]
                    m = p[k]
                    moves_group = moves_groups[k]
                    submoves_group = []
                    for i in range(1, m + 1):
                        subsums = SubSum(i, n)
                        for s in subsums:
                            submoves = SubMoves(moves_group, s)
                            submoves_group += submoves
                    div_moves.append(submoves_group)
                all_moves += self.GetUpdates(div_moves)
        return all_moves

    def GetMoves(self, x : int, y : int):
        """
        Given a position, gets all the accessible positions from there

        :param x: absciss
        :param y: ordinate
        :type x: int
        :type y: int
        :return: list of 4-uplets where the first 2 elements represent the starting position and the last 2 
        the ending position of a move
        :rtype: list[tuple[int, int, int, int]]
        """
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

    def GetUpdates(self, all_moves : list):
        """
        Given the list of all possible moves, returns the list of all possible update lists with same format as server's UPD packages. Every update is associated with the corresponding MOV request

        :param all_moves: List of list. Each sublist corresponds to a group of allied creatures on the board and contains other sublists, that themselves contain a set of compatible moves from this group
        :type all_moves: list[list[list[tuple[int, int, int, int, int]]]]
        :return: A list of list of compatible updates. Every sublist contains dictionaries that contain the UPD 5-uplet and the MOV 5-uplet, and all these dictionaries are moves that can be performed the same turn
        :rtype: list[list[[dict, tuple[int, int, int, int, int]]]]
        """
        if len(all_moves) == 1:
            updates = []
            submoves_group = all_moves[0]
            for submoves in submoves_group:
                n = 0
                upd = []
                for submove in submoves:
                    m = [submove[3], submove[4], 0, 0, 0]
                    if not(submove[4] == submove[1] and submove[3] == submove[0]):
                        n += submove[2]
                        if self.MAP[submove[4], submove[3], 0] == self.Type:
                            m[1 + self.Type] = self.MAP[submove[4], submove[3], 1] + submove[2]
                        elif self.MAP[submove[4], submove[3], 0] == 1:
                            if submove[2] >= self.MAP[submove[4], submove[3], 1]:
                                m[1 + self.Type] = self.MAP[submove[4], submove[3], 1] + submove[2]
                            else : 
                                (win, n1) = RandomBattle(submove[2], self.MAP[submove[4], submove[3], 1], True)
                                if win:
                                    m[1 + self.Type] = n1
                                else:
                                    m[2] = n1
                        else:
                            if submove[2] >= 1.5 * self.MAP[submove[4], submove[3], 1]:
                                m[1 + self.Type] = submove[2]
                            elif self.MAP[submove[4], submove[3], 1] < 1.5 * submove[2]:
                                (win, n1) = RandomBattle(submove[2], self.MAP[submove[4], submove[3], 1], False)
                                if win:
                                    m[1 + self.Type] = n1
                                else:
                                    m[6 - self.Type] = n1
                        m1 = [submove[0], submove[1], 0, 0, 0]
                        m1[1 + self.Type] = self.MAP[submove[1], submove[0], 1] - n                        
                        upd.append({'UPD' : [tuple(m), tuple(m1)], 'MOV' : tuple(submove)})
                updates.append(upd)
            return updates
        else:
            submoves_group = all_moves.pop(0)
            updates = self.GetUpdates([submoves_group])
            res = []
            for upd in updates:
                tray = Tray(self.N, self.M, [], Type = self.Type)
                tray.MAP = np.copy(self.MAP)
                up = []
                for u in upd:
                    up += [u['UPD'][0], u['UPD'][1]]
                tray.UpdateTray(up)
                other_updates = tray.GetUpdates(all_moves)
                for other_upd in other_updates:
                    res.append(upd + other_upd)
            return res            


def RandomBattle(attack : int, defend : int, humans : bool):
    """
    Finds the most probable result of a random battle (if probability that attackers win is 0.5, we suppose that they win)
    
    :param attack: number of attackers
    :param defend: number of defenders
    :param humans: boolean such that True means that defenders are humans, false means they are not
    :type attack: int
    :type defend: int
    :type humans: bool
    :return: couple composed of a boolean assigned to True if attackers won, and an int that represents the mean number of survivors after the battle
    :rtype: tuple[bool, int]

    :Example:

    >>> RandomBattle(5, 6, True)
    (False, 3)
    """
    p = attack / (2 * defend) if attack <= defend else attack / defend - 0.5
    if p >= 0.5:
        surv = attack * p
        if humans:
            surv += defend * p
        return (True, int(surv))
    else:
        surv = defend * (1 - p)
        return (False, int(surv))


def SubMoves(moves : list, subsum : list):
    """
    Given a set of possible moves from a cell that contains n creatures and a subsum list of k-size arrays, gives all the possible submoves created by splitting the n elements in k
    
    :param moves: List of 4-uplets that represent all possible moves from a cell. For each 4-uplet, the first two elements represent the position of origin, and the last 2 the position of arrival
    :param subsum: k-size (k fixed) array such that the sum of all elements of the array is n 
    :type moves: list[tuple[int, int, int, int]]
    :type subsum: list[array[int]]
    :return: List of len(moves) sublists. Each sublist contains k 5-uplets that represents a move with the same format as the MOV request. The sum of all 3rd elements of a sublist is n. 
    :rtype: list[list[tuple[int, int, int, int, int]]]

    :Example:

    >>> moves = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1)]
    >>> subsum = np.array([1, 3])
    >>> SubMoves(moves, subsum)
    [[(0, 0, 1, 0, 1), (0, 0, 3, 1, 0)],
     [(0, 0, 1, 0, 1), (0, 0, 3, 1, 1)],
     [(0, 0, 1, 1, 0), (0, 0, 3, 1, 1)],
     [(0, 0, 1, 1, 0), (0, 0, 3, 0, 1)],
     [(0, 0, 1, 1, 1), (0, 0, 3, 0, 1)],
     [(0, 0, 1, 1, 1), (0, 0, 3, 1, 0)]]
    """
    if subsum.shape[0] == 1:
        return [[(m[0], m[1], subsum[0], m[2], m[3])] for m in moves]
    else:
        res = []
        for _ in range(len(moves)):
            m = moves.pop(0)
            sum_b = subsum[1:]
            submoves = SubMoves(moves, sum_b)
            for submove in submoves:
                res.append([(m[0], m[1], subsum[0], m[2], m[3])] + submove)
            moves.append(m)
        return res

def SubSum(k : int, n : int):
    """
    Computes all the k-uplets that sum to n

    :param k: Represents the number of elements to be summed
    :param n: Represents the result to be found
    :type k: int
    :type k: int
    :return: List of arrays of size k such that the sum of all elements of an array is n
    :rtype: list[array[int]]

    :Example:

    >>> k = 2
    >>> n = 5
    >>> SubSum(k, n)
    [array([1, 4]), array([2, 3])]
    """
    if k == 1:
        return [np.array([n])]
    else:
        subsums = []
        for i in range(1, int(n / 2) + 1):
            prec = SubSum(k - 1, n - i)
            for p in prec:
                res = np.zeros(k, dtype = int)
                res[0] = i
                test = True
                for j in range(1, res.shape[0]):
                    test = res[j - 1] <= p[j - 1]
                    if test:
                        res[j] = p[j - 1]
                    else:
                        break
                if test:
                    subsums.append(res)
        return subsums

