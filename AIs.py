from map import Tray
import numpy as np

def AlphaBeta(tray : Tray, d : int, maxSplit : int):
    children = tray.GetChildren(maxSplit)[1:]
    moves : list
    maxv = -float('inf')
    for child in children:
        upd = []
        for c in child:            
            upd += [c['UPD'][0], c['UPD'][1]]
        newTray = Tray(tray.N, tray.M, [], Type = 5 - tray.Type)
        newTray.MAP = np.copy(tray.MAP)
        newTray.updateLists()
        newTray.UpdateTray(upd)
        v = MinValue(newTray, -float('inf'), float('inf'), d - 1, maxSplit)
        if v >= maxv:
            maxv = v
            moves = [c['MOV'] for c in child]
    return ["MOV", len(moves), [m for move in moves for m in move]]


def MaxValue(tray : Tray, alpha : float, beta : float, d : int, maxSplit : int):
    if tray.IsTerminal() or d == 0:
        return heuristic(tray, 1) 
    v = -float('inf')
    children = tray.GetChildren(maxSplit)[1:]
    for child in children:
        upd = []
        for c in child:            
            upd += [c['UPD'][0], c['UPD'][1]]
        #print(upd)
        newTray = Tray(tray.N, tray.M, [], Type = 5 - tray.Type)
        newTray.MAP = np.copy(tray.MAP)
        newTray.updateLists()
        newTray.UpdateTray(upd)
        v = max(v, MinValue(newTray, alpha, beta, d - 1, maxSplit))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def MinValue(tray : Tray, alpha : float, beta : float, d : int, maxSplit : int):
    if tray.IsTerminal() or d == 0:
        return heuristic(tray, -1)
    v = float('inf')
    children = tray.GetChildren(maxSplit) 
    for child in children:
        upd = []
        for c in child:            
            upd += [c['UPD'][0], c['UPD'][1]]
        newTray = Tray(tray.N, tray.M, [], Type = 5 - tray.Type)
        newTray.MAP = np.copy(tray.MAP)
        newTray.updateLists()
        newTray.UpdateTray(upd)
        v = min(v, MaxValue(newTray, alpha, beta, d - 1, maxSplit))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def heuristic(tray : Tray, nodeType : int):
    if tray.Type == 2:
        return nodeType*(tray.N_vampires-tray.N_werewolves)
    else:
        return nodeType*(tray.N_werewolves-tray.N_vampires)