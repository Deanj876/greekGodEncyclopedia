# functions.py

def clear_screen():
    print("\033[H\033[J", end="")

def greet(name):
    print(f"Hello, {name}!")

def create_connection():
    # Dummy implementation
    print("Creating a connection...")
    return None, None

def get_or_create_parent(cursor, name):
    # Dummy implementation
    print(f"Getting or creating parent with name: {name}")
    return None

def get_or_create_level(cursor, level):
    # Dummy implementation
    print(f"Getting or creating level: {level}")
    return None

def menu():
    print("1. Add a God / Deity / Titan")
    print("2. Search for a God / Deity / Titan's information")
    print("3. Search for a God / Deity / Titan by letter or key word")
    print("4. Delete a God / Deity / Titan")
    print("5. Display all Gods / Deities / Titans")
    print("6. Edit a God / Deity / Titan")
    print("7. Flag a God / Deity / Titan")
    print("8. Unflag a God / Deity / Titan")
    print("9. Exit")
    choice = input("Enter your choice: ")
    return choice