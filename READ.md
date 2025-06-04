# Cinema Ticket Sales System by Ruben Da Silva, BE.2022.V6T6C1

This is a Python-based client-server application using **sockets**, **SQLite**, and a **Tkinter GUI** to manage movie listings and ticket sales for a cinema. It includes sales logging, receipt generation, and administrative functions for adding, updating, and deleting movies.

---

## 🔧 Features

- View all movies with available tickets.
- Purchase tickets through a GUI.
- Add, update, or delete movie listings.
- Log each sale to a database.
- Generate text file receipts for each ticket purchase.
- Validates input and handles errors gracefully.
- Persists data using `SQLite`.

---

## 📁 Project Structure

```
Cinema-Sales/
├── client/
│   ├── client.py            # Tkinter GUI Client
│   └── client_log.log       # Client-side logs
├── server/
│   ├── server.py            # Socket server logic
│   ├── cinema.db            # SQLite database
│   ├── database_config.py   # Optional database setup logic
│   ├── server_log.log       # Server-side logs
│   └── receipts/            # Automatically saved receipts
└── README.md
```

---

## ▶️ How to Run

### 1. Start the Server
Navigate to the `server` folder and run:

```bash
python server.py
```

The server will listen for connections on `127.0.0.1:5050`.

### 2. Run the Client
In a **separate terminal**, go to the `client` folder and run:

```bash
python client.py
```

This will launch the GUI interface.

---

## 🖥 GUI Functionality

- **Dropdown Menu**: Select from available movies (automatically fetched).
- **Entry Field**: Enter number of tickets to purchase.
- **Buttons**:
  - `Add to Cart`: Calculates and displays total price.
  - `Purchase Tickets`: Completes purchase, updates inventory, and saves receipt.
  - `Add Movie`: Opens a sub-window to enter full movie details.
  - `Update Movie`: Edit existing movie by ID.
  - `Delete Movie`: Remove a movie from the list.
- **Receipts**: Saved to `server/receipts/` with timestamped filenames.

---

## ⚙️ Requirements

- Python 3.8+
- No third-party libraries required (only `socket`, `sqlite3`, `tkinter`, `json`, `logging`, `os`)

---

## ❗ Notes

- The database must exist before starting the server (`cinema.db` is included).
- Receipts are saved as plain text files in the `receipts/` directory.
- Make sure the server is running **before** launching the client.
- Default connection is to `127.0.0.1:5050` — edit in `client.py` and `server.py` if needed.

---

## 📜 License

This project is intended for educational/demo use.