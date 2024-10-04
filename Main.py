import sqlite3
import os

# Function to greet a user
def greet(name):
    print(f"Hello, {name}!")

# Function to clear the terminal screen
def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')

# Function to create a database connection and table
def create_connection():
    conn = sqlite3.connect('gods.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gods (
            name TEXT PRIMARY KEY,
            title TEXT,
            god_of TEXT,
            symbol TEXT,
            greek_name TEXT,
            roman_name TEXT,
            description TEXT,
            child_of TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

# Function to add a new god to the database
def add_god(cursor, conn):
    clear_screen()
    name = input("Enter the name of the god: ")
    god_of = input("Enter the god of what: ")
    title = input("Enter the title of the god: ")
    symbol = input("Enter the symbol of the god: ")
    greek_name = input("Enter the Greek name of the god: ")
    roman_name = input("Enter the Roman name of the god: ")
    description = input("Enter the description of the god: ")
    child_of = input("Enter the god's parent: ")
    
    cursor.execute('''
        INSERT INTO gods (name, title, god_of, symbol, greek_name, roman_name, description, child_of)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, title, god_of, symbol, greek_name, roman_name, description, child_of))
    conn.commit()
    print("God added successfully!")
    input("Press enter to continue...")
    clear_screen()

# Function to search for a god in the database
def search_god(cursor):
    clear_screen()
    name = input("Enter the name of the god: ")
    cursor.execute('SELECT * FROM gods WHERE name = ?', (name,))
    god = cursor.fetchone()
    if god:
        clear_screen()
        print("#--------------------------------#")
        print(f"Title: {god[1]}")
        print(f"God of: {god[2]}")
        print(f"Symbol: {god[3]}")
        print(f"Greek Name: {god[4]}")
        print(f"Roman Name: {god[5]}")
        print(f"Description: {god[6]}")
        print(f"Child of: {god[7]}")
        print("#--------------------------------#")
        input("Press enter to continue...")
        clear_screen()
    else:
        print("God not found!")

# Function to search for a god in the database by letter or word
def search_god_by_letter(cursor):
    clear_screen()
    letter = input("Enter the letter or word to search for: ")
    found = False
    if letter.lower() == "olympians":
        print("#--------------------------------#")
        print("Zeus")
        print("Hera")
        print("Poseidon")
        print("Hades")
        print("Athena")
        print("Apollo")
        print("Artemis")
        print("Ares")
        print("Aphrodite")
        print("Hephaestus")
        print("Hermes")
        print("Hestia")
        print("#--------------------------------#")
        input("Press enter to continue...")
        clear_screen()
        return
    else: 
        print("#--------------------------------#")
        cursor.execute('SELECT name FROM gods WHERE name LIKE ?', ('%' + letter + '%',))
        gods = cursor.fetchall()
        for god in gods:
            print(god[0])
            found = True
        print("#--------------------------------#")
        input("Press enter to continue...")
        clear_screen()
        if not found:
            print("No gods found!")

# Function to delete a god from the database
def delete_god(cursor, conn):
    clear_screen()
    name = input("Enter the name of the god: ")
    cursor.execute('DELETE FROM gods WHERE name = ?', (name,))
    conn.commit()
    if cursor.rowcount > 0:
        print("God deleted successfully!")
    else:
        print("God not found!")
    input("Press enter to continue...")
    clear_screen()

# Function to display all the gods in the database
def display_gods(cursor):
    clear_screen()
    cursor.execute('SELECT name FROM gods ORDER BY name')
    gods = cursor.fetchall()
    if gods:
        print("#--------------------------------#")
        for god in gods:
            print(god[0])
        print("#--------------------------------#")
        print("\nTotal gods:", len(gods))
        print("#--------------------------------#")
        input("Press enter to continue...")
        clear_screen()
    else:
        print("No gods found!")

# Function to edit the information of a god in the database
def edit_god(cursor, conn):
    clear_screen()
    name = input("Enter the name of the god: ")
    cursor.execute('SELECT * FROM gods WHERE name = ?', (name,))
    god = cursor.fetchone()
    if god:
        print("Enter the information you want to edit: ")
        print("1. Title")
        print("2. God of")
        print("3. Symbol")
        print("4. Greek Name")
        print("5. Roman Name")
        print("6. Description")
        print("7. Child of")
        choice = input("Enter your choice: ")
        if choice == "1":
            new_value = input("Enter the new title: ")
            cursor.execute('UPDATE gods SET title = ? WHERE name = ?', (new_value, name))
        elif choice == "2":
            new_value = input("Enter the new god of: ")
            cursor.execute('UPDATE gods SET god_of = ? WHERE name = ?', (new_value, name))
        elif choice == "3":
            new_value = input("Enter the new symbol: ")
            cursor.execute('UPDATE gods SET symbol = ? WHERE name = ?', (new_value, name))
        elif choice == "4":
            new_value = input("Enter the new Greek name: ")
            cursor.execute('UPDATE gods SET greek_name = ? WHERE name = ?', (new_value, name))
        elif choice == "5":
            new_value = input("Enter the new Roman name: ")
            cursor.execute('UPDATE gods SET roman_name = ? WHERE name = ?', (new_value, name))
        elif choice == "6":
            new_value = input("Enter the new description: ")
            cursor.execute('UPDATE gods SET description = ? WHERE name = ?', (new_value, name))
        elif choice == "7":
            new_value = input("Enter the new child of: ")
            cursor.execute('UPDATE gods SET child_of = ? WHERE name = ?', (new_value, name))
        conn.commit()
        print("God information updated successfully!")
    else:
        print("God not found!")
    input("Press enter to continue...")
    clear_screen()

# Function to display the menu
def menu():
    print("1. Add a god")
    print("2. Search for a god's information")
    print("3. Search for a god by letter or key word")
    print("4. Delete a god")
    print("5. Display all gods")
    print("6. Edit a god")
    print("7. Exit")
    choice = input("Enter your choice: ")
    return choice

# Main program
clear_screen()
greet("John Doe")
conn, cursor = create_connection()
while True:
    choice = menu()
    if choice == "1":
        add_god(cursor, conn)
    elif choice == "2":
        search_god(cursor)
    elif choice == "3":
        search_god_by_letter(cursor)
    elif choice == "4":
        delete_god(cursor, conn)
    elif choice == "5":
        display_gods(cursor)
    elif choice == "6":
        edit_god(cursor, conn)
    elif choice == "7":
        break
    else:
        print("Invalid choice!")
        input("Press enter to continue...")
        clear_screen()
clear_screen()
conn.close()