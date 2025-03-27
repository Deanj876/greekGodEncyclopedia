# ui.py
import sys
import sqlite3
import textwrap
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QTextEdit, QFormLayout, QMessageBox, QDialog, QScrollArea
from PyQt5.QtGui import QPixmap
import sys
# import openai

# class GodInfoScreen(QWidget):
#     def __init__(self, god_info):
#         super().__init__()
#         self.setWindowTitle("God Information")
#         # Set the background color to white
#         self.setStyleSheet("background-color: white;")
#         layout = QVBoxLayout()
#         for key, value in god_info.items():
#             layout.addWidget(QLabel(f"{key}: {value}"))
#         self.setLayout(layout)

class GodInfoScreen(QWidget):
    def __init__(self, god_info):
        super().__init__()
        self.setWindowTitle("God Information")
        
        layout = QVBoxLayout()
        for key, value in god_info.items():
            layout.addWidget(QLabel(f"{key}: {value}"))
        
        # Add the "Image" button
        image_button = QPushButton("Image")
        image_button.clicked.connect(lambda: self.open_image_screen(god_info.get("name", "")))
        layout.addWidget(image_button)
        
        self.setLayout(layout)

    def open_image_screen(self, god_name):
        # Open the image display screen
        self.image_screen = ImageDisplayScreen(god_name, self.cursor)
        self.image_screen.show()
class GodsListScreenDisplay(QWidget):
    def __init__(self):
        super().__init__()
        # Example button to open the image screen
        button = QPushButton("Show Zeus Image")
        button.clicked.connect(lambda: self.open_image_screen("Zeus"))
        layout = QVBoxLayout()
        layout.addWidget(button)
        self.setLayout(layout)

    def open_image_screen(self, god_name):
        self.image_screen = ImageDisplayScreen(god_name, self.cursor)
        self.image_screen.show()
# TEST___________________________________________________________
class ImageDisplayScreen(QWidget):
    def __init__(self, god_name, cursor):
        super().__init__()
        self.setWindowTitle(f"{god_name} Image")
        layout = QVBoxLayout()
        
        # Debug: Check the value of god_name
        print(f"God name received: {god_name}")
        
        # Handle empty or invalid god_name
        if not god_name:
            god_name = "Unknown"
            print("Warning: god_name is empty. Using default value.")
        
        # Specify the absolute folder path where images are stored
        image_folder = r"C:\Users\djohnson876\Documents\GitHub\pf24-greek-god-encyclopedia\images"
        image_path = os.path.join(image_folder, f"{god_name}.png")
        
        # Debug: Print the constructed path
        print(f"Looking for image at: {image_path}")
        
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            layout.addWidget(image_label)
        else:
            layout.addWidget(QLabel("Image not found."))
        
        self.setLayout(layout)


class GodsListScreen(QWidget):
    def __init__(self, gods, initial):
        super().__init__()
        self.setWindowTitle(f"Gods List - {initial}")
        self.resize(800, 600)  # Set the window size
        layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        for god in gods:
            if god[0].startswith(initial):
                god_info = f"Name: {god[0]}"
                scroll_layout.addWidget(QLabel(god_info))
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        self.setLayout(layout)
class GodsListScreenDisplay(QWidget):
    def __init__(self, gods, letter, next_callback, back_callback):
        super().__init__()
        self.setWindowTitle(f"Gods List - {letter}")
        self.resize(800, 800)  # Set the window size to 800x600
        self.layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.update_gods_list(gods)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(next_callback)
        self.layout.addWidget(self.next_button)
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(back_callback)
        self.layout.addWidget(self.back_button)
        self.setLayout(self.layout)
    def update_gods_list(self, gods):
        # Clear the current layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        # Add new gods to the layout
        for god in gods:
            god_info = f"Name: {god[0]}"
            self.scroll_layout.addWidget(QLabel(god_info))
