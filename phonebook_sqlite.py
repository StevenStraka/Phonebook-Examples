import sqlite3
import tkinter as tk
from tkinter import ttk
from datetime import datetime

def init_db():
    conn = sqlite3.connect("phonebook.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS name (
            name_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            name TEXT NOT NULL,
            zip INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            contacts_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_id INTEGER NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            FOREIGN KEY (name_id) REFERENCES name(name_id) 
        )
    ''')
    conn.commit()

    # Add some test data but only when no data in table

     # Query the database
    cursor.execute("SELECT * FROM name")
    rows = cursor.fetchall()

    if not rows:
        # Insert a record
        id = cursor.execute("INSERT INTO name (date, name, zip) VALUES (?, ?, ?)", (datetime.now(), "Steve", 78610))
        cursor.execute("INSERT INTO contacts (name_id, phone, email) VALUES (?, ?, ?)", (id.lastrowid, '555.555.2903', 'Steve@yahoo.com'))
        id = cursor.execute("INSERT INTO name (date, name, zip) VALUES (?, ?, ?)", (datetime.now(), "April", 78620))
        cursor.execute("INSERT INTO contacts (name_id, phone, email) VALUES (?, ?, ?)", (id.lastrowid, '444.444.2904', 'April@gmail.com'))
        id = cursor.execute("INSERT INTO name (date, name, zip) VALUES (?, ?, ?)", (datetime.now(), "Chuck", 78630))
        cursor.execute("INSERT INTO contacts (name_id, phone, email) VALUES (?, ?, ?)", (id.lastrowid, '333.333.2905', 'Chuck@yahoo.com'))
        id = cursor.execute("INSERT INTO name (date, name, zip) VALUES (?, ?, ?)", (datetime.now(), "Anne", 78640))
        cursor.execute("INSERT INTO contacts (name_id, phone, email) VALUES (?, ?, ?)", (id.lastrowid, '222.222.2906', 'Anne@hotmail.com'))
        # Commit the transaction
        conn.commit()

        # Query the database
        cursor.execute("SELECT * FROM name")
        rows = cursor.fetchall()

        # Print query results
        for row in rows:
            print(row)

        # Query the database
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()

        # Print query results
        for row in rows:
            print(row)

        conn.close()


# Business logic (Controller)
def get_phone_number():
    name = entry.get()

    conn = sqlite3.connect("phonebook.db")
    cursor = conn.cursor()
    
    query = """SELECT c.phone FROM name AS n
        JOIN contacts AS c ON n.name_id = c.name_id
        WHERE n.name = ?"""
    params = (name,)
    cursor.execute(query, params)
    
    # Print query results
    rows = cursor.fetchone()
    if rows:
        num = rows[0]
    else:
        num = "not found."

    output_label.config(text=f"{name}'s number: {num}")

    conn.close()

# GUI (View)
def setup_ui():
    global entry, output_label
    # create root window
    window = tk.Tk()
    window.title("Phone Bokk")
    window.geometry("425x150")

    # Title label
    title_label = ttk.Label(master=window, text="Phone Book", font = ('Calibri', 24, 'bold'))
    title_label.pack()

    # # input field
    input_frame = ttk.Frame(master=window)
    name_label = button = ttk.Button(master=input_frame, text = 'Find phone number for? ')
    entry = ttk.Entry(master=input_frame)  # create entry field
    button = ttk.Button(master=input_frame, text = 'Find', command = get_phone_number)
    name_label.pack(side = 'left', padx = 2)  # place entry field on window
    entry.pack(side = 'left', padx = 2)  # place entry field on window
    button.pack(side = 'left')  # place button field on window
    input_frame.pack(pady = 10)

    # ouput
    output_label = ttk.Label(master=window, text = '      ', font = ('Calibri', 18))
    output_label.pack(pady = 5)

    #run  main window
    window.mainloop()

if __name__ == "__main__":
    init_db()
    setup_ui()