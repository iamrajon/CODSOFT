import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QListWidgetItem, QInputDialog
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from database import add_todo, fetch_todos, update_todo, delete_todo


class TodoListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()

    def settings(self):
        self.setGeometry(600, 200, 400, 450)
        self.setWindowTitle("To-Do List App")

    # Design the User Interface of App
    def initUI(self):
        # create all widget objects
        widget = QWidget()
        self.setCentralWidget(widget)
        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)

        # Title label
        title = QLabel("To-Do List")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Input field and button
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter new task...")
        input_layout.addWidget(self.task_input)

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        input_layout.addWidget(self.add_button)

        main_layout.addLayout(input_layout)

        # To-Do list widget
        self.todo_list_widget = QListWidget()
        main_layout.addWidget(self.todo_list_widget)
        # self.todo_list_widget.itemClicked.connect(self.load_task)

        # Update and Delete buttons
        button_layout = QHBoxLayout()
        self.update_button = QPushButton("Update Task")
        self.update_button.clicked.connect(self.update_task)
        self.update_button.setObjectName("btn_update")   # acts as id for chasnging the color of button
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.clicked.connect(self.delete_task)
        self.delete_button.setObjectName("btn_delete")   # act as id for changing the color of the button
        button_layout.addWidget(self.delete_button)

        main_layout.addLayout(button_layout)

        # style the widgets with css
        self.style_widgets()

        # function call to load all tasks to User Interface
        self.load_tasks()

    # function to sltyle the widgets with css
    def style_widgets(self):
        self.setStyleSheet(
            """
                QWidget {
                    background-color: #ffffff; /* Set background to white */
                    font-family: Arial, sans-serif;
                    color: #000000
                }
                QLabel {
                    font-size: 20px;
                    font-weight: bold;
                    color: #333333; /* Darker text color for contrast */
                }
                QLineEdit {
                    font-size: 16px;
                    padding: 8px;
                    border: 1px solid #888888; /* Border for input field */
                    border-radius: 5px;
                    background-color: #f2f2f2; /* Light gray background for input field */
                    color: #000000;
                }
                QPushButton {
                    background-color: #4CAF50; /* Green button */
                    color: #ffffff; /* White text */
                    font-size: 16px;
                    padding: 8px;
                    border-radius: 5px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #45a049; /* Darker green on hover */
                }

                /* Edit and Delete button  */
                #btn_delete {
                    background-color: #ff102e; /* Red Button */
                    color: #ffffff; /* White text */
                    font-size: 16px;
                    padding: 8px;
                    border-radius: 5px;
                    border: none;
                }

                #btn_delete:hover {
                    background-color: #ff108d;
                }

                #btn_update {
                    background-color: #008CBA; /* Blue button */
                    color: #ffffff; /* White text */
                    font-size: 16px;
                    padding: 8px;
                    border-radius: 5px;
                    border: none;
                }

                #btn_update:hover {
                    background-color: #005CBA;
                }


                QListWidget {
                    font-size: 16px;
                    color: #333333; /* Darker text color for list */
                    border: 1px solid #888888;
                    border-radius: 5px;
                    background-color: #f9f9f9; /* Light gray for better contrast */
                }
            """
        )

    # clear the inputs form
    def clear_inputs(self):
        self.task_input.clear()

    # add new task to database
    def add_task(self):
        task = self.task_input.text() #get text from QLIneEdit
        if not task:
            QMessageBox.warning(self, "Input Error", "Task Cannot Be empty!")
            return
        
        if add_todo(task):
            # load task list
            self.load_tasks()
            
            # clear the form
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "Failed to add task!")

    # load all tha tasks to UI being fetched from datagase
    def load_tasks(self):
        self.todo_list_widget.clear() 
        todos_list = fetch_todos()

        for todo in todos_list:
            task_id = todo[0]
            task_text = todo[1]
            
            # create a QListWidgetItem
            item = QListWidgetItem(task_text)

            # Associate task ID with the item for later use
            item.setData(Qt.ItemDataRole.UserRole, task_id)

            # Add the item to the list widget
            self.todo_list_widget.addItem(item)

    # load a particular task to input field for updation or editing
    def load_task(self, item):
        self.task_input.setText(item.text())

    # update the selected task and display the change too UI
    def update_task(self):
        current_item = self.todo_list_widget.currentItem()

        if not current_item:
            QMessageBox.warning(self, "Input Error", "Please select the item for Updation!")
            return
        
        # Get the task ID from the item metadata
        task_id = current_item.data(Qt.ItemDataRole.UserRole)

        # Prompt the user for a new task text
        new_task_text, ok = QInputDialog.getText(self, "Update Task", "Edit Your task:", text=current_item.text())

        if not ok or not new_task_text.strip():  # User cancelled or entered an empty string
            return
        
        # Update the database
        if update_todo(task_id, new_task_text.strip()):
            # Reflect the change in the UI
            current_item.setText(new_task_text.strip())
            print("Task updated successfully.")
        else:
            QMessageBox.critical(self, "Error", "Failed to Update the task!")

    # Delete the selected task and reflect the change to UI
    def delete_task(self):
        current_item = self.todo_list_widget.currentItem()

        if not current_item:
            print("No task selected.")
            QMessageBox.warning(self, "Selection Error", "Please Select an Item for Deletion!")
            return
        
        # Get the task ID from the item metadata
        task_id = current_item.data(Qt.ItemDataRole.UserRole)

        # Confirm the deletion with the user
        confirm = QMessageBox.question(
            self,
            "Delete Task",
            f"Are you sure you want to delete the task: '{current_item.text()}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            # Delete the task from the database
            if delete_todo(task_id):
                # Remove the item from the QListWidget
                self.todo_list_widget.takeItem(self.todo_list_widget.row(current_item))
                print("Task deleted successfully.")
            else:
                print("Failed to delete task.")
                QMessageBox.critical(self, "Error", "Unable to Delete the Task!")


