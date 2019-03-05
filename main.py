import ServerConnection
import map
import time
from AIs import AlphaBeta, Node

TCP_IP = "127.0.0.1"
TCP_PORT = 5555

client = ServerConnection.ClientThread()
res = client.connect(TCP_IP,TCP_PORT)
n,m=res[0]
n_houses=res[1]
hum=res[2:2+n_houses]
x,y=res[2+n_houses]
Map=res[3+n_houses:]
tray = map.Tray(n, m, Map, x = x, y = y)
upd=client.receive("UPD")
tray.UpdateTray(upd)
node = Node(tray)

while True:    
    #print(tray.MAP)
    #print(tray.vampires)
    node, moves = AlphaBeta(node, 2, 2)
    print(moves)
    upd = client.send(moves)
    print(upd)
    tray.UpdateTray(upd)
    test = False
    for child in node.children:
        if tray == child.tray:
            test = True
            node = child
    if not(test):
        node = Node(tray)
