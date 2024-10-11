import sqlite3
import textwrap
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
            father TEXT,
            mother TEXT,
            level_of_god TEXT
        )
    ''')
    create_log_table(cursor)
    create_triggers(cursor)
    conn.commit()
    return conn, cursor

# Function to create the log table
def create_log_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS god_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            god_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

# Function to create triggers
def create_triggers(cursor):
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS after_god_insert
        AFTER INSERT ON gods
        BEGIN
            INSERT INTO god_logs (action, god_name) VALUES ('INSERT', NEW.name);
        END;
    ''')

    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS after_god_delete
        AFTER DELETE ON gods
        BEGIN
            INSERT INTO god_logs (action, god_name) VALUES ('DELETE', OLD.name);
        END;
    ''')

# Function to add a new God / Deity / Titan to the database
def add_god(cursor, conn):
    clear_screen()
    name = input("Enter the name of the God / Deity / Titan: ")
    god_of = input("Enter the God / Deity / Titan of what: ")
    title = input("Enter the title of the God / Deity / Titan: ")
    symbol = input("Enter the symbol of the God / Deity / Titan: ")
    greek_name = input("Enter the Greek name of the God / Deity / Titan: ")
    roman_name = input("Enter the Roman name of the God / Deity / Titan: ")
    description = input("Enter the description of the God / Deity / Titan: ")
    father = input("Enter the God / Deity / Titan's father: ")
    mother = input("Enter the God / Deity / Titan's mother: ")
    level_of_god = input("Enter the level of the God / Deity / Titan (e.g., Major God / Olympian): ")
    
    cursor.execute('''
        INSERT INTO gods (name, title, god_of, symbol, greek_name, roman_name, description, father, mother, level_of_god)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, title, god_of, symbol, greek_name, roman_name, description, father, mother, level_of_god))
    conn.commit()
    print("God / Deity / Titan added successfully!")
    input("Press enter to continue...")
    clear_screen()

# Function to search for a God / Deity / Titan in the database
def search_god(cursor):
    clear_screen()
    name = input("Enter the name of the God / Deity / Titan: ").strip()
    name = textwrap.fill(name, width=70)  # Adjust width as needed
    cursor.execute('SELECT * FROM gods WHERE TRIM(name) = ?', (name,))
    god = cursor.fetchone()
    if god:
        print(f"\033[1mName:\033[0m {god[0]}")
        print(f"\033[1mTitle:\033[0m {god[1]}")
        print(f"\033[1mGod of:\033[0m {god[2]}")
        print(f"\033[1mSymbol:\033[0m {god[3]}")
        print(f"\033[1mGreek Name:\033[0m {god[4]}")
        print(f"\033[1mRoman Name:\033[0m {god[5]}")
        print(f"\033[1mDescription:\033[0m {textwrap.fill(god[6], width=70)}")  # Adjust width as needed
        print(f"\033[1mFather:\033[0m {god[7]}")
        print(f"\033[1mMother:\033[0m {god[8]}")
        print(f"\033[1mLevel of God:\033[0m {god[9]}")
    else:
        print("God / Deity / Titan not found.")
    input("Press enter to continue...")
    clear_screen()

