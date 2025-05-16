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

def handle_requests(request):
    pass

def get_movies():
    try:
        connection = sqlite3.connect('cinema.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM movies')
        movies = cursor.fetchall()
        return {'status':'success', 'movies': movies}
    except:
        return {'status':'error', 'message': 'Failed to fetch movies'}
    finally:
        connection.close()

def add_movie():
    try:
        connection = sqlite3.connect('cinema.db')
        cursor = connection.cursor()
    except:
        pass
    finally:
        connection.close()

def update_movie():
    try:
        connection = sqlite3.connect('cinema.db')
        cursor = connection.cursor()
    except:
        pass
    finally:
        connection.close()

def delete_movie():
    try:
        connection = sqlite3.connect('cinema.db')
        cursor = connection.cursor()
    except:
        pass
    finally:
        connection.close()

def update_tickets_of_movie():
    try:
        connection = sqlite3.connect('cinema.db')
        cursor = connection.cursor()
    except:
        pass
    finally:
        connection.close()

def record_ticket_sale():
    try:
        connection = sqlite3.connect('cinema.db')
        cursor = connection.cursor()
    except:
        pass
    finally:
        connection.close()

while True:
    client, address = server.accept()
    print(f'New connection from address: {address}')
    logging.info(f'New connection from {address}')

    request = client.recv(1024).decode()
    print(f'[RECEIVED] {request}')
    logging.debug(f'Received request from {address}:{request}')
    
    client.send('[SENT] Helllo from server!'.encode())
    logging.info(f'Sent response to {address}')

    client.close()
    logging.info(f'Connection closed to {address}')