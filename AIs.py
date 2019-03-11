from map import Tray
import numpy as np

class Node():
    def __init__(self, tray):
        self.tray = tray
        self.children = []
        self.edges = []

    def expand(self, maxSplit):
        if self.children == []:
            self.edges = self.tray.GetChildren(maxSplit)[1:]
            for edge in self.edges:
                upd = []
                for e in edge:
                    upd += [e['UPD'][0], e['UPD'][1]]
                newTray = Tray(self.tray.N, self.tray.M, [], Type = 5 - self.tray.Type)
                newTray.MAP = np.copy(self.tray.MAP)
                newTray.updateLists()
                newTray.UpdateTray(upd)
                self.children.append(Node(newTray))


def AlphaBeta(node : Node, d : int, maxSplit : int):
    if node.tray.IsTerminal() or d == 0:
        return heuristic(node.tray, 1) 

    node.expand(maxSplit)
    moves : list
    maxv = -float('inf')
    res : Node
    for k, child in enumerate(node.children):
        v = MinValue(child, -float('inf'), float('inf'), d - 1, maxSplit)
        if v >= maxv:
            maxv = v
            moves = [e['MOV'] for e in node.edges[k]]
            res = child
    return res, ["MOV", len(moves), [m for move in moves for m in move]]


def MaxValue(node : Node, alpha : float, beta : float, d : int, maxSplit : int):
    if node.tray.IsTerminal() or d == 0:
        return heuristic(node.tray, 1) 
    v = -float('inf')
    #node.expand(maxSplit)
    node.children = [Node(node.tray)]
    for k, child in enumerate(node.children):
        v = max(v, MinValue(child, alpha, beta, d - 1, maxSplit))
        if v >= beta:
            node.children = node.children[:k+1]
            return v
        alpha = max(alpha, v)
    return v

def MinValue(node : Node, alpha : float, beta : float, d : int, maxSplit : int):
    if node.tray.IsTerminal() or d == 0:
        return heuristic(node.tray, -1)
    v = float('inf')
    node.expand(maxSplit)
    for k, child in enumerate(node.children):
        v = min(v, MaxValue(child, alpha, beta, d - 1, maxSplit))
        if v <= alpha:
            node.children = node.children[:k+1]
            return v
        beta = min(beta, v)
    return v

def heuristic(tray : Tray, nodeType : int):
    if tray.Type == 2:
        return nodeType*(tray.N_vampires-tray.N_werewolves)
    else:
        return nodeType*(tray.N_werewolves-tray.N_vampires)