import socket
import json
import logging
import tkinter
from tkinter import ttk, messagebox

logging.basicConfig(
    filename='client_log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PORT = 5050
SERVER = '127.0.0.1'
ADDRESS = (SERVER, PORT)

def send_request(request):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info("Client started up.")
        client.connect(ADDRESS)
        logging.info(f"Connected to server at {ADDRESS}.")
        client.send(json.dumps(request).encode())
        response = client.recv(2048).decode()
        client.close()
        return json.loads(response)
    except Exception as e:
        logging.error(f"Error sending request: {e}")
        return {'status': 'error', 'message': str(e)}
        
# Example operations
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

def get_movies():
    result = send_request({'operation': 'get_movies'})
    if result['status'] == 'success':
        movies = result['movies']
        movie_dropdown['values'] = [movie[1] for movie in movies]
        return movies
    else:
        messagebox.showerror("Error", result['message'])
        return []

def calculate_total_and_display():
    try:
        selected_title = movie_variable.get()
        qty = int(ticket_entry.get())
        all_movies = get_movies()
        movie = next((m for m in all_movies if m[1] == selected_title), None)
        if not movie:
            raise Exception("Movie not found")
        price = movie[6]
        total = qty * price
        total_label.config(text=f"Total: R{total:.2f}")
        return total
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def purchase_tickets():
    selected_title = movie_variable.get()
    qty = ticket_entry.get()
    try:
        qty = int(qty)
        if qty <= 0:
            raise ValueError("Quantity must be greater than 0")
        all_movies = get_movies()
        movie = next((m for m in all_movies if m[1] == selected_title), None)
        if not movie:
            raise Exception("Movie not found")
        price = movie[6]
        total = qty * price
        sale_request = {
            'operation': 'record_ticket_sale',
            'title': selected_title,
            'customer_name': 'GUI User',
            'number_of_tickets': str(qty),
            'total': str(total)
        }
        result = send_request(sale_request)
        if result['status'] == 'success':
            messagebox.showinfo("Success", result['message'])
        else:
            messagebox.showerror("Failed", result['message'])
    except Exception as e:
        messagebox.showerror("Error", str(e))

def open_add_movie_window():
    add_window = tkinter.Toplevel(window)
    add_window.title("Add a New Movie")
    add_window.geometry("600x400")

    fields = {
        "Title": tkinter.Entry(add_window),
        "Cinema Room": tkinter.Entry(add_window),
        "Release Date (DD-MM-YYYY)": tkinter.Entry(add_window),
        "End Date (DD-MM-YYYY)": tkinter.Entry(add_window),
        "Tickets Available": tkinter.Entry(add_window),
        "Ticket Price": tkinter.Entry(add_window),
    }

    for idx, (label, entry) in enumerate(fields.items()):
        tkinter.Label(add_window, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        entry.grid(row=idx, column=1, padx=10, pady=5)

    def save_movie():
        request = {
            'operation': 'add_movie',
            'title': fields["Title"].get(),
            'cinema_room': fields["Cinema Room"].get(),
            'release_date': fields["Release Date (DD-MM-YYYY)"].get(),
            'end_date': fields["End Date (DD-MM-YYYY)"].get(),
            'tickets_available': fields["Tickets Available"].get(),
            'ticket_price': fields["Ticket Price"].get(),
        }
        response = send_request(request)
        messagebox.showinfo("Add Movie", response['message'])
        add_window.destroy()

    tkinter.Button(add_window, text="Save", command=save_movie).grid(row=len(fields), column=0, columnspan=2, pady=10)
    
def open_update_movie_window():
    update_window= tkinter.Toplevel(window)
    update_window.title("Update a Movie's Details")
    update_window.geometry("600x400")
    
    fields = {
        "Movie ID": tkinter.Entry(update_window),
        "Title": tkinter.Entry(update_window),
        "Cinema Room": tkinter.Entry(update_window),
        "Release Date (DD-MM-YYYY)": tkinter.Entry(update_window),
        "End Date (DD-MM-YYYY)": tkinter.Entry(update_window),
        "Ticket Price": tkinter.Entry(update_window),
    }
    for idx, (label, entry) in enumerate(fields.items()):
        tkinter.Label(update_window, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        entry.grid(row=idx, column=1, padx=10, pady=5)
        
        def update_movie():
            request = {
                'operation': 'update_movie_details',
                'id': fields["Movie ID"].get(),
                'title': fields["Title"].get(),
                'cinema_room': fields["Cinema Room"].get(),
                'release_date': fields["Release Date (DD-MM-YYYY)"].get(),
                'end_date': fields["End Date (DD-MM-YYYY)"].get(),
                'ticket_price': fields["Ticket Price"].get(),
            }
            response = send_request(request)
            messagebox.showinfo("Update Movie", response['message'])
            update_window.destroy()
    tkinter.Button(update_window, text="Update", command=update_movie).grid(row=len(fields), column=0, columnspan=2, pady=10)
    
def open_delete_movie_window():
    delete_window = tkinter.Toplevel(window)
    delete_window.title("Delete a Movie")
    delete_window.geometry("600x100")

    tkinter.Label(delete_window, text="Select Movie to Delete:").grid(row=0, column=0, padx=10, pady=10, sticky="e")

    movie_var = tkinter.StringVar()
    movie_dropdown = ttk.Combobox(delete_window, textvariable=movie_var, state="readonly", width=30)
    movie_dropdown.grid(row=0, column=1, padx=10, pady=10)

    response = send_request({'operation': 'get_movies'})
    if response['status'] == 'success':
        movie_titles = [movie[1] for movie in response['movies']]
        movie_dropdown['values'] = movie_titles
    else:
        messagebox.showerror("Error", response['message'])

    def delete_movie():
        title = movie_var.get()
        if not title:
            messagebox.showwarning("Missing Input", "Please select a movie.")
            return

        request = {
            'operation': 'delete_movie',
            'title': title,
        }
        response = send_request(request)
        messagebox.showinfo("Delete Movie", response['message'])
        delete_window.destroy()

    tkinter.Button(delete_window, text="Delete", command=delete_movie).grid(row=1, column=0, columnspan=2, pady=10)

window = tkinter.Tk()
window.title("Cinema Sales System - BE.2022.V6T6C1")
window.geometry("600x400")

main_frame = tkinter.Frame(window, padx=20, pady=20)
main_frame.grid(row=0, column=0, sticky="nsew")

tkinter.Label(main_frame, text="Select a Movie:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
movie_variable = tkinter.StringVar()
movie_dropdown = ttk.Combobox(main_frame, textvariable=movie_variable, state="readonly", width=30)
movie_dropdown.grid(row=0, column=1, sticky="w", padx=5, pady=5)
get_movies()

tkinter.Label(main_frame, text="Number of Tickets to Purchase:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
ticket_entry = tkinter.Entry(main_frame, width=10)
ticket_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

tkinter.Button(main_frame, text="Add to Cart", command=calculate_total_and_display).grid(row=2, column=0, columnspan=2, pady=5)

total_label = tkinter.Label(main_frame, text="Total: R0.00", font=('Arial', 10, 'bold'))
total_label.grid(row=3, column=0, columnspan=2, pady=5)

tkinter.Button(main_frame, text="Purchase Tickets", command=purchase_tickets).grid(row=4, column=0, columnspan=2, pady=10)
tkinter.Button(main_frame, text="Add Movie", command=lambda: open_add_movie_window()).grid(row=5, column=0, columnspan=2, pady=10)
tkinter.Button(main_frame, text="Update Movie", command=lambda: open_update_movie_window()).grid(row=6, column=0, columnspan=2, pady=10)
tkinter.Button(main_frame, text="Delete Movie", command=lambda: open_delete_movie_window()).grid(row=7, column=0, columnspan=2, pady=10)

window.mainloop()