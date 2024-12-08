from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QPixmap

class GodInfoScreen(QWidget):
    def __init__(self, god_info, image_path):
        super().__init__()
        self.setWindowTitle("God Information")
        layout = QVBoxLayout()

        # Add text information
        for key, value in god_info.items():
            layout.addWidget(QLabel(f"{key}: {value}"))

        # Add image
        image_label = QLabel()
        pixmap = QPixmap(image_path)

        # Scale the image to fit within a specific size (e.g., 400x400)
        scaled_pixmap = pixmap.scaled(400, 400, aspectRatioMode=True, transformMode=True)
        image_label.setPixmap(scaled_pixmap)
        layout.addWidget(image_label)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(800, 600)

        # Example data
        god_info = {"Name": "Zeus", "Title": "King of the Gods"}
        image_path = r"C:\Users\tenor\OneDrive\Documents\GitHub\pf24-greek-god-encyclopedia\Test_UI\Zeus.jpg"  # Replace with the path to your image

        self.god_info_screen = GodInfoScreen(god_info, image_path)
        self.setCentralWidget(self.god_info_screen)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())