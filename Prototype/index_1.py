import sys
import logging
import sqlite3
import os  # Импортируем os для работы с файловой системой
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QListWidget, QMessageBox)

# Устанавливаем путь к директории
db_directory = 'Prototype'
db_path = os.path.join(db_directory, 'tasks.db')

# Проверка и создание директории, если она не существует
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Подключение к базе данных SQLite
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Создание таблицы, если её нет
c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
''')
conn.commit()


class Logger:
    def __init__(self, name):
        self.name = name

    def log(self, message):
        logging.info(f"[{self.name}] {message}")


class TaskManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.logger = Logger("TaskManagerApp")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Система управления задачами")
        self.layout = QVBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText('Введите задачу')

        self.add_button = QPushButton('Добавить задачу')
        self.add_button.clicked.connect(self.add_task)

        self.delete_button = QPushButton('Удалить задачу')
        self.delete_button.clicked.connect(self.delete_task)

        self.search_button = QPushButton('Поиск задач')
        self.search_button.clicked.connect(self.search_tasks)

        self.results_list = QListWidget()

        # Настройка стилей
        self.task_input.setStyleSheet("padding: 5px; font-size: 16px;")
        self.add_button.setStyleSheet("font-size: 16px; background-color: #4CAF50; color: white;")
        self.delete_button.setStyleSheet("font-size: 16px; background-color: #F44336; color: white;")
        self.search_button.setStyleSheet("font-size: 16px; background-color: #2196F3; color: white;")
        self.results_list.setStyleSheet("font-size: 16px;")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.search_button)

        self.layout.addWidget(self.task_input)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.results_list)

        self.setLayout(self.layout)

        # Обновляем список задач при запуске приложения
        self.refresh_task_list()

    def add_task(self):
        task_title = self.task_input.text().strip()
        if not task_title:
            QMessageBox.warning(self, 'Предупреждение', 'Введите задачу для добавления.')
            return

        # Выполняем вставку задачи в базу данных
        c.execute("INSERT INTO tasks (title) VALUES (?)", (task_title,))
        conn.commit()  # Сохраняем изменения в базе данных
        self.logger.log(f"Задача добавлена: {task_title}")

        self.task_input.clear()  # Очищаем поле ввода
        self.refresh_task_list()  # Обновляем список задач

    def delete_task(self):
        selected_item = self.results_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите задачу для удаления.')
            return

        task_title = selected_item.text()
        c.execute("DELETE FROM tasks WHERE title = ?", (task_title,))
        conn.commit()  # Сохраняем изменения в базе данных
        self.logger.log(f"Задача удалена: {task_title}")

        self.refresh_task_list()  # Обновляем список задач

    def search_tasks(self):
        task_title = self.task_input.text().strip()
        if not task_title:
            QMessageBox.warning(self, 'Предупреждение', 'Введите текст для поиска.')
            return

        c.execute("SELECT * FROM tasks WHERE title LIKE ?", ('%' + task_title + '%',))
        tasks = c.fetchall()
        self.display_results(tasks)

    def refresh_task_list(self):
        c.execute("SELECT * FROM tasks")
        tasks = c.fetchall()
        self.display_results(tasks)

    def display_results(self, tasks):
        self.results_list.clear()
        if not tasks:
            self.results_list.addItem("Задачи не найдены.")
            self.logger.log("Задачи не найдены.")
        else:
            for task in tasks:
                self.results_list.addItem(task[1])

    def closeEvent(self, event):
        conn.close()  # Закрываем соединение с базой данных при выходе
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    task_manager = TaskManagerApp()
    task_manager.resize(500, 300)
    task_manager.show()
    sys.exit(app.exec_())