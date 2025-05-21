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

operation1 = {
    'operation':'get_movies',
}

operation2 = {
        'operation':'add_movie',
    'title':'Test',    
    'cinema_room':'1',
    'release_date':'20-05-2025',
    'end_date':'02-06-2025',
    'tickets_available':'100',
    'ticket_price':'420.0',
}

operation3 = {
    'operation':'update_movie_details',
    'title':'Grown Ups',
    'cinema_room':'1',
    'release_date':'20-05-2025',
    'end_date':'02-06-2025',
    'ticket_price':'420.0',
}

operation4 = {
    'operation':'delete_movie',
    'title':'Test',
}

operation5 = {
    'operation':'update_tickets_of_movie',
    'title':'Grown Ups',
    'tickets_available':'100'
}

operation6 = {
    'operation':'record_ticket_sale',
    'title':'Test',
    'customer_name':'Ruben Da Silva',
    'number_of_tickets':'2',
    'total':'840.0'
}

request = operation1

client.send(json.dumps(request).encode())
logging.info(f'Sent request: {request}')

response = client.recv(1024).decode()
reponse_data = json.loads(response)
print(reponse_data)
logging.info(f'Received response: {reponse_data}')

client.close()
logging.info('Client is shutting down')