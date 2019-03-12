from Tray import Tray
import numpy as np

class Node():
    def __init__(self, tray):
        self.tray = tray
        self.children = []
        self.edges = []

    def Expand(self, maxSplit):
        if self.children == []:
            self.edges = self.tray.GetChildren(maxSplit)[1:]
            for edge in self.edges:
                upd = []
                for e in edge:
                    upd += [e['UPD'][0], e['UPD'][1]]
                newTray = Tray(self.tray.N, self.tray.M, [], Type = 5 - self.tray.Type)
                newTray.Grid = np.copy(self.tray.Grid)
                newTray.UpdateLists()
                newTray.UpdateTray(upd)
                self.children.append(Node(newTray))


def AlphaBeta(node : Node, d : int, maxSplit : int, gamma = 0.8):
    if node.tray.IsTerminal() or d == 0:
        return node.tray.Heuristic(1) 
    node.Expand(maxSplit)
    moves : list
    maxv = -float('inf')
    res : Node
    for k, child in enumerate(node.children):
        v = MinValue(child, -float('inf'), float('inf'), d - 1, maxSplit, gamma)
        if v >= maxv:
            maxv = v
            moves = [e['MOV'] for e in node.edges[k]]
            res = child
    return res, ["MOV", len(moves), [m for move in moves for m in move]]


def MaxValue(node : Node, alpha : float, beta : float, d : int, maxSplit : int, gamma = 0.8):
    if node.tray.IsTerminal():
        if node.tray.Win():
            return 10000
        else:
            return -10000
    elif d==0:
        return node.tray.Heuristic(1) 
    v = -float('inf')
    node.Expand(maxSplit)
    for k, child in enumerate(node.children):
        v = gamma*max(v, MinValue(child, alpha, beta, d - 1, maxSplit, gamma))
        if v >= beta:
            node.children = node.children[:k+1]
            return v
        alpha = max(alpha, v)
    return v

def MinValue(node : Node, alpha : float, beta : float, d : int, maxSplit : int, gamma = 0.8):
    if node.tray.IsTerminal():
        if node.tray.Win():
            return -10000
        else:
            return 10000
    elif d == 0:
        return node.tray.Heuristic(-1)
    v = float('inf')
    #node.children = [Node(node.tray)]
    node.Expand(maxSplit)
    for k, child in enumerate(node.children):
        v = gamma * min(v, MaxValue(child, alpha, beta, d - 1, maxSplit, gamma))
        if v <= alpha:
            node.children = node.children[:k+1]
            return v
        beta = min(beta, v)
    return v
