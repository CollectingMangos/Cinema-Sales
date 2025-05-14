import sqlite3

connection = sqlite3.connect('cinema.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        cinema_room INTEGER NOT NULL CHECK (cinema_room BETWEEN 1 AND 7),
        release_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        tickets_available INTEGER NOT NULL,
        ticket_price REAL NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER NOT NULL,
        customer_name TEXT NOT NULL,
        number_of_tickets INTEGER NOT NULL CHECK (number_of_tickets > 0),
        total REAL NOT NULL,        
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    )
''')

movies = [
    ('Grown Ups', 1, '25-06-2010', '06-07-2025', 200, 100.00),
    ('Avatar', 2, '18-12-2009', '12-06-2025', 150, 150.00),
    ('Treasure Planet', 3, '06-11-2002', '12-06-2025', 100, 50.00),
    ('Jurassic Park', 4, '11-06-1993', '12-06-2025', 100, 80.00),
    ('Star Wars: Episode III - Revenge of the Sith', 5, '19-05-2005', '12-06-2025', 50, 125.00),
    ('The Big Wedding', 6, '26-04-2013', '12-06-2025', 50, 75.00),
    ('Lilo & Stitch', 7, '21-06-2002', '12-06-2025', 50, 50.00),
]

cursor.executemany('''
    INSERT INTO movies (title, cinema_room, release_date, end_date, tickets_available, ticket_price)
    VALUES (?, ?, ?, ?, ?, ?)
''', movies)

connection.commit()
connection.close()