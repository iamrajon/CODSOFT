import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from app import TodoListApp
from database import init_db


def main():
    app = QApplication(sys.argv)

    if not init_db("todos.db"):
        QMessageBox.critical(None, "Error", "Could Not lead your Database..")
        sys.exit(1)

    window = TodoListApp()
    window.show()

    # Start ehe event loop
    sys.exit(app.exec())


if __name__ in "__main__":
    main()
