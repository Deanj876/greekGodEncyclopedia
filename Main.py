# from functions import clear_screen, greet, create_connection, get_or_create_parent, get_or_create_level, menu
# from functions import add_god, search_god, search_god_by_letter, delete_god, display_gods, edit_god, flag_god, unflag_god
from UI import main

# Main program

# clear_screen()
# greet("John Doe")
# conn, cursor = create_connection()
# while True:
#     choice = menu()
#     if choice == "1":
#         add_god(cursor, conn)
#     elif choice == "2":
#         search_god(cursor)
#     elif choice == "3":
#         search_god_by_letter(cursor)
#     elif choice == "4":
#         delete_god(cursor, conn)
#     elif choice == "5":
#         display_gods(cursor)
#     elif choice == "6":
#         edit_god(cursor, conn)
#     elif choice == "7":
#         flag_god(cursor, conn)
#     elif choice == "8":
#         unflag_god(cursor, conn)  # Add this line
#     elif choice == "9":
#         break
#     else:
#         print("Invalid choice! Please try again.")
#     input("Press enter to continue...")
#     clear_screen()
# clear_screen()
# conn.close()


if __name__ == "__main__":
    main()