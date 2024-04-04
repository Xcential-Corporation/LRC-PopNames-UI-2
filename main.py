import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == '__main__':
    print("Starting the application...")
    app = QApplication(sys.argv)
    print("Creating the main window...")
    window = MainWindow()
    print("Showing the main window...")
    window.show()
    print("Executing the application...")
    sys.exit(app.exec())