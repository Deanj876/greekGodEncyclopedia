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
    create_parent_table(cursor)
<<<<<<< HEAD
    create_level_table(cursor)  # Create the levels table
=======
    create_levels_table(cursor)
>>>>>>> test-main
    create_gods_table(cursor)
    create_log_table(cursor)
    create_triggers(cursor)
    migrate_data(cursor)
    conn.commit()
    return conn, cursor

# Function to create the parent table
def create_parent_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

# Function to create the levels table
<<<<<<< HEAD
def create_level_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT UNIQUE NOT NULL
=======
def create_levels_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
>>>>>>> test-main
        )
    ''')

# Function to create the gods table
def create_gods_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gods_new (
            name TEXT PRIMARY KEY,
            title TEXT,
            god_of TEXT,
            symbol TEXT,
            greek_name TEXT,
            roman_name TEXT,
            description TEXT,
            father_id INTEGER,
            mother_id INTEGER,
            level_id INTEGER,
            FOREIGN KEY (father_id) REFERENCES parents(id),
            FOREIGN KEY (mother_id) REFERENCES parents(id),
            FOREIGN KEY (level_id) REFERENCES levels(id)
        )
    ''')

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

# Function to migrate existing data
def migrate_data(cursor):
    # Insert unique parents into the parents table
    cursor.execute('SELECT DISTINCT father FROM gods WHERE father IS NOT NULL')
    fathers = cursor.fetchall()
    for father in fathers:
        cursor.execute('INSERT OR IGNORE INTO parents (name) VALUES (?)', (father[0],))

    cursor.execute('SELECT DISTINCT mother FROM gods WHERE mother IS NOT NULL')
    mothers = cursor.fetchall()
    for mother in mothers:
        cursor.execute('INSERT OR IGNORE INTO parents (name) VALUES (?)', (mother[0],))

    # Insert unique levels into the levels table
<<<<<<< HEAD
    cursor.execute('SELECT DISTINCT level FROM gods WHERE level IS NOT NULL')
    levels = cursor.fetchall()
    for level in levels:
        cursor.execute('INSERT OR IGNORE INTO levels (level) VALUES (?)', (level[0],))
=======
    cursor.execute('SELECT DISTINCT level_of_god FROM gods WHERE level_of_god IS NOT NULL')
    levels = cursor.fetchall()
    for level in levels:
        cursor.execute('INSERT OR IGNORE INTO levels (name) VALUES (?)', (level[0],))
>>>>>>> test-main

    # Migrate gods data to the new gods table
    cursor.execute('SELECT * FROM gods')
    gods = cursor.fetchall()
    for god in gods:
<<<<<<< HEAD
        father_id = None
        if god[7]:
            cursor.execute('SELECT id FROM parents WHERE name = ?', (god[7],))
            father_record = cursor.fetchone()
            if father_record:
                father_id = father_record[0]

        mother_id = None
        if god[8]:
            cursor.execute('SELECT id FROM parents WHERE name = ?', (god[8],))
            mother_record = cursor.fetchone()
            if mother_record:
                mother_id = mother_record[0]

        level_id = None
        if god[9]:
            cursor.execute('SELECT id FROM levels WHERE level = ?', (god[9],))
            level_record = cursor.fetchone()
            if level_record:
                level_id = level_record[0]
=======
        cursor.execute('SELECT id FROM parents WHERE name = ?', (god[7],))
        father_id = cursor.fetchone()[0] if god[7] else None

        cursor.execute('SELECT id FROM parents WHERE name = ?', (god[8],))
        mother_id = cursor.fetchone()[0] if god[8] else None

        cursor.execute('SELECT id FROM levels WHERE name = ?', (god[9],))
        level_id = cursor.fetchone()[0] if god[9] else None
>>>>>>> test-main

        cursor.execute('''
            INSERT INTO gods_new (name, title, god_of, symbol, greek_name, roman_name, description, father_id, mother_id, level_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (god[0], god[1], god[2], god[3], god[4], god[5], god[6], father_id, mother_id, level_id))

    # Drop the old gods table and rename the new one
    cursor.execute('DROP TABLE gods')
    cursor.execute('ALTER TABLE gods_new RENAME TO gods')

# Function to get or create a parent
def get_or_create_parent(cursor, name):
    cursor.execute('SELECT id FROM parents WHERE name = ?', (name,))
    parent = cursor.fetchone()
    if parent:
        return parent[0]
    cursor.execute('INSERT INTO parents (name) VALUES (?)', (name,))
    return cursor.lastrowid

# Function to get or create a level
<<<<<<< HEAD
def get_or_create_level(cursor, level):
    cursor.execute('SELECT id FROM levels WHERE level = ?', (level,))
    level_record = cursor.fetchone()
    if level_record:
        return level_record[0]
    cursor.execute('INSERT INTO levels (level) VALUES (?)', (level,))
=======
def get_or_create_level(cursor, name):
    cursor.execute('SELECT id FROM levels WHERE name = ?', (name,))
    level = cursor.fetchone()
    if level:
        return level[0]
    cursor.execute('INSERT INTO levels (name) VALUES (?)', (name,))
>>>>>>> test-main
    return cursor.lastrowid

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
    father_name = input("Enter the God / Deity / Titan's father: ")
    mother_name = input("Enter the God / Deity / Titan's mother: ")
<<<<<<< HEAD
    level_of_god = input("Enter the level of the God / Deity / Titan (e.g., Major God / Olympian): ")

    father_id = get_or_create_parent(cursor, father_name)
    mother_id = get_or_create_parent(cursor, mother_name)
    level_id = get_or_create_level(cursor, level_of_god)
=======
    level_name = input("Enter the level of the God / Deity / Titan (e.g., Major God / Olympian): ")

    father_id = get_or_create_parent(cursor, father_name)
    mother_id = get_or_create_parent(cursor, mother_name)
    level_id = get_or_create_level(cursor, level_name)
>>>>>>> test-main
    
    cursor.execute('''
        INSERT INTO gods (name, title, god_of, symbol, greek_name, roman_name, description, father_id, mother_id, level_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, title, god_of, symbol, greek_name, roman_name, description, father_id, mother_id, level_id))
    conn.commit()
    print("God / Deity / Titan added successfully!")
    input("Press enter to continue...")
    clear_screen()

