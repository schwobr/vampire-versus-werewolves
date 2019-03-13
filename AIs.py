from Tray import Tray
import numpy as np

class Node():
    def __init__(self, tray):
        self.tray = tray
        self.children = []
        self.edges = []

    def Expand(self, maxSplit):
        if self.children == []:
            #self.edges = self.tray.GetChildren(maxSplit)[1:]
            self.edges = self.tray.GetEdges(maxSplit)[1:]
            for edge in self.edges:
                newTray = Tray(self.tray.N, self.tray.M, [], Type = self.tray.Type)
                newTray.Grid = np.copy(self.tray.Grid)
                newTray.UpdateLists()
                newTray.UpdateTray(edge, is_upd = False)
                newTray.Type = 5 - newTray.Type
                self.children.append(Node(newTray))

def AlphaBeta(node : Node, d : int, maxSplit : int, gamma = 0.8):
    node.Expand(maxSplit)
    moves : list
    maxv = -float('inf')
    res : Node
    for k, child in enumerate(node.children):
        v = MinValue(child, -float('inf'), float('inf'), d - 1, maxSplit, gamma)
        if v >= maxv:
            maxv = v
            moves = node.edges[k]
            res = child
    mov = []
    for move in moves:
        if not(move[0]==move[3] and move[1]==move[4]):
            mov += move
    return res, ["MOV", int(len(mov)/5), mov]


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
    node.Expand(maxSplit)
    node.children.append(Node(node.tray))
    for k, child in enumerate(node.children):
        v = gamma * min(v, MaxValue(child, alpha, beta, d - 1, maxSplit, gamma))
        if v <= alpha:
            node.children = node.children[:k+1]
            return v
        beta = min(beta, v)
    return v
