# All imports
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QFont

class CalculatorApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QT_Calculator App")
        self.resize(350, 400)

        # All Widgets/Objects
        self.text_box = QLineEdit()
        self.text_box.setFont(QFont("Helvetica", 32))
        self.text_box.setStyleSheet("background-color: #2d2d2d; color: white; padding: 10px; border-radius: 5px;")

        self.grid = QGridLayout()

        self.buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]
        # for loop for showing all buttons
        row = 0
        col = 0 

        for text in self.buttons:
            button = QPushButton(text)
            button.clicked.connect(self.button_click)
            button.setStyleSheet(
                "QPushButton {font: 25pt Comic Sans MS; padding: 10px; background-color: #454545; color: white; border-radius: 5px;}"
                "QPushButton:hover { background-color: #5e5e5e; }"
            )
            self.grid.addWidget(button, row, col)
            col += 1

            if col > 3:
                col = 0
                row += 1

        self.clear = QPushButton("Clear")
        self.clear.setStyleSheet(
            "QPushButton {font: 25pt Comic Sans MS; padding: 10px; background-color: #d9534f; color: white; border-radius: 5px;}"
            "QPushButton:hover { background-color: #c9302c; }"
        )

        self.delete = QPushButton("<-")
        self.delete.setStyleSheet(
            "QPushButton {font: 25pt Comic Sans MS; padding: 10px; background-color: #f0ad4e; color: white; border-radius: 5px;}"
            "QPushButton:hover { background-color: #ec971f; }"
        )

        # Designs
        master_layout = QVBoxLayout()
        master_layout.addWidget(self.text_box)
        master_layout.addLayout(self.grid)

        button_row = QHBoxLayout()
        button_row.addWidget(self.clear)
        button_row.addWidget(self.delete)

        master_layout.addLayout(button_row)
        master_layout.setContentsMargins(25, 25, 25, 25)

        # set main layout of application
        self.setLayout(master_layout)

        self.clear.clicked.connect(self.button_click)
        self.delete.clicked.connect(self.button_click)

    def button_click(self):
        button = self.sender()
        text = button.text()

        if text == "=":
            symbol = self.text_box.text()
            try:
                res = eval(symbol)
                self.text_box.setText(str(res))
            except Exception as e:
                print("Error: ", e)

        elif text == "Clear":
            self.text_box.clear()

        elif text == "<-":
            current_value = self.text_box.text()
            self.text_box.setText(current_value[:-1])
        else:
            current_value = self.text_box.text()
            self.text_box.setText(current_value + text)

if __name__ == "__main__":
    app = QApplication([])
    main_window = CalculatorApp()
    # Background gradient
    main_window.setStyleSheet("""
        QWidget { 
            background-color: #f0f0f8; 
            background-image: linear-gradient(45deg, #303841, #3a4750);
        }
    """)
    main_window.show()
    app.exec()
