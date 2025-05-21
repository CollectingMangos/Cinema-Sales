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
        operation = request.get('operation')
        if operation == 'get_movies':
            return get_movies()
        elif operation == 'delete_movie':
            return delete_movie(request.get('title'))
        elif operation == 'add_movie':
            return add_movie(
                request.get('title'),
                int(request.get('cinema_room')),
                request.get('release_date'),
                request.get('end_date'),
                int(request.get('tickets_available')),
                float(request.get('ticket_price'))
                )
        elif operation == 'update_movie_details':
            return update_movie_details(
                request.get('title'),
                int(request.get('cinema_room')),
                request.get('release_date'),
                request.get('end_date'),
                float(request.get('ticket_price'))
                )
        elif operation == 'update_tickets_of_movie':
            return update_tickets_of_movie(request.get('title'),int(request.get('tickets_available')))
        elif operation == 'record_ticket_sale':
            return record_ticket_sale()
        else:
            return {'status': 'failed', 'message': 'Invalid request'}
    except json.JSONDecodeError:
        return {'status': 'failed', 'message': 'Invalid JSON format'}
    except Exception as e:
        return {'status': 'error', 'message': f'Unexpected server error: {e}'}

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

def add_movie(title, cinema_room, release_date, end_date, tickets_available, ticket_price):
    try:
        title = title.strip()
        connection = get_db_connection()
        cursor = connection.cursor()
        if not (1 <= cinema_room <= 7):
            return {'status': 'error', 'message': 'Cinema room must be between 1 and 7!'}
        if tickets_available < 0:
            return {'status': 'error', 'message': 'Tickets available must be greater than 0!'}
        if ticket_price < 0:
            return {'status': 'error', 'message': 'Ticket price must be greater than 0!'}
        cursor.execute('SELECT title FROM movies WHERE title = ?', (title,))
        if cursor.fetchone():
            return {'status': 'error', 'message': f'Movie: {title} already exists!'}
        cursor.execute('SELECT cinema_room FROM movies WHERE cinema_room = ?', (cinema_room,))
        if cursor.fetchone():
            return {'status': 'error', 'message': f'Cinema room {cinema_room} is already in use!'}
        cursor.execute('''
            INSERT INTO movies (title, cinema_room, release_date, end_date, tickets_available, ticket_price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, cinema_room, release_date, end_date, tickets_available, ticket_price))
        connection.commit()
        logging.debug(f'Movie added: {title}')
        return {'status': 'success', 'message': f'Movie: {title} has been added successfully'}
    except Exception as e:
        logging.error(f'Error adding the movie: {title}. {e}')
        return {'status': 'error', 'message': f'Failed to add the movie: {title}'}
    finally:
        connection.close()

def update_movie_details(title, cinema_room, release_date, end_date, ticket_price):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT title FROM movies WHERE title = ?', (title,))
        if not cursor.fetchone():
            logging.debug(f'Movie not found: {title}')
            return {'status': 'error', 'message': f'Movie: {title} not found!'}
        cursor.execute('''
            UPDATE movies
            SET cinema_room = ?, release_date = ?, end_date = ?, ticket_price = ?
            WHERE title = ?
        ''', (cinema_room, release_date, end_date, ticket_price, title))
        connection.commit()
        logging.debug(f'Movie details updated: {title}')
        return {'status': 'success', 'message': f'Movie: {title} has been updated successfully!'}
    except Exception as e:
        logging.error(f'Error updating movie details: {title}. {e}')
        return {'status': 'error', 'message': f'Failed to update movie: {title}'}
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

def update_tickets_of_movie(title, tickets_available):
    try:
        title = title.strip()
        tickets_available = int(tickets_available)
        logging.debug(f'Parsed tickets_available: {tickets_available}')
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT title FROM movies WHERE title = ?', (title,))
        if cursor.fetchone():
            cursor.execute(
                'UPDATE movies SET tickets_available = ? WHERE title = ?', 
                (tickets_available, title)
            )
            connection.commit()
            logging.debug(f'Tickets updated for movie: {title}')
            return {'status': 'success', 'message': f'Tickets updated for movie: {title}'}
        else:
            logging.debug(f'Movie not found: {title}')
            return {'status': 'error', 'message': f'Movie: {title} not found'}
    except Exception as e:
        logging.error(f'Error updating tickets for movie: {title}. {e}')
        return {'status': 'error', 'message': f'Failed to update tickets for movie: {title}'}
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
    request_data = client.recv(1024).decode()
    logging.debug(f'Received request from {address}: {request_data}')
    try:
        request = json.loads(request_data)
        response = handle_requests(request)
    except json.JSONDecodeError:
        response = {'status': 'failed', 'message': 'Invalid JSON format'}
    client.send(json.dumps(response).encode())
    logging.info(f'Sent response to {address}')
    client.close()
    logging.info(f'Connection closed to {address}')