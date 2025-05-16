import socket
import json
import logging

logging.basicConfig(
    filename='client_log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PORT = 5050
SERVER = '127.0.0.1'
ADDRESS = (SERVER, PORT)

logging.info('Client is starting up')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

request = {
    'operation': 'get_movies'
}
client.send(json.dumps(request).encode())
logging.info(f'Sent request: {request}')

response = client.recv(1024).decode()
reponse_data = json.loads(response)
print(reponse_data)
logging.info(f'Received response: {reponse_data}')

client.close()
logging.info('Client is shutting down')