import socket
import sqlite3
import logging
import os
import json

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
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDRESS)

server.listen()
print(f'[STARTING] Listening on server: {SERVER} & port: {PORT}')
logging.info(f'Server is now listening on {SERVER}:{PORT}')

def get_db_connection():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cinema.db'))
    logging.debug(f'Database path: {db_path}')
    return sqlite3.connect(db_path)

def handle_requests(request):
    try:
        request = json.loads(request)
        operation = request.get('operation')
        if operation == 'get_movies':
            return get_movies()
        elif operation == 'delete_movie':
            return delete_movie(request.get('title'))
        elif operation == 'add_movie':
            return add_movie()
        elif operation == 'update_movie':
            return update_movie()
        elif operation == 'update_tickets_of_movie':
            return update_tickets_of_movie()
        elif operation == 'record_ticket_sale':
            return record_ticket_sale()
        else:
            return {'status': 'failed', 'message': 'Invalid request'}
    except json.JSONDecodeError:
        return {'status': 'failed', 'message': 'Invalid JSON format'}

def get_movies():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM movies')
        movies = cursor.fetchall()
        return {'status':'success', 'movies': movies}
    except:
        return {'status':'error', 'message': 'Failed to get all movies'}
    finally:
        connection.close()

def add_movie():
    try:
        connection = get_db_connection()        
        cursor = connection.cursor()
    except:
        pass
    finally:
        connection.close()

def update_movie():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
    except:
        pass
    finally:
        connection.close()

def delete_movie(title):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT title FROM movies WHERE title = ?', (title,))
        if cursor.fetchone():
            cursor.execute('DELETE FROM movies WHERE title = ?', (title,))
            connection.commit()
            logging.debug(f'Movie deleted: {title}')
            return {'status': 'success', 'message': f'Movie: {title} has been deleted successfully'}
        else:
            logging.debug(f'Movie not found: {title}')
            return {'status': 'error', 'message': f'Movie: {title} not found'}
    except:
        logging.error(f'Error deleting movie: {title}.')
        return {'status': 'error', 'message': f'Failed to delete movie: {title}'}
    finally:
        connection.close()

def update_tickets_of_movie():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
    except:
        pass
    finally:
        connection.close()

def record_ticket_sale():
    try:
        connection = get_db_connection()
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
    
    response = handle_requests(request)
    
    client.send(json.dumps(response).encode())
    logging.info(f'Sent response to {address}')

    client.close()
    logging.info(f'Connection closed to {address}')