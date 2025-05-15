import socket

PORT = 5050
SERVER = '127.0.0.1'
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

client.send('Hello from client'.encode())
print(client.recv(1024).decode())