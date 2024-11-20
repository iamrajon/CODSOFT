from PyQt6.QtSql import QSqlDatabase, QSqlQuery


def init_db(db_name):
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_name)

    if not database.open():
        return False
    
    sql = QSqlQuery()
    sql.exec(
        """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL
            );
        """
    )
    return True


# Adding todo to the database
def add_todo(task):
    query = QSqlQuery()
    query.prepare(
        "INSERT INTO todos (task) VALUES (?);"   
    )
    query.addBindValue(task)
    return query.exec()

# fetching all tasks from database
def fetch_todos():
    todos = []
    query = QSqlQuery()
    query.exec("SELECT * FROM todos;")

    while query.next():
        todos.append((query.value(0), query.value(1))) # get the value of first column (task)

    return todos

# updating the selected task to the database
def update_todo(task_id, new_task_text):
    query = QSqlQuery()
    query.prepare("UPDATE todos SET task = :task WHERE id = :id")
    query.bindValue(":task", new_task_text)
    query.bindValue(":id", task_id)

    if query.exec():
        return True
    else:
        print(f"Error updating task: {query.lastError().text()}")
        return False
    
# Deleting the selected task frm the database
def delete_todo(task_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM todos WHERE id = :id")
    query.bindValue(":id", task_id)

    if query.exec():
        return True
    else:
        return False


