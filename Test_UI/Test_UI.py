from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QLineEdit, QDialog

class GodInfoScreen(QWidget):
    def __init__(self, god_info):
        super().__init__()
        self.setWindowTitle("God Information")
        layout = QVBoxLayout()

        for key, value in god_info.items():
            layout.addWidget(QLabel(f"{key}: {value}"))

        self.setLayout(layout)

class GodsListScreen(QWidget):
    def __init__(self, gods):
        super().__init__()
        self.setWindowTitle("Gods List")
        layout = QVBoxLayout()

        for god in gods:
            god_info = f"Name: {god[0]}"
            layout.addWidget(QLabel(god_info))

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

class DisplayScreens(QWidget):
    def __init__(self, god_info, gods, next_callback, back_callback):
        super().__init__()
        self.layout = QVBoxLayout()

        self.god_info_screen = GodInfoScreen(god_info)
        self.gods_list_screen = GodsListScreen(gods)
        self.gods_list_screen_display = GodsListScreenDisplay(gods, "A", next_callback, back_callback)

        self.layout.addWidget(self.god_info_screen)
        self.layout.addWidget(self.gods_list_screen)
        self.layout.addWidget(self.gods_list_screen_display)

        self.setLayout(self.layout)

class EditDialogs(QWidget):
    def __init__(self, god, edit_callback, submit_callback):
        super().__init__()
        self.layout = QVBoxLayout()

        self.edit_property_window = EditPropertyWindow("Title", "Current Value", submit_callback)
        self.gods_list_screen_edit = GodsListScreenEdit(god, edit_callback)

        self.layout.addWidget(self.edit_property_window)
        self.layout.addWidget(self.gods_list_screen_edit)

        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(800, 600)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Example data
        god_info = {"Name": "Zeus", "Title": "King of the Gods"}
        gods = [("Zeus",), ("Hera",), ("Poseidon",)]

        # Create instances of groups
        self.display_screens = DisplayScreens(god_info, gods, self.next_callback, self.back_callback)
        self.edit_dialogs = EditDialogs(god_info, self.edit_callback, self.submit_callback)

        # Add groups to the stacked widget
        self.central_widget.addWidget(self.display_screens)
        self.central_widget.addWidget(self.edit_dialogs)

        # Set the initial screen
        self.central_widget.setCurrentWidget(self.display_screens)

    def next_callback(self):
        # Fetch new gods list for the next page
        new_gods = [("Apollo",), ("Artemis",)]
        self.display_screens.gods_list_screen_display.update_gods_list(new_gods)
        self.central_widget.setCurrentWidget(self.display_screens)

    def back_callback(self):
        # Fetch new gods list for the previous page
        new_gods = [("Zeus",), ("Hera",), ("Poseidon",)]
        self.display_screens.gods_list_screen_display.update_gods_list(new_gods)
        self.central_widget.setCurrentWidget(self.display_screens)

    def edit_callback(self, property_name, god):
        # Show edit dialog for the selected property
        self.central_widget.setCurrentWidget(self.edit_dialogs)

    def submit_callback(self, property_name, new_value):
        # Handle the submission of the edited property
        print(f"Updated {property_name} to {new_value}")
        self.central_widget.setCurrentWidget(self.display_screens)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())