import socket
import json
import logging
import tkinter
from tkinter import *

logging.basicConfig(
    filename='client_log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PORT = 5050
SERVER = '127.0.0.1'
ADDRESS = (SERVER, PORT)

def send_request(request_data):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info("Client started up.")
        client.connect(ADDRESS)
        logging.info(f"Connected to server at {ADDRESS}.")
        client.send(json.dumps(request_data).encode())
        response = client.recv(2048).decode()
        client.close()
        return json.loads(response)
    except Exception as e:
        logging.error(f"Error sending request: {e}")
        return {'status': 'error', 'message': str(e)}
        
# operation1 = {
#     'operation':'get_movies',
# }

# operation2 = {
#         'operation':'add_movie',
#     'title':'Test',    
#     'cinema_room':'7',
#     'release_date':'20-05-2025',
#     'end_date':'02-06-2025',
#     'tickets_available':'69',
#     'ticket_price':'420.0',
# }

# operation3 = {
#     'operation':'update_movie_details',
#     'id':'8',
#     'title':'Lilo & Stitch',
#     'cinema_room':'7',
#     'release_date':'21-06-2002',
#     'end_date':'02-06-2025',
#     'ticket_price':'50.0',
# }

# operation4 = {
#     'operation':'delete_movie',
#     'title':'Lilo & Stitch',
# }

# operation5 = {
#     'operation':'update_tickets_of_movie',
#     'title':'Lilo & Stitch',
#     'tickets_available':'125'
# }

# operation6 = {
#     'operation':'record_ticket_sale',
#     'title':'Avatar',
#     'customer_name':'Ruben Da Silva',
#     'number_of_tickets':'2',
#     'total':'300.0'
# }

# request = operation6

window = tkinter.Tk()
window.title("Cinema Sales System - BE.2022.V6T6C1")
window.geometry("400x250")
window.mainloop()