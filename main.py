import ServerConnection

TCP_IP = "127.0.0.1"
TCP_PORT = 5555

client = ServerConnection.ClientThread()
client.connect(TCP_IP,TCP_PORT)
