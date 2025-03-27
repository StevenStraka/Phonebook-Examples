import mysql.connector
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Database utility functions
def open_mysql_db():
    """Returns the connection and cursor to interact with the database."""
    db_name = "test_db"
    conn = mysql.connector.connect(host="localhost", user="root", password="my-secret-pw")
    cursor = conn.cursor()
    return db_name, conn, cursor

def execute_query(cursor, query, params=None):
    """Executes a query with optional parameters."""
    cursor.execute(query, params) if params else cursor.execute(query)

def create_database(cursor, db_name):
    """Creates the database if it doesn't exist."""
    execute_query(cursor, f"CREATE DATABASE IF NOT EXISTS {db_name}")

def create_tables(cursor):
    """Creates the necessary tables for the app."""
    execute_query(cursor, """
        CREATE TABLE IF NOT EXISTS name (
            name_id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE NOT NULL,
            name VARCHAR(100) NOT NULL,
            zip INT NOT NULL
        )
    """)
    execute_query(cursor, """
        CREATE TABLE IF NOT EXISTS contacts (
            contacts_id INT AUTO_INCREMENT PRIMARY KEY,
            name_id INT NOT NULL,
            phone VARCHAR(20) NOT NULL,
            email VARCHAR(100),
            FOREIGN KEY (name_id) REFERENCES name(name_id)
        )
    """)

def add_test_data(cursor, conn):
    """Inserts test data if the 'name' table is empty."""
    execute_query(cursor, "SELECT * FROM name")
    if not cursor.fetchall():
        test_data = [
            ("Steve", 78610, '555.555.2903', 'Steve@yahoo.com'),
            ("April", 78620, '444.444.2904', 'April@gmail.com'),
            ("Chuck", 78630, '333.333.2905', 'Chuck@yahoo.com'),
            ("Anne", 78640, '222.222.2906', 'Anne@hotmail.com'),
        ]
        for name, zip, phone, email in test_data:
            execute_query(cursor, "INSERT INTO name (date, name, zip) VALUES (%s, %s, %s)", (datetime.now(), name, zip))
            id = cursor.lastrowid
            execute_query(cursor, "INSERT INTO contacts (name_id, phone, email) VALUES (%s, %s, %s)", (id, phone, email))
        conn.commit()

def seed_db():
    """Seeds the database with initial data."""
    db_name, conn, cursor = open_mysql_db()
    create_database(cursor, db_name)
    cursor.execute(f"USE {db_name}")
    create_tables(cursor)
    add_test_data(cursor, conn)
    cursor.close()
    conn.close()

# Business logic (Controller)
def get_phone_number_from_db(name):

    db_name, conn, cursor = open_mysql_db()
    cursor.execute(f"USE {db_name}")

    """Fetches the phone number for the given name."""
    query = """
        SELECT c.phone FROM name AS n
        JOIN contacts AS c ON n.name_id = c.name_id
        WHERE n.name = %s
    """
    execute_query(cursor, query, (name,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else None

def get_phone_number_for_name():
    """Handles the UI action of retrieving the phone number."""
    name = entry.get()
    
    phone_number = get_phone_number_from_db(name)
    if phone_number:
        output_label.config(text=f"{name}'s number: {phone_number}")
    else:
        output_label.config(text=f"Name '{name}' not found.")

# GUI (View)
def setup_ui():
    """Sets up the user interface for the phone book."""
    global entry, output_label
    window = tk.Tk()
    window.title("Phone Book")
    window.geometry("425x150")

    title_label = ttk.Label(master=window, text="Phone Book", font=('Calibri', 24, 'bold'))
    title_label.pack()

    input_frame = ttk.Frame(master=window)
    name_label = ttk.Label(master=input_frame, text='Find phone number for? ')
    entry = ttk.Entry(master=input_frame)
    button = ttk.Button(master=input_frame, text='Find', command=get_phone_number_for_name)
    name_label.pack(side='left', padx=2)
    entry.pack(side='left', padx=2)
    button.pack(side='left')
    input_frame.pack(pady=10)

    output_label = ttk.Label(master=window, text='      ', font=('Calibri', 18))
    output_label.pack(pady=5)

    window.mainloop()

def main():
    """Main function to run the application."""
    seed_db()
    setup_ui()

if __name__ == "__main__":
    main()
