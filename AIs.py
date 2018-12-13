from map import Tray

def MaxValue(tray : Tray, alpha, beta):
    if tray.IsTerminal():
        return heuristic(tray)
    v = -float('inf')
    children = tray.GetChildren(3)[1:]
    for child_move in children_moves:
        child = Tray(tray.N, tray.M, [], Type = tray.Type)
        child.MAP = np.Copy(tray.MAP)
        child.updateTray(child_move)
        v = max(v, MinValue(child, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def MinValue(tray : Tray, alpha, beta):
    if tray.IsTerminal():
        return heuristic(tray)
    v = float('inf')
    children_moves = tray.GetChildren(3)[1:]    
    for child_move in children_moves:
        child = Tray(tray.N, tray.M, [], Type = tray.Type)
        child.MAP = np.Copy(tray.MAP)
        child.updateTray(child_move)
        v = min(v, MaxValue(child, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def heuristic(tray : Tray):
    return 0