# Function to search for a God / Deity / Titan in the database by letter or word
def search_god_by_letter(cursor):
    clear_screen()
    letter = input("Enter the letter or word to search for: ").strip()
    print("Search by:")
    print("1. Name")
    print("2. Father")
    print("3. Mother")
    print("4. Level of God")
    choice = input("Enter your choice: ").strip()
    print("#--------------------------------#")
    
    if choice == "1":
        cursor.execute('SELECT name FROM gods WHERE TRIM(name) LIKE ?', ('%' + letter + '%',))
        field = "Name"
    elif choice == "2":
        cursor.execute('SELECT name FROM gods WHERE TRIM(father) LIKE ?', ('%' + letter + '%',))
        field = "Father"
    elif choice == "3":
        cursor.execute('SELECT name FROM gods WHERE TRIM(mother) LIKE ?', ('%' + letter + '%',))
        field = "Mother"
    elif choice == "4":
        cursor.execute('SELECT name FROM gods WHERE TRIM(level_of_god) LIKE ?', ('%' + letter + '%',))
        field = "Level of God"
    else:
        print("Invalid choice!")
        input("Press enter to continue...")
        clear_screen()
        return

    gods = cursor.fetchall()
    if gods:
        print(f"Gods / Deities / Titans found by {field}:")
        print("#--------------------------------#")
        for god in gods:
            print(god[0])
        print("#--------------------------------#")
        
        selected_god = input("Enter the name of the God / Deity / Titan you want to display: ").strip()
        cursor.execute('SELECT * FROM gods WHERE TRIM(name) = ?', (selected_god,))
        god = cursor.fetchone()
        if god:
            clear_screen()
            print(f"\033[1mName:\033[0m {god[0]}")
            print(f"\033[1mTitle:\033[0m {god[1]}")
            print(f"\033[1mGod of:\033[0m {god[2]}")
            print(f"\033[1mSymbol:\033[0m {god[3]}")
            print(f"\033[1mGreek Name:\033[0m {god[4]}")
            print(f"\033[1mRoman Name:\033[0m {god[5]}")
            print(f"\033[1mDescription:\033[0m {textwrap.fill(god[6], width=70)}")  # Adjust width as needed
            print(f"\033[1mFather:\033[0m {god[7]}")
            print(f"\033[1mMother:\033[0m {god[8]}")
            print(f"\033[1mLevel of God:\033[0m {god[9]}")
        else:
            print("God / Deity / Titan not found!")
    else:
        print("No Gods / Deities / Titans found!")
    
    input("Press enter to continue...")
    clear_screen()
# Function to delete a God / Deity / Titan from the database
def delete_god(cursor, conn):
    clear_screen()
    name = input("Enter the name of the God / Deity / Titan: ")
    cursor.execute('DELETE FROM gods WHERE name = ?', (name,))
    conn.commit()
    if cursor.rowcount > 0:
        print("God / Deity / Titan deleted successfully!")
    else:
        print("God / Deity / Titan not found!")
    input("Press enter to continue...")
    clear_screen()

# Function to display all the Gods / Deities / Titans in the database
def display_gods(cursor):
    clear_screen()
    cursor.execute('SELECT name FROM gods ORDER BY name')
    gods = cursor.fetchall()
    if gods:
        print("#--------------------------------#")
        for god in gods:
            print(god[0])
        print("#--------------------------------#")
        print("\nTotal Gods / Deities / Titans:", len(gods))
        print("#--------------------------------#")
        input("Press enter to continue...")
        clear_screen()
    else:
        print("No Gods / Deities / Titans found!")

# Function to edit the information of a God / Deity / Titan in the database
def edit_god(cursor, conn):
    clear_screen()
    name = input("Enter the name of the God / Deity / Titan: ")
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
        print("7. Father")
        print("8. Mother")
        print("9. Level of God")
        choice = input("Enter your choice: ")
        if choice == "1":
            new_value = input("Enter the new title: ")
            cursor.execute('UPDATE gods SET title = ? WHERE name = ?', (new_value, name))
        elif choice == "2":
            new_value = input("Enter the new God / Deity / Titan of: ")
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
            new_value = input("Enter the new father: ")
            cursor.execute('UPDATE gods SET father = ? WHERE name = ?', (new_value, name))
        elif choice == "8":
            new_value = input("Enter the new mother: ")
            cursor.execute('UPDATE gods SET mother = ? WHERE name = ?', (new_value, name))
        elif choice == "9":
            new_value = input("Enter the new level of God / Deity / Titan: ")
            cursor.execute('UPDATE gods SET level_of_god = ? WHERE name = ?', (new_value, name))
        conn.commit()
        print("God / Deity / Titan information updated successfully!")
    else:
        print("God / Deity / Titan not found!")
    input("Press enter to continue...")
    clear_screen()

# Function to display the menu
def menu():
    print("1. Add a God / Deity / Titan")
    print("2. Search for a God / Deity / Titan's information")
    print("3. Search for a God / Deity / Titan by letter or key word")
    print("4. Delete a God / Deity / Titan")
    print("5. Display all Gods / Deities / Titans")
    print("6. Edit a God / Deity / Titan")
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