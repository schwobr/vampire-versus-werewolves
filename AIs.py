from map import Tray
import numpy as np



def MaxValue(tray : Tray, alpha, beta, d : int, max_d : int):
    if tray.IsTerminal() or d == max_d:
        return heuristic(tray) 
    v = -float('inf')
    children = tray.GetChildren(3)[1:]
    for child in children:
        newTray = Tray(tray.N, tray.M, [], Type = 5 - tray.Type)
        newTray.MAP = np.copy(tray.MAP)
        newTray.UpdateTray(child['UPD'])
        v = max(v, MinValue(newTray, alpha, beta, d + 1, max_d))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def MinValue(tray : Tray, alpha, beta, d, max_d):
    if tray.IsTerminal() or d == max_d:
        return heuristic(tray)
    v = float('inf')
    children = tray.GetChildren(3)[1:]    
    for child in children:
        newTray = Tray(tray.N, tray.M, [], Type = 5 - tray.Type)
        newTray.MAP = np.copy(tray.MAP)
        newTray.UpdateTray(child)
        v = min(v, MaxValue(newTray, alpha, beta, d + 1, max_d))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def heuristic(tray : Tray):
    return 0