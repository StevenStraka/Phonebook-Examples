import mysql.connector
import tkinter as tk
from tkinter import ttk
from datetime import datetime

def open_mysql_db():
    db_name = "elite102"
    conn = mysql.connector.connect(host="localhost", user="root", password="my-secret-pw")
    cursor = conn.cursor()
    return db_name,conn,cursor

def seed_db():
    db_name, conn, cursor = open_mysql_db()
    
    create_database(cursor, db_name)
    cursor.execute(f"USE {db_name}")
    create_tables(cursor)
    add_test_data(cursor, conn)

    cursor.close()
    conn.close()

def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS name (
            name_id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE NOT NULL,
            name VARCHAR(100) NOT NULL,
            zip INT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            contacts_id INT AUTO_INCREMENT PRIMARY KEY,
            name_id INT NOT NULL,
            phone VARCHAR(20) NOT NULL,
            email VARCHAR(100),
            FOREIGN KEY (name_id) REFERENCES name(name_id) 
        )
    """)

# Add some test data
def add_test_data(cursor, conn):

     # Query the database
    cursor.execute("SELECT * FROM name")
    rows = cursor.fetchall()

    if not rows:
        #Insert records
        cursor.execute("INSERT INTO name (date, name, zip) VALUES (%s, %s, %s)", (datetime.now(), "Steve", 78610))
        id = cursor.lastrowid
        cursor.execute("INSERT INTO contacts (name_id, phone, email) VALUES (%s, %s, %s)", (id, '555.555.2903', 'Steve@yahoo.com'))
        cursor.execute("INSERT INTO name (date, name, zip) VALUES (%s, %s, %s)", (datetime.now(), "April", 78620))
        id = cursor.lastrowid
        cursor.execute("INSERT INTO contacts (name_id, phone, email) VALUES (%s, %s, %s)", (id, '444.444.2904', 'April@gmail.com'))
        cursor.execute("INSERT INTO name (date, name, zip) VALUES (%s, %s, %s)", (datetime.now(), "Chuck", 78630))
        id = cursor.lastrowid
        cursor.execute("INSERT INTO contacts (name_id, phone, email) VALUES (%s, %s, %s)", (id, '333.333.2905', 'Chuck@yahoo.com'))
        cursor.execute("INSERT INTO name (date, name, zip) VALUES (%s, %s, %s)", (datetime.now(), "Anne", 78640))
        id = cursor.lastrowid
        cursor.execute("INSERT INTO contacts (name_id, phone, email) VALUES (%s, %s, %s)", (id, '222.222.2906', 'Anne@hotmail.com'))

        # Commit the transaction
        conn.commit()

        # Query the name table
        cursor.execute("SELECT * FROM name")
        rows = cursor.fetchall()

        # Print query results
        for row in rows:
            print(row)

        # Query the contacts table
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()

        # Print query results
        for row in rows:
            print(row)

        cursor.close()
        conn.close()

# Business logic (Controller)
def get_phone_number():
    name = entry.get()

    #connect to DB
    db_name, conn, cursor = open_mysql_db()
    cursor.execute(f"USE {db_name}")
    
    # Query the database
    query = """SELECT c.phone FROM name AS n
        JOIN contacts AS c ON n.name_id = c.name_id
        WHERE n.name = %s"""
    params = (name,)
    cursor.execute(query, params)
    
    # Print query results
    rows = cursor.fetchone()
    if rows:
        num = rows[0]
    else:
        num = "not found."

    output_label.config(text=f"{name}'s number: {num}")

    cursor.close()
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

def main():
    seed_db()
    setup_ui()

if __name__ == "__main__":
    main()