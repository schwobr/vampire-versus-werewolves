import ServerConnection
from Tray import Tray
import time
from AIs import AlphaBeta, Node
import sys

if __name__=='__main__':
    try:
        TCP_IP = sys.argv[1]
        TCP_PORT = int(sys.argv[2])
    except:
        TCP_IP="127.0.0.1"
        TCP_PORT = 5555

    client = ServerConnection.ClientThread()
    res = client.connect(TCP_IP,TCP_PORT, "StupidAI2")
    n, m = res[0]
    n_houses = res[1]
    hum = res[2:2+n_houses]
    x, y = res[2+n_houses]
    upd = res[3+n_houses:]
    tray = Tray(n, m, upd, x = x, y = y)
    upd=client.receive("UPD")
    tray.UpdateTray(upd)
    node = Node(tray)
    playNext = True

    while True:           
        if playNext:
            t1 = time.time()
            moves = tray.StupidAI()
            t2 = time.time()
            print(t2-t1)
            print(moves)
            upd = client.send(moves)            
        else:
            upd = client.receive('UPD')
            t2 = t1
        print(upd)
        if t2-t1 <= 10:
            playNext = True
            try:
                tray.UpdateTray(upd)
            except:
                break
            test = False
            """
            print(node.GetDepth())
            for child in node.children:
                if tray == child.tray:
                    test = True
                    node = child
                    break
            if not(test):
                print('not ok')
                node = Node(tray)
            """
        else:
            playNext = False

