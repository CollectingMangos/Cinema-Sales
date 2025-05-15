import socket
import sqlite3
import logging

logging.basicConfig(
    filename='server_log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PORT = 5050
SERVER = '127.0.0.1'
ADDRESS = (SERVER, PORT)

logging.info('Server is starting up')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

server.listen()
print(f'[STARTING] Listening on server: {SERVER} & port: {PORT}')
logging.info(f'Server is now listening on {SERVER}:{PORT}')

while True:
    client, address = server.accept()
    print(f'New connection from address: {address}')
    logging.info(f'New connection from {address}')

    request = client.recv(1024).decode()
    print(f'[RECEIVED] {request}')
    logging.debug(f'Received request from {address}:{request}')
    
    client.send('Message received.'.encode())
    logging.info(f'Sent response to {address}')

    client.close()
    logging.info(f'Connection closed to {address}')