class EditPropertyWindow(QDialog):
    def __init__(self, property_name, current_value, submit_callback):
        super().__init__()
        self.setWindowTitle(f"Edit {property_name}")
        self.resize(400, 200)
        layout = QVBoxLayout()
        self.property_name = property_name
        self.input_field = QLineEdit(current_value)
        layout.addWidget(QLabel(f"Current {property_name}:"))
        layout.addWidget(self.input_field)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: submit_callback(self.property_name, self.input_field.text()))
        layout.addWidget(submit_button)
        self.setLayout(layout)
class GodsListScreenEdit(QDialog):
    def __init__(self, god, edit_callback):
        super().__init__()
        self.setWindowTitle("Edit God / Deity / Titan")
        self.resize(400, 300)
        layout = QVBoxLayout()
        self.god = god
        self.edit_buttons = {
            "Title": QPushButton("Edit Title"),
            "God of": QPushButton("Edit God of"),
            "Symbol": QPushButton("Edit Symbol"),
            "Greek Name": QPushButton("Edit Greek Name"),
            "Roman Name": QPushButton("Edit Roman Name"),
            "Description": QPushButton("Edit Description"),
            "Father Name": QPushButton("Edit Father Name"),
            "Mother Name": QPushButton("Edit Mother Name"),
            "Level Name": QPushButton("Edit Level Name")
        }
        for key, button in self.edit_buttons.items():
            button.clicked.connect(lambda _, k=key: edit_callback(k, self.god))
            layout.addWidget(button)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gods Database UI")
        layout = QVBoxLayout()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
        # self.add_button("Fetch and Print Gods", self.fetch_and_print_gods, layout)
        # self.add_button("Migrate Data", self.migrate_data, layout)
        # self.add_button("Get or Create Parent", self.get_or_create_parent, layout)
        # self.add_button("Get or Create Level", self.get_or_create_level, layout)
        self.add_button("Display Gods", self.display_gods, layout)
        self.add_button("Search God", self.show_search_god_form, layout)
        self.add_button("Search God by Letter", self.show_search_god_by_letter_form, layout)
        self.add_button("Add God", self.show_add_god_form, layout)
        self.add_button("Edit God", self.show_edit_god_form, layout)
        self.add_button("Delete God", self.show_delete_god_form, layout)
        # self.add_button("Show Menu", self.show_menu, layout)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.conn, self.cursor = self.create_connection()
    def add_button(self, label, function, layout):
        button = QPushButton(label)
        button.clicked.connect(function)
        layout.addWidget(button)

    #---------- Add God Section ----------# (Done)
    def add_god(self, name, title, god_of, symbol, greek_name, roman_name, description, father_name, mother_name, level_name):
        father_id = self.get_or_create_parent(father_name)
        mother_id = self.get_or_create_parent(mother_name)
        level_id = self.get_or_create_level(level_name)
        self.cursor.execute('''
            INSERT INTO gods (name, title, god_of, symbol, greek_name, roman_name, description, father_id, mother_id, level_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, title, god_of, symbol, greek_name, roman_name, description, father_id, mother_id, level_id))
        self.conn.commit()
        print("God / Deity / Titan added successfully!")
    def show_add_god_form(self):
        self.form_window = QWidget()
        self.form_window.setWindowTitle("Add God / Deity / Titan")
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.god_of_input = QLineEdit()
        self.title_input = QLineEdit()
        self.symbol_input = QLineEdit()
        self.greek_name_input = QLineEdit()
        self.roman_name_input = QLineEdit()
        self.description_input = QLineEdit()
        self.father_name_input = QLineEdit()
        self.mother_name_input = QLineEdit()
        self.level_name_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("God of:", self.god_of_input)
        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Symbol:", self.symbol_input)
        form_layout.addRow("Greek Name:", self.greek_name_input)
        form_layout.addRow("Roman Name:", self.roman_name_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Father Name:", self.father_name_input)
        form_layout.addRow("Mother Name:", self.mother_name_input)
        form_layout.addRow("Level Name:", self.level_name_input)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_add_god_form)
        form_layout.addWidget(submit_button)
        self.form_window.setLayout(form_layout)
        self.form_window.show()
    def submit_add_god_form(self):
        name = self.name_input.text()
        god_of = self.god_of_input.text()
        title = self.title_input.text()
        symbol = self.symbol_input.text()
        greek_name = self.greek_name_input.text()
        roman_name = self.roman_name_input.text()
        description = self.description_input.text()
        father_name = self.father_name_input.text()
        mother_name = self.mother_name_input.text()
        level_name = self.level_name_input.text()
        father_id = self.get_or_create_parent(father_name)
        mother_id = self.get_or_create_parent(mother_name)
        level_id = self.get_or_create_level(level_name)
        self.cursor.execute('''
            INSERT INTO gods (name, title, god_of, symbol, greek_name, roman_name, description, father_id, mother_id, level_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, title, god_of, symbol, greek_name, roman_name, description, father_id, mother_id, level_id))
        self.conn.commit()
        self.output.append("God / Deity / Titan added successfully!")
        self.form_window.close()
    #---------- Edit God Section ----------# (Done)
    def show_edit_god_window(self, god):
        def edit_callback(property_name, god):
            current_value = self.get_current_value(property_name, god)
            self.edit_property_window = EditPropertyWindow(property_name, current_value, self.submit_edit_god_property)
            self.edit_property_window.show()
        self.edit_god_window = GodsListScreenEdit(god, edit_callback)
        self.edit_god_window.show()
    def submit_edit_god_property(self, property_name, new_value):
        god_name = self.edit_god_window.god[0]  # Assuming the first element is the name
        if property_name == "Father Name":
            new_value = self.get_or_create_parent(new_value)
            self.cursor.execute('UPDATE gods SET father_id = ? WHERE name = ?', (new_value, god_name))
        elif property_name == "Mother Name":
            new_value = self.get_or_create_parent(new_value)
            self.cursor.execute('UPDATE gods SET mother_id = ? WHERE name = ?', (new_value, god_name))
        elif property_name == "Level Name":
            new_value = self.get_or_create_level(new_value)
            self.cursor.execute('UPDATE gods SET level_id = ? WHERE name = ?', (new_value, god_name))
        else:
            self.cursor.execute(f'UPDATE gods SET {property_name.lower().replace(" ", "_")} = ? WHERE name = ?', (new_value, god_name))
        self.conn.commit()
        self.output.append(f"{property_name} updated successfully!")
        self.edit_property_window.close()
    def show_edit_god_form(self):
        self.form_window = QWidget()
        self.form_window.setWindowTitle("Edit God / Deity / Titan")
        form_layout = QFormLayout()
        self.edit_name_input = QLineEdit()
        form_layout.addRow("Name:", self.edit_name_input)
        submit_button = QPushButton("Edit")
        submit_button.clicked.connect(self.submit_edit_god_form)
        form_layout.addWidget(submit_button)
        self.form_window.setLayout(form_layout)
        self.form_window.show()
    def submit_edit_god_form(self):
        name = self.edit_name_input.text().strip()
        self.cursor.execute('SELECT * FROM gods WHERE name = ?', (name,))
        god = self.cursor.fetchone()
        if god:
            self.show_edit_god_window(god)
        else:
            self.output.append("God / Deity / Titan not found!")
        self.form_window.close()
    def edit_god(self, name, new_name=None, new_title=None, new_god_of=None, new_symbol=None, new_greek_name=None, new_roman_name=None, new_description=None, new_father_name=None, new_mother_name=None, new_level_name=None):
        god = self.search_god(name)
        if not god:
            print("God / Deity / Titan not found.")
            return
        if new_name:
            self.cursor.execute('UPDATE gods SET name = ? WHERE name = ?', (new_name, name))
        if new_title:
            self.cursor.execute('UPDATE gods SET title = ? WHERE name = ?', (new_title, name))
        if new_god_of:
            self.cursor.execute('UPDATE gods SET god_of = ? WHERE name = ?', (new_god_of, name))
        if new_symbol:
            self.cursor.execute('UPDATE gods SET symbol = ? WHERE name = ?', (new_symbol, name))
        if new_greek_name:
            self.cursor.execute('UPDATE gods SET greek_name = ? WHERE name = ?', (new_greek_name, name))
        if new_roman_name:
            self.cursor.execute('UPDATE gods SET roman_name = ? WHERE name = ?', (new_roman_name, name))
        if new_description:
            self.cursor.execute('UPDATE gods SET description = ? WHERE name = ?', (new_description, name))
        if new_father_name:
            father_id = self.get_or_create_parent(new_father_name)
            self.cursor.execute('UPDATE gods SET father_id = ? WHERE name = ?', (father_id, name))
        if new_mother_name:
            mother_id = self.get_or_create_parent(new_mother_name)
            self.cursor.execute('UPDATE gods SET mother_id = ? WHERE name = ?', (mother_id, name))
        if new_level_name:
            level_id = self.get_or_create_level(new_level_name)
            self.cursor.execute('UPDATE gods SET level_id = ? WHERE name = ?', (level_id, name))
        self.conn.commit()
        print("God / Deity / Titan updated successfully!")
        self.cursor.execute('SELECT name FROM levels WHERE id = ?', (level_id,))
        level = self.cursor.fetchone()
        return level[0] if level else "Unknown"
    #---------- Search God Section ----------# (Done)
    def search_god(self):
        self.submit_search_god_form()
    def show_search_god_form(self):
        self.search_window = QWidget()
        self.search_window.setWindowTitle("Search God / Deity / Titan")
        form_layout = QFormLayout()
        self.search_name_input = QLineEdit()
        form_layout.addRow("Name:", self.search_name_input)
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.submit_search_god_form)
        form_layout.addWidget(search_button)
        self.search_window.setLayout(form_layout)
        self.search_window.show()
    def submit_search_god_form(self):
        name = self.search_name_input.text()
        self.cursor.execute('SELECT * FROM gods WHERE name = ?', (name,))
        god = self.cursor.fetchone()
        if god:
            # Fetch the corresponding names for Father, Mother, and Level
            self.cursor.execute('SELECT name FROM parents WHERE id = ?', (god[7],))
            father_name = self.cursor.fetchone()
            father_name = father_name[0] if father_name else "Unknown"
            self.cursor.execute('SELECT name FROM parents WHERE id = ?', (god[8],))
            mother_name = self.cursor.fetchone()
            mother_name = mother_name[0] if mother_name else "Unknown"
            self.cursor.execute('SELECT name FROM levels WHERE id = ?', (god[9],))
            level_name = self.cursor.fetchone()
            level_name = level_name[0] if level_name else "Unknown"
            # Ensure the description is treated as a string
            description = str(god[6])
            paragraphs = description.split('\n')
            formatted_description = description.replace('. ', '.\t\n')
            god_info = {
                "Name": god[0],
                "Title": god[1],
                "God of": god[2],
                "Symbol": god[3],
                "Greek Name": god[4],
                "Roman Name": god[5],
                "Description": formatted_description,
                "Father": father_name,
                "Mother": mother_name,
                "Level": level_name
            }
            self.show_god_info(god_info)
        else:
            self.output.append("God / Deity / Titan not found.")
    #---------- Search God by Letter Section ----------# (Done), Could Optimize and Come back to this.
    def show_search_god_by_letter_form(self):
        self.form_window = QWidget()
        self.form_window.setWindowTitle("Search God / Deity / Titan by Letter")
        form_layout = QFormLayout()
        self.search_letter_input = QLineEdit()
        form_layout.addRow("Letter or Word:", self.search_letter_input)
        submit_button = QPushButton("Search")
        submit_button.clicked.connect(self.submit_search_god_by_letter_form)
        form_layout.addWidget(submit_button)
        self.form_window.setLayout(form_layout)
        self.form_window.show()
    def submit_search_god_by_letter_form(self):
        letter = self.search_letter_input.text().strip()
        self.cursor.execute('SELECT * FROM gods WHERE name LIKE ?', ('%' + letter + '%',))
        gods = self.cursor.fetchall()
        if gods:
            self.show_gods_list(gods, initial=letter)
        else:
            self.output.append("No gods found matching the letter or keyword.")
        self.form_window.close()
    def search_god_by_letter(self, letter):
        self.submit_search_god_by_letter_form()
    def show_gods_list(self, gods, initial):
        self.gods_list_screen = GodsListScreen(gods, initial)
        self.gods_list_screen.show()
    #---------- Delete God Section ----------# (Done)
    def delete_god(self, name):
        self.cursor.execute('DELETE FROM gods WHERE name = ?', (name,))
        self.conn.commit()
        print("God / Deity / Titan deleted successfully!")
    def show_delete_god_form(self):
        self.form_window = QWidget()
        self.form_window.setWindowTitle("Delete God / Deity / Titan")
        form_layout = QFormLayout()
        self.delete_name_input = QLineEdit()
        form_layout.addRow("Name:", self.delete_name_input)
        submit_button = QPushButton("Delete")
        submit_button.clicked.connect(self.submit_delete_god_form)
        form_layout.addWidget(submit_button)
        self.form_window.setLayout(form_layout)
        self.form_window.show()
    def submit_delete_god_form(self):
        name = self.delete_name_input.text().strip()
        self.cursor.execute('DELETE FROM gods WHERE name = ?', (name,))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            self.output.append("God / Deity / Titan deleted successfully!")
        else:
            self.output.append("God / Deity / Titan not found!")
        self.form_window.close()
    #---------- Display Gods Section ----------# (Done)
    def display_gods(self):
        self.current_letter = 'A'
        self.display_gods_by_letter()
    def display_gods_by_letter(self):
        self.cursor.execute('SELECT * FROM gods WHERE name LIKE ? ORDER BY name', (self.current_letter + '%',))
        gods = self.cursor.fetchall()
        if gods:
            self.show_gods_list_with_pagination(gods, self.current_letter)
        else:
            # self.output.append(f"No gods found starting with {self.current_letter}.")
            self.current_letter = chr(ord(self.current_letter) + 1)
            if self.current_letter <= 'Z':
                self.display_gods_by_letter()
    def show_gods_list_with_pagination(self, gods, letter):
        def next_callback():
            self.gods_list_screen.close()
            self.current_letter = chr(ord(letter) + 1)
            if self.current_letter <= 'Z':
                self.display_gods_by_letter()
        def back_callback():
            self.gods_list_screen.close()
            self.current_letter = chr(ord(letter) + -1)
            if self.current_letter <= 'Z':
                self.display_gods_by_letter()
        self.gods_list_screen = GodsListScreenDisplay(gods, letter, next_callback, back_callback)
        self.gods_list_screen.show()
    #---------- Flag God Section ----------#
    def show_flag_god_form(self):
        self.form_window = QWidget()
        self.form_window.setWindowTitle("Flag God / Deity / Titan")
        form_layout = QFormLayout()
        self.flag_name_input = QLineEdit()
        form_layout.addRow("Name:", self.flag_name_input)
        submit_button = QPushButton("Flag")
        submit_button.clicked.connect(self.submit_flag_god_form)
        form_layout.addWidget(submit_button)
        self.form_window.setLayout(form_layout)
        self.form_window.show()
    def submit_flag_god_form(self):
        name = self.flag_name_input.text().strip()
        self.cursor.execute('UPDATE gods SET flagged = TRUE WHERE name = ?', (name,))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            self.output.append("God / Deity / Titan flagged successfully!")
        else:
            self.output.append("God / Deity / Titan not found!")
        self.form_window.close()
    #---------- Unflag God Section ----------#
    def unflag_god(self):
        self.cursor.execute('''
            SELECT name, title, god_of, symbol, greek_name, roman_name, description
            FROM gods
            WHERE flagged = TRUE
        ''')
        flagged_gods = self.cursor.fetchall()
        if flagged_gods:
            msg = QMessageBox()
            msg.setWindowTitle("Flagged Gods")
            msg.setText("Select a God / Deity / Titan to unflag:")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Ok)
            for index, god in enumerate(flagged_gods, start=1):
                msg.setInformativeText(f"Record {index}: Name: {god[0]}")
            ret = msg.exec_()
            if ret == QMessageBox.Ok:
                selected_index = int(input("Enter the record number of the God / Deity / Titan you want to unflag: ").strip()) - 1
                if 0 <= selected_index < len(flagged_gods):
                    selected_god = flagged_gods[selected_index][0]
                    self.cursor.execute('UPDATE gods SET flagged = FALSE WHERE TRIM(name) = ?', (selected_god,))
                    self.conn.commit()
                    if self.cursor.rowcount > 0:
                        self.output.append(f"The record for {selected_god} has been unflagged.")
                    else:
                        self.output.append(f"No flagged record found for {selected_god}.")
                else:
                    self.output.append("Invalid record number.")
            else:
                self.output.append("No action taken.")
        else:
            self.output.append("No flagged records found.")
    #---------- Menu Section ----------#
    #---------- SQLite / Tables Section ----------#
    def fetch_and_print_gods(self, query, params=()):
        self.cursor.execute(query, params)
        gods = self.cursor.fetchall()
        if gods:
            gods_by_initial = {}
            for god in gods:
                if god and god[0]:  # Check if god is not empty and has at least one character
                    initial = god[0][0].upper()
                    if initial not in gods_by_initial:
                        gods_by_initial[initial] = []
                    gods_by_initial[initial].append(god)
            for initial in sorted(gods_by_initial.keys()):
                self.output.append(f"Initial: {initial}")
                self.output.append("#--------------------------------#")
                for god in gods_by_initial[initial]:
                    self.output.append(god[0])
                self.output.append("#--------------------------------#")
            self.output.append(f"\nTotal Gods / Deities / Titans: {len(gods)}")
            self.output.append("#--------------------------------#")
            selected_god = input("Enter the name of the God / Deity / Titan you want to display: ").strip()
            self.cursor.execute('''
                SELECT gods.*, p1.name AS father_name, p2.name AS mother_name, l.name AS level_name
                FROM gods
                LEFT JOIN parents p1 ON gods.father_id = p1.id
                LEFT JOIN parents p2 ON gods.mother_id = p2.id
                LEFT JOIN levels l ON gods.level_id = l.id
                WHERE TRIM(gods.name) = ? AND gods.flagged = FALSE
            ''', (selected_god,))
            god = self.cursor.fetchone()
            if god:
                self.output.append(f"\033[1mName:\033[0m {god[0]}")
                self.output.append(f"\033[1mTitle:\033[0m {god[1]}")
                self.output.append(f"\033[1mGod of:\033[0m {god[2]}")
                self.output.append(f"\033[1mSymbol:\033[0m {god[3]}")
                self.output.append(f"\033[1mGreek Name:\033[0m {god[4]}")
                self.output.append(f"\033[1mRoman Name:\033[0m {god[5]}")
                self.output.append(f"\033[1mDescription:\033[0m {textwrap.fill(god[6], width=70)}")  # Adjust width as needed
                self.output.append(f"\033[1mFather:\033[0m {god[11]}")  # father_name
                self.output.append(f"\033[1mMother:\033[0m {god[12]}")  # mother_name
                self.output.append(f"\033[1mLevel of God:\033[0m {god[13]}")  # level_name
            else:
                self.output.append("God / Deity / Titan not found or is flagged.")
        else:
            self.output.append("No Gods / Deities / Titans found!")
    def create_connection(self):
        conn = sqlite3.connect('gods.db')
        cursor = conn.cursor()
        self.create_parent_table(cursor)
        self.create_levels_table(cursor)
        self.create_gods_table(cursor)
        self.create_log_table(cursor)
        self.create_triggers(cursor)
        self.migrate_data(cursor)
        conn.commit()
        return conn, cursor
    def create_parent_table(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
    def create_levels_table(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
    def create_gods_table(self, cursor):
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
                flagged BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (father_id) REFERENCES parents(id),
                FOREIGN KEY (mother_id) REFERENCES parents(id),
                FOREIGN KEY (level_id) REFERENCES levels(id)
            )
        ''')
    def create_log_table(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS god_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                god_name TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    def create_triggers(self, cursor):
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
    def migrate_data(self, cursor):
        cursor.execute('SELECT * FROM gods')
        gods = cursor.fetchall()
        for god in gods:
            cursor.execute('''
                INSERT INTO gods_new (name, title, god_of, symbol, greek_name, roman_name, description, father_id, mother_id, level_id, flagged)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (god[0], god[1], god[2], god[3], god[4], god[5], god[6], god[7], god[8], god[9], god[10]))  # Include flagged column

        cursor.execute('DROP TABLE gods')
        cursor.execute('ALTER TABLE gods_new RENAME TO gods')
    def get_or_create_parent(self, name):
        self.cursor.execute('SELECT id FROM parents WHERE name = ?', (name,))
        parent = self.cursor.fetchone()
        if parent:
            return parent[0]
        else:
            self.cursor.execute('INSERT INTO parents (name) VALUES (?)', (name,))
            self.conn.commit()
            return self.cursor.lastrowid
    def get_or_create_level(self, level):
        self.cursor.execute('SELECT id FROM levels WHERE name = ?', (level,))
        level_record = self.cursor.fetchone()
        if level_record:
            return level_record[0]
        else:
            self.cursor.execute('INSERT INTO levels (name) VALUES (?)', (level,))
            self.conn.commit()
            return self.cursor.lastrowid
    def show_god_info(self, god_info):
        self.god_info_window = GodInfoScreen(god_info)
        self.god_info_window.show()
    def get_current_value(self, property_name, god):
        property_map = {
            "Title": god[1],
            "God of": god[2],
            "Symbol": god[3],
            "Greek Name": god[4],
            "Roman Name": god[5],
            "Description": god[6],
            "Father Name": self.get_parent_name(god[7]),
            "Mother Name": self.get_parent_name(god[8]),
            "Level Name": self.get_level_name(god[9])
        }
        return property_map[property_name]
    def get_parent_name(self, parent_id):
        self.cursor.execute('SELECT name FROM parents WHERE id = ?', (parent_id,))
        parent = self.cursor.fetchone()
        return parent[0] if parent else "Unknown"
    def get_level_name(self, level_id):
        self.cursor.execute('SELECT name FROM levels WHERE id = ?', (level_id,))
        level = self.cursor.fetchone()
        return level[0] if level else "Unknown"
    
    # def show_menu(self):
    #     print("1. Add a God / Deity / Titan")
    #     print("2. Search for a God / Deity / Titan's information")
    #     print("3. Search for a God / Deity / Titan by letter or key word")
    #     print("4. Delete a God / Deity / Titan")
    #     print("5. Display all Gods / Deities / Titans")
    #     print("6. Edit a God / Deity / Titan")
    #     print("7. Flag a God / Deity / Titan")
    #     print("8. Unflag a God / Deity / Titan")
    #     print("9. Exit")
    #     choice = input("Enter your choice: ")
    #     return choice

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()