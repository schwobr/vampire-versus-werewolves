from map import Tray

def MaxValue(tray : Tray, alpha, beta):
    if tray.IsTerminal():
        return heuristic(tray)
    v = -float('inf')
    children = tray.GetChildren()
    for child in children:
        v = max(v, MinValue(child, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def MinValue(tray : Tray, alpha, beta):
    if tray.IsTerminal():
        return heuristic(tray)
    v = float('inf')
    children = tray.GetChildren()
    for child in children:
        v = min(v, MaxValue(child, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v