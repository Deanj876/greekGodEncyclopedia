# ui.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from functions_Test import clear_screen, greet, create_connection, menu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple PyQt UI")

        layout = QVBoxLayout()

        self.greet_button = QPushButton("Greet")
        self.greet_button.clicked.connect(self.greet_user)
        layout.addWidget(self.greet_button)

        self.clear_button = QPushButton("Clear Screen")
        self.clear_button.clicked.connect(self.clear_screen)
        layout.addWidget(self.clear_button)

        self.menu_button = QPushButton("Show Menu")
        self.menu_button.clicked.connect(self.show_menu)
        layout.addWidget(self.menu_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def greet_user(self):
        greet("John Doe")

    def clear_screen(self):
        clear_screen()

    def show_menu(self):
        choice = menu()
        print(f"Menu choice: {choice}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()