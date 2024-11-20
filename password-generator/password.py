import sys
import random
import string
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon

class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Generator")
        self.setGeometry(100, 100, 400, 250)

        # Set a more attractive background color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#e0f7fa"))  # Light blue background
        self.setPalette(palette)

        # Set main font style
        font = QFont('Arial', 10)
        self.setFont(font)

        # Main layout
        layout = QVBoxLayout()

        # Title Label
        title = QLabel("Generate a Strong Password")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #00796b;")  # Dark cyan text
        layout.addWidget(title)

        # Length label (above the TextField)
        self.length_label = QLabel("Password Length:")
        self.length_label.setFont(QFont('Arial', 11))
        self.length_label.setStyleSheet("color: #00796b;")  # Dark cyan text
        layout.addWidget(self.length_label)

        # Input layout for length
        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText("Enter length")
        self.length_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #00796b;
                border-radius: 5px;
                background-color: #ffffff;
                color: #000000;
            }
        """)
        layout.addWidget(self.length_input)

        # Button to generate password
        self.generate_button = QPushButton("Generate Password")
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #00796b;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #004d40;
            }
        """)
        self.generate_button.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_button)

        # Horizontal layout for password and copy button
        password_layout = QHBoxLayout()

        # Label to display the generated password
        self.password_label = QLabel("")
        self.password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.password_label.setStyleSheet("color: #00796b;")
        password_layout.addWidget(self.password_label)

        # Copy button with an icon (hidden by default)
        self.copy_button = QPushButton()
        self.copy_button.setIcon(QIcon.fromTheme("edit-copy"))
        self.copy_button.setFixedSize(30, 30)
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #676e69;
                border: 1px solid #00796b;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #525954;
            }
        """)
        self.copy_button.setToolTip("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setVisible(False)  # Hide initially
        password_layout.addWidget(self.copy_button)

        layout.addLayout(password_layout)

        # Set the layout
        self.setLayout(layout)

    def generate_password(self):
        try:
            length = int(self.length_input.text())
            if length < 1:
                raise ValueError

            # Characters to be used in the password
            characters = string.ascii_letters + string.digits + string.punctuation

            # Generate random password
            password = ''.join(random.choice(characters) for _ in range(length))

            # Display the password and show the copy button
            self.password_label.setText(password)
            self.copy_button.setVisible(True)  # Show the copy button
        except ValueError:
            self.show_error_message("Please enter a valid number for password length!")

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_label.text())
        QMessageBox.information(self, "Copied", "Password copied to clipboard!")

    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setWindowTitle("Input Error")
        error_dialog.setText(message)
        error_dialog.setIcon(QMessageBox.Icon.Warning)
        error_dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec())
