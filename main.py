import ServerConnection
from Tray import Tray
import time
from AIs import AlphaBeta, Node
import sys

try:
    TCP_IP = sys.argv[1]
    TCP_PORT = int(sys.argv[2])
except:
    TCP_IP="127.0.0.1"
    TCP_PORT = 5555

client = ServerConnection.ClientThread()
res = client.connect(TCP_IP,TCP_PORT)
n, m = res[0]
n_houses = res[1]
hum = res[2:2+n_houses]
x, y = res[2+n_houses]
upd = res[3+n_houses:]
tray = Tray(n, m, upd, x = x, y = y)
upd=client.receive("UPD")
tray.UpdateTray(upd)
node = Node(tray)

while True:    
    node, moves = AlphaBeta(node, 5, 1)
    print(moves)
    upd = client.send(moves)
    print(upd)
    tray.UpdateTray(upd)
    test = False
    if tray != node.tray:
            test = True
            node = Node(tray)
    if not(test):
        node = Node(tray)
