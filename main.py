import ServerConnection
import map

TCP_IP = "127.0.0.1"
TCP_PORT = 5555

client = ServerConnection.ClientThread()
res = client.connect(TCP_IP,TCP_PORT)
n,m=res[0]
n_houses=res[1]
hum=res[2:2+n_houses]
x,y=res[2+n_houses]
Map=res[3+n_houses:]
print(Map)
tray = map.Tray(n,m,x,y,Map)
print(tray.humans)
print(tray.vampires)
print(tray.werewolves)

