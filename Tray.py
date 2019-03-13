# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 10:10:20 2018

@author: hassenzarrouk
"""
import numpy as np
from itertools import permutations, zip_longest
import concurrent.futures
#   import multiprocessing

class Tray():
    
    def __init__(self, N, M, upd, x = None, y = None, Type = None, ):        
        self.N = N
        self.M = M
        self.N_humans = 0
        self.N_vampires = 0
        self.N_werewolves = 0
        self.Humans = []
        self.Vampires = []
        self.Werewolves = []
        self.Grid = np.zeros((N, M, 2), int)
        self.UpdateTray(upd)
        if Type == None:
            self.Type = self.CheckPlayer(upd, x, y)
        else:
            self.Type = Type

        
    def __eq__(self, tray):
        return self.Humans == tray.Humans and self.Vampires == tray.Vampires and self.Werewolves == tray.Werewolves and self.Type == tray.Type

    def __ne__(self, tray):
        return not(self.__eq__(tray))

    def UpdateTray(self, liste, is_upd = True):
        if is_upd:
            for upd in liste:
                if upd[2] != 0:
                    self.Grid[upd[1], upd[0], 0] = 1
                    self.Grid[upd[1], upd[0], 1] = upd[2]
                elif upd[3] != 0:
                    self.Grid[upd[1], upd[0], 0] = 2
                    self.Grid[upd[1] ,upd[0], 1] = upd[3]
                elif upd[4] != 0:
                    self.Grid[upd[1], upd[0], 0] = 3
                    self.Grid[upd[1], upd[0], 1] = upd[4]
                else:
                    self.Grid[upd[1], upd[0], 0] = 0
                    self.Grid[upd[1], upd[0], 1] = 0
        else:
            for mov in liste:
                self.Grid[mov[1], mov[0], 1] -= mov[2]
                if self.Grid[mov[1], mov[0], 1] == 0:
                    self.Grid[mov[1], mov[0], 0] = 0
                if self.Grid[mov[4], mov[3], 0] == self.Type:
                    self.Grid[mov[4], mov[4], 1] += mov[2]
                elif self.Grid[mov[4], mov[3], 0] == 0:
                    self.Grid[mov[4], mov[3], 0] = self.Type
                    self.Grid[mov[4], mov[3], 1] = mov[2]
                elif self.Grid[mov[4], mov[3], 0] == 1:
                    if mov[2] >= self.Grid[mov[4], mov[3], 1]:
                        self.Grid[mov[4], mov[3], 0] = self.Type
                        self.Grid[mov[4], mov[3], 1] += mov[2]
                    else : 
                        (win, surv) = randomBattle(mov[2], self.Grid[mov[4], mov[3], 1], True)
                        if surv == 0:
                            self.Grid[mov[4], mov[3], 0] = 0
                        elif win:
                            self.Grid[mov[4], mov[3], 0] = self.Type
                        self.Grid[mov[4], mov[3], 1] = surv
                else:
                    if mov[2] >= 1.5 * self.Grid[mov[4], mov[3], 1]:
                        self.Grid[mov[4], mov[3], 0] = self.Type
                        self.Grid[mov[4], mov[3], 1] = mov[2]
                    elif self.Grid[mov[4], mov[3], 1] < 1.5 * mov[2]:
                        (win, surv) = randomBattle(mov[2], self.Grid[mov[4], mov[3], 1], False)
                        if surv == 0:
                            self.Grid[mov[4], mov[3], 0] = 0
                        elif win:
                            self.Grid[mov[4], mov[3], 0] = self.Type
                        self.Grid[mov[4], mov[3], 1] = surv
        self.UpdateLists()
        
    def CheckPlayer(self, liste, x, y):
        for el in liste:
            if el[0] == x and el[1] == y:
                if el[3] != 0:
                    return 2
                elif el[4] != 0:
                    return 3
    
    def Count(self):
        self.N_humans = np.sum([h[2] for h in self.Humans])
        self.N_vampires = np.sum([v[2] for v in self.Vampires])
        self.N_werewolves = np.sum([w[2] for w in self.Werewolves])

    def UpdateLists(self):
        self.Humans = []
        self.Vampires = []
        self.Werewolves = []
        for x in range(self.N):
            for y in range(self.M):
                if self.Grid[x, y, 0] != 0:
                    i = self.Grid[x, y, 0]
                    j = self.Grid[x, y, 1]
                    if i == 1:
                        self.Humans.append((y, x, j))
                    elif i == 2:
                        self.Vampires.append((y, x, j))
                    elif i == 3:
                        self.Werewolves.append((y, x, j))
        self.Count()
    
    def StupidAI(self):
        moves = []
        test = self.Type == 2
        us = self.Vampires if test else self.Werewolves
        them = self.Werewolves if test else self.Vampires
        n=0
        for u in us:
            x = 0
            y = 0
            mini = 100000
            if self.N_humans>0:
                for h in self.Humans:
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

    def Win(self):
        if self.Type==2:
            return self.N_werewolves==0 and self.N_vampires>0
        else:
             return self.N_vampires==0 and self.N_werewolves>0


    def GetEdges(self, maxSplit : int):
        """Returns the list of all possible children of the tray as lists of updates and moves
        
        :param maxSplit: maximum number of subgroups that can be present on the board
        :type maxSplit: int
        :return: List of all possible children. Each child is represented by a list of dictionnaries that contain a MOV 5-uplet and a UPD 5-uplet
        :rtype: list[list[dict, tuple[int, int, int , int]]
        """
        test = self.Type == 2
        us = self.Vampires if test else self.Werewolves   
        moves_all_groups = [self.GetMoves(u[0], u[1]) for u in us]
        all_moves = []  
        n_groups = len(us)
        for n_splits in range(1, maxSplit+1):
            splits = possibleSplits(n_groups, n_splits)
            for split in splits:
                splits_permutations = set(permutations(split))
                for permutation in splits_permutations:
                    split_moves = []
                    for k, u in enumerate(us):
                        n = u[2]
                        m = permutation[k]
                        moves_group = moves_all_groups[k]
                        all_moves_group = []
                        group_splits = possibleSplits(m, n)
                        for group_split in group_splits:
                            all_moves_group += splitMoves(moves_group, group_split)
                        split_moves.append(all_moves_group)
                    all_moves += getAllMoves(split_moves)
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

    def Heuristic(self, nodeType : int):
        if self.Type == 2:
            if nodeType == 1:
                us = self.Vampires
                them = self.Werewolves
                N_us = self.N_vampires
                N_them = self.N_werewolves
            else:
                them = self.Vampires
                us = self.Werewolves
                N_them = self.N_vampires
                N_us = self.N_werewolves
        else:
            if nodeType == 1:
                them = self.Vampires
                us = self.Werewolves
                N_them = self.N_vampires
                N_us = self.N_werewolves
            else:
                us = self.Vampires
                them = self.Werewolves
                N_us = self.N_vampires
                N_them = self.N_werewolves
        heuristic = 100 * (N_us - N_them) 
        try:
            d_hum_us = np.sum([np.min([max(abs(u[0]-hum[0]), abs(u[1]-hum[1])) for hum in self.Humans if u[2]>=hum[2]]) for u in us])
        except:
            d_hum_us = 0
        try:
            d_hum_them = np.sum([np.min([max(abs(t[0]-hum[0]), abs(t[1]-hum[1])) for hum in self.Humans if t[2]>=hum[2]]) for t in them])
        except:
            d_hum_them = 0
        heuristic -= 10 * (d_hum_us - d_hum_them)
        dmax = max(self.N, self.M)
        for u in us:
            d_min = 10000
            en_min = (0, 0, 0)
            res = 0
            for en in them:
                d = max(abs(en[0]-u[0]), abs(en[1]-u[1])) 
                if d < d_min:
                    d_min = d
                    en_min = en
            if en_min[2]>=1.5*u[2]:
                res = -10*en_min[2]*(dmax-d_min)
            elif u[2] >= 1.5*en_min[2]:
                res = 10*u[2]*(dmax-d_min)
            else:
                win1, res1 = randomBattle(u[2], en_min[2], False)
                win2, res2 = randomBattle(en_min[2], u[2], False)               
                if win1:
                    res+= res1*(dmax-d_min)
                else:
                    res -= res1*(dmax-d_min)
                if win2:
                    res -= res2*(dmax-d_min)
                else:
                    res += res2*(dmax-d_min)
            heuristic += res
        return heuristic




def randomBattle(attack : int, defend : int, humans : bool):
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

    >>> randomBattle(5, 6, True)
    (False, 3)
    """
    p = attack / (2 * defend) if attack <= defend else attack / defend - 0.5
    if p > 0.5:
        surv = attack * p
        if humans:
            surv += defend * p
        return (True, int(surv))
    else:
        surv = defend * (1 - p)
        return (False, int(surv))


def splitMoves(moves : list, splits : list):
    """
    Given a set of possible moves from a cell that contains n creatures and a splits list of k-size arrays, gives all the possible splitMoves created by splitting the n elements in k
    
    :param moves: List of 4-uplets that represent all possible moves from a cell. For each 4-uplet, the first two elements represent the position of origin, and the last 2 the position of arrival
    :param splits: k-size (k fixed) array such that the sum of all elements of the array is n 
    :type moves: list[tuple[int, int, int, int]]
    :type splits: list[array[int]]
    :return: List of len(moves) sublists. Each sublist contains k 5-uplets that represents a move with the same format as the MOV request. The sum of all 3rd elements of a sublist is n. 
    :rtype: list[list[tuple[int, int, int, int, int]]]

    :Example:

    >>> moves = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1)]
    >>> splits = np.array([1, 3])
    >>> splitMoves(moves, splits)
    [[(0, 0, 1, 0, 1), (0, 0, 3, 1, 0)],
     [(0, 0, 1, 0, 1), (0, 0, 3, 1, 1)],
     [(0, 0, 1, 1, 0), (0, 0, 3, 1, 1)],
     [(0, 0, 1, 1, 0), (0, 0, 3, 0, 1)],
     [(0, 0, 1, 1, 1), (0, 0, 3, 0, 1)],
     [(0, 0, 1, 1, 1), (0, 0, 3, 1, 0)]]
    """
    if splits.shape[0] == 1:
        return [[(m[0], m[1], splits[0], m[2], m[3])] for m in moves]
    else:
        split_moves = []
        for _ in range(len(moves)):
            m = moves.pop(0)
            splits_rest = splits[1:]
            split_moves_rest = splitMoves(moves, splits_rest)
            for split_move in split_moves_rest:
                split_moves.append([(m[0], m[1], splits[0], m[2], m[3])] + split_move)
            moves.append(m)
        return split_moves

def possibleSplits(n_splits : int, n_elements : int):
    """
    Computes all the n_splits-uplets that sum to n

    :param n_splits: Represents the number of elements to be summed
    :param n_elements: Represents the result to be found
    :type n_splits: int
    :type n_elements: int
    :return: List of arrays of size n_splits such that the sum of all elements of an array is n_elements
    :rtype: list[array[int]]

    :Example:

    >>> n_splits = 2
    >>> n_elements = 5
    >>> possibleSplits(n_splits, n_elements)
    [array([1, 4]), array([2, 3])]
    """
    if n_splits == 1:
        return [np.array([n_elements])]
    else:
        splits = []
        for i in range(1, int(n_elements / 2) + 1):
            sub_splits = possibleSplits(n_splits - 1, n_elements - i)
            for sub_split in sub_splits:
                split = np.zeros(n_splits, dtype = int)
                split[0] = i
                test = True
                for j in range(1, split.shape[0]):
                    test = split[j - 1] <= sub_split[j - 1]
                    if test:
                        split[j] = sub_split[j - 1]
                    else:
                        break
                if test:
                    splits.append(split)
        return splits

def getAllMoves(split_moves : list):
    if len(split_moves) == 1:
        return split_moves[0]
    else:
        group_moves_init = split_moves.pop()
        all_moves_rest = getAllMoves(split_moves)
        all_moves= []
        for moveList_rest in all_moves_rest:
            for moveList in group_moves_init:
                all_moves.append(moveList_rest+moveList)
        return all_moves
