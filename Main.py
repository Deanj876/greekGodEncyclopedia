# Greek God Encyclopedia / Dictionary
# This program allows the user to add, search, delete, and display the Greek gods and their information.

# Website of Information: 
# https://greekgodsandgoddesses.net/ 
# https://www.greekmythology.com/Olympians/olympians.html

# ---------------------------------------------- #
#          Notes on Program Functionality        #
# 1. Removed Consorts and Children from the dictionary due to how extensive the information is, 
#    Along with the fact that the information is not consistent across religions, translations, myths, and stories.
# ---------------------------------------------- #
# Importing the necessary libraries
import json
import os

# Function to clear the terminal screen
def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')
    
# Function to load the data from the json file
def load_data():
    if not os.path.exists("data.json"):
        with open("data.json", "w") as file:
            json.dump({}, file)  # Initialize with an empty dictionary
    with open("data.json") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}  # Initialize with an empty dictionary if JSON is invalid
    return data

# Function to add a new god to the dictionary
def add_god(data):
    clear_screen()
    name = input("Enter the name of the god: ")
    godOf = input("Enter the god of what: ")
    title = input("Enter the title of the god: ")
    symbol = input("Enter the symbol of the god: ")
    greek_name = input("Enter the Greek name of the god: ")
    roman_name = input("Enter the Roman name of the god: ")
    description = input("Enter the description of the god: ")
    childOf = input("Enter the god's parent: ")
    # consorts = input("Enter the god's consort(s): ")
    # children = input("Enter the god's child(ren): ")
    data[name] = {
        "title": title,
        "god of": godOf,
        "symbol": symbol,
        "greek_name": greek_name,
        "roman_name": roman_name,
        "description": description,
        "child of": childOf,
        # "consorts": consorts,
        # "children": children
    }
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)
    print("God added successfully!")
    exit = input("Press enter to continue...")
    clear_screen()

# Function to search for a god in the dictionary
def search_god(data):
    clear_screen()
    name = input("Enter the name of the god: ")
    if name in data:
        clear_screen()
        print("#--------------------------------#")
        print(f"Title: {data[name]['title']}")
        print(f"God of: {data[name]['god of']}")
        print(f"Symbol: {data[name]['symbol']}")
        print(f"Greek Name: {data[name]['greek_name']}")
        print(f"Roman Name: {data[name]['roman_name']}")
        print(f"Description: {data[name]['description']}")
        print(f"Child of: {data[name]['child of']}")
        # print(f"Consort(s): {data[name]['consorts']}")
        # print(f"Child(ren): {data[name]['children']}")
        print("#--------------------------------#")

        exit = input("Press enter to continue...")
        clear_screen()
    else:
        print("God not found!")

# Function to search for a god in the dictionary by letter or word
def search_god_by_letter(data):
    clear_screen()
    letter = input("Enter the letter or word to search for: ")
    found = False
    # isolate the 12 olympians from other gods when displaying
    # 12 Olympians: Zeus, Hera, Poseidon, Demeter, Athena, Apollo, Artemis, Ares, Aphrodite, Hephaestus, Hermes, Hestia
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
        exit = input("Press enter to continue...")
        clear_screen()
        return
    else: 
        print("#--------------------------------#")
        for god in data:
            if letter.lower() in god.lower():
                print(god)
                found = True
        print("#--------------------------------#")
        exit = input("Press enter to continue...")
        clear_screen()
        if not found:
            print("No gods found!")

# Function to delete a god from the dictionary
def delete_god(data):
    clear_screen()
    name = input("Enter the name of the god: ")
    if name in data:
        del data[name]
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
        print("God deleted successfully!")
    else:
        print("God not found!")

# Function to display all the gods in the dictionary
def display_gods(data):
    clear_screen()
    if data:
        print("#--------------------------------#")
        # Display all the gods in Alphabetical order
        for god in sorted(data):
            print(god)
        print("#--------------------------------#")
        print("\nTotal gods:", len(data))
        print("#--------------------------------#")
        exit = input("Press enter to continue...")
        clear_screen()
    else:
        print("No gods found!")

# Function to Edit the information of a god
def edit_god(data):
    clear_screen()
    name = input("Enter the name of the god: ")
    if name in data:
        print("Enter the information you want to edit: ")
        print("1. Title")
        print("2. God of")
        print("3. Symbol")
        print("4. Greek Name")
        print("5. Roman Name")
        print("6. Description")
        print("7. Child of")
        # print("8. Consort(s)")
        # print("9. Child(ren)")
        choice = input("Enter your choice: ")
        if choice == "1":
            # Display old Data
            print("Old Title: ", data[name]["title"])
            # Update Data
            data[name]["title"] = input("Enter the new title: ")
        elif choice == "2":
            # Display old Data
            print("Old \"god of\": ", data[name]["god of"])
            # Update Data
            data[name]["god of"] = input("Enter the new god of: ")
        elif choice == "3":
            # Display old Data
            print("Old symbol: ", data[name]["symbol"])
            # Update Data
            data[name]["symbol"] = input("Enter the new symbol: ")
        elif choice == "4":
            # Display old Data
            print("Old greek_name: ", data[name]["greek_name"])
            # Update Data
            data[name]["greek_name"] = input("Enter the new Greek name: ")
        elif choice == "5":
            # Display old Data
            print("Old roman_name: ", data[name]["roman_name"])
            # Update Data
            data[name]["roman_name"] = input("Enter the new Roman name: ")
        elif choice == "6":
            # Display old Data
            print("Old description: ", data[name]["description"])
            # Update Data
            data[name]["description"] = input("Enter the new description: ")
        elif choice == "7":
            # Display old Data
            print("Old \"child of\": ", data[name]["child of"])
            # Update Data
            data[name]["child of"] = input("Enter the new child of: ")
        # elif choice == "8":
        #     data[name]["consorts"] = input("Enter the new consort(s): ")
        # elif choice == "9":
        #     data[name]["children"] = input("Enter the new child(ren): ")
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
        print("God information updated successfully!")
    else:
        print("God not found!")

# Function to display the menu
def menu():
    print("1. Add a god")
    print("2. Search for a god's information")
    print("3. Search for a god by letter or  key word")
    print("4. Delete a god")
    print("5. Display all gods")
    print("6. Edit a god")
    print("7. Exit")
    choice = input("Enter your choice: ")
    return choice

# Main program
clear_screen()
data = load_data()
while True:
    choice = menu()
    if choice == "1":
        add_god(data)
    elif choice == "2":
        search_god(data)
    elif choice == "3":
        search_god_by_letter(data)
    elif choice == "4":
        delete_god(data)
    elif choice == "5":
        display_gods(data)
    elif choice == "6":
        edit_god(data)
    elif choice == "7":
        break
    else:
        print("Invalid choice!")
        exit = input("Press enter to continue...")
        clear_screen()
clear_screen()