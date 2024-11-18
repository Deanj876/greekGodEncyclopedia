# ui.py
import sys
import sqlite3
import textwrap
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QTextEdit, QFormLayout, QMessageBox, QDialog
import sys
# from functions import (
#     fetch_and_print_gods, migrate_data, get_or_create_parent, get_or_create_level,
#     add_god, search_god, search_god_by_letter, delete_god, display_gods, edit_god, menu
# )

class GodInfoWindow(QDialog):
    def __init__(self, god_info):
        super().__init__()
        self.setWindowTitle("God Information")
        layout = QVBoxLayout()

        for key, value in god_info.items():
            layout.addWidget(QLabel(f"{key}: {value}"))

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gods Database UI")

        layout = QVBoxLayout()

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.add_button("Add God", self.show_add_god_form, layout)
        self.add_button("Search God", self.show_search_god_form, layout)
        self.add_button("Search God by Letter", self.show_search_god_by_letter_form, layout)
        self.add_button("Delete God", self.show_delete_god_form, layout)
        self.add_button("Display Gods", self.display_gods, layout)
        self.add_button("Edit God", self.show_edit_god_form, layout)
        self.add_button("Flag God", self.show_flag_god_form, layout)
        self.add_button("Unflag God", self.unflag_god, layout)
        self.add_button("Show Menu", self.show_menu, layout)

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
    #---------- Edit God Section ----------#
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
            self.edit_god_details(god)
        else:
            self.output.append("God / Deity / Titan not found!")
        self.form_window.close()
    def edit_god_details(self, god):
        self.edit_form_window = QWidget()
        self.edit_form_window.setWindowTitle("Edit God / Deity / Titan Details")

        form_layout = QFormLayout()

        self.edit_title_input = QLineEdit(god[1])
        self.edit_god_of_input = QLineEdit(god[2])
        self.edit_symbol_input = QLineEdit(god[3])
        self.edit_greek_name_input = QLineEdit(god[4])
        self.edit_roman_name_input = QLineEdit(god[5])
        self.edit_description_input = QLineEdit(god[6])
        self.edit_father_name_input = QLineEdit(god[7])
        self.edit_mother_name_input = QLineEdit(god[8])
        self.edit_level_name_input = QLineEdit(god[9])

        form_layout.addRow("Title:", self.edit_title_input)
        form_layout.addRow("God of:", self.edit_god_of_input)
        form_layout.addRow("Symbol:", self.edit_symbol_input)
        form_layout.addRow("Greek Name:", self.edit_greek_name_input)
        form_layout.addRow("Roman Name:", self.edit_roman_name_input)
        form_layout.addRow("Description:", self.edit_description_input)
        form_layout.addRow("Father Name:", self.edit_father_name_input)
        form_layout.addRow("Mother Name:", self.edit_mother_name_input)
        form_layout.addRow("Level Name:", self.edit_level_name_input)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.submit_edit_god_details(god[0]))
        form_layout.addWidget(submit_button)

        self.edit_form_window.setLayout(form_layout)
        self.edit_form_window.show()
    def submit_edit_god_details(self, name):
        title = self.edit_title_input.text()
        god_of = self.edit_god_of_input.text()
        symbol = self.edit_symbol_input.text()
        greek_name = self.edit_greek_name_input.text()
        roman_name = self.edit_roman_name_input.text()
        description = self.edit_description_input.text()
        father_name = self.edit_father_name_input.text()
        mother_name = self.edit_mother_name_input.text()
        level_name = self.edit_level_name_input.text()

        father_id = self.get_or_create_parent(father_name)
        mother_id = self.get_or_create_parent(mother_name)
        level_id = self.get_or_create_level(level_name)

        self.cursor.execute('''
            UPDATE gods
            SET title = ?, god_of = ?, symbol = ?, greek_name = ?, roman_name = ?, description = ?, father_id = ?, mother_id = ?, level_id = ?
            WHERE name = ?
        ''', (title, god_of, symbol, greek_name, roman_name, description, father_id, mother_id, level_id, name))
        self.conn.commit()

        self.output.append("God / Deity / Titan information updated successfully!")
        self.edit_form_window.close()
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
    #---------- Search God by Letter Section ----------#
    def search_god_by_letter(self, letter):
        self.cursor.execute('SELECT * FROM gods WHERE name LIKE ?', (letter + '%',))
        gods = self.cursor.fetchall()
        for god in gods:
            print(god)
    def submit_search_god_by_letter_form(self):
        letter = self.search_letter_input.text().strip()
        self.fetch_and_print_gods('SELECT name FROM gods WHERE TRIM(name) LIKE ? AND flagged = FALSE', ('%' + letter + '%',))
        self.form_window.close()
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
    #---------- Delete God Section ----------# (Delete)
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
    #---------- Display Gods Section ----------#
    def display_gods(self):
        self.fetch_and_print_gods('SELECT name FROM gods WHERE flagged = FALSE ORDER BY name')
    def display_gods(self):
        self.cursor.execute('SELECT * FROM gods')
        gods = self.cursor.fetchall()
        for god in gods:
            print(god)
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
        self.god_info_window = GodInfoWindow(god_info)
        self.god_info_window.show()


    # def menu(self):
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
    
    def show_menu(self):
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

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()