# Function to search for a God / Deity / Titan in the database
def search_god(cursor):
    clear_screen()
    name = input("Enter the name of the God / Deity / Titan: ").strip()
    name = textwrap.fill(name, width=70)  # Adjust width as needed
    cursor.execute('''
<<<<<<< HEAD
        SELECT gods.*, p1.name AS father_name, p2.name AS mother_name, l.level AS level_of_god
=======
        SELECT gods.*, p1.name AS father_name, p2.name AS mother_name, l.name AS level_name
>>>>>>> test-main
        FROM gods
        LEFT JOIN parents p1 ON gods.father_id = p1.id
        LEFT JOIN parents p2 ON gods.mother_id = p2.id
        LEFT JOIN levels l ON gods.level_id = l.id
        WHERE TRIM(gods.name) = ?
    ''', (name,))
    god = cursor.fetchone()
    if god:
        print(f"\033[1mName:\033[0m {god[0]}")
        print(f"\033[1mTitle:\033[0m {god[1]}")
        print(f"\033[1mGod of:\033[0m {god[2]}")
        print(f"\033[1mSymbol:\033[0m {god[3]}")
        print(f"\033[1mGreek Name:\033[0m {god[4]}")
        print(f"\033[1mRoman Name:\033[0m {god[5]}")
        print(f"\033[1mDescription:\033[0m {textwrap.fill(god[6], width=70)}")  # Adjust width as needed
        print(f"\033[1mFather:\033[0m {god[10]}")  # father_name
        print(f"\033[1mMother:\033[0m {god[11]}")  # mother_name
<<<<<<< HEAD
        print(f"\033[1mLevel of God:\033[0m {god[12]}")  # level_of_god
=======
        print(f"\033[1mLevel of God:\033[0m {god[12]}")  # level_name
>>>>>>> test-main
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
        cursor.execute('''
            SELECT gods.name
            FROM gods
            LEFT JOIN parents p1 ON gods.father_id = p1.id
            WHERE TRIM(p1.name) LIKE ?
        ''', ('%' + letter + '%',))
        field = "Father"
    elif choice == "3":
        cursor.execute('''
            SELECT gods.name
            FROM gods
            LEFT JOIN parents p2 ON gods.mother_id = p2.id
            WHERE TRIM(p2.name) LIKE ?
        ''', ('%' + letter + '%',))
        field = "Mother"
    elif choice == "4":
        cursor.execute('''
            SELECT gods.name
            FROM gods
            LEFT JOIN levels l ON gods.level_id = l.id
<<<<<<< HEAD
            WHERE TRIM(l.level) LIKE ?
=======
            WHERE TRIM(l.name) LIKE ?
>>>>>>> test-main
        ''', ('%' + letter + '%',))
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
        cursor.execute('''
<<<<<<< HEAD
            SELECT gods.*, p1.name AS father_name, p2.name AS mother_name, l.level AS level_of_god
=======
            SELECT gods.*, p1.name AS father_name, p2.name AS mother_name, l.name AS level_name
>>>>>>> test-main
            FROM gods
            LEFT JOIN parents p1 ON gods.father_id = p1.id
            LEFT JOIN parents p2 ON gods.mother_id = p2.id
            LEFT JOIN levels l ON gods.level_id = l.id
            WHERE TRIM(gods.name) = ?
        ''', (selected_god,))
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
            print(f"\033[1mFather:\033[0m {god[10]}")  # father_name
            print(f"\033[1mMother:\033[0m {god[11]}")  # mother_name
<<<<<<< HEAD
            print(f"\033[1mLevel of God:\033[0m {god[12]}")  # level_of_god
=======
            print(f"\033[1mLevel of God:\033[0m {god[12]}")  # level_name
>>>>>>> test-main
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
            father_id = get_or_create_parent(cursor, new_value)
            cursor.execute('UPDATE gods SET father_id = ? WHERE name = ?', (father_id, name))
        elif choice == "8":
            new_value = input("Enter the new mother: ")
            mother_id = get_or_create_parent(cursor, new_value)
            cursor.execute('UPDATE gods SET mother_id = ? WHERE name = ?', (mother_id, name))
        elif choice == "9":
            new_value = input("Enter the new level of God / Deity / Titan: ")
            level_id = get_or_create_level(cursor, new_value)
            cursor.execute('UPDATE gods SET level_id = ? WHERE name = ?', (level_id, name))
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