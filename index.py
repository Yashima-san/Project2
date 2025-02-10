import sys
import logging
import sqlite3
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QListWidget, QComboBox, QMessageBox)

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Подключение к базе данных SQLite
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Создание таблицы, если ее нет
c.execute('''
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        city TEXT
    )
''')

conn.commit()

class Logger:
    def __init__(self, name):
        self.name = name
    def log(self, message):
        logging.info(f"[{self.name}] {message}")

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.logger = Logger("SearchApp")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Work DataBase")
        self.layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Введите имя')

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText('Введите возраст')

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText('Введите город')

        self.filter_button = QPushButton('Фильтровать')
        self.filter_button.clicked.connect(self.perform_filter)

        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Имя", "Возраст", "Город"])

        self.sort_button = QPushButton('Сортировать')
        self.sort_button.clicked.connect(self.perform_sort)

        self.results_list = QListWidget()

        # Set styles for widgets
        self.name_input.setStyleSheet("font-size: 18px; padding: 5px;")
        self.age_input.setStyleSheet("font-size: 18px; padding: 5px;")
        self.city_input.setStyleSheet("font-size: 18px; padding: 5px;")
        self.sort_combo.setStyleSheet("font-size: 18px; padding: 5px;")
        self.filter_button.setStyleSheet("font-size: 18px; background-color: #2196F3; color: white;")
        self.sort_button.setStyleSheet("font-size: 18px; background-color: #4CAF50; color: white;")
        self.results_list.setStyleSheet("font-size: 18px; background-color: white;")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.age_input)
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.filter_button)

        sort_layout = QHBoxLayout()
        sort_layout.addWidget(self.sort_combo)
        sort_layout.addWidget(self.sort_button)

        self.layout.addLayout(input_layout)
        self.layout.addLayout(sort_layout)
        self.layout.addWidget(self.results_list)

        self.setLayout(self.layout)

    def perform_filter(self):
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()
        city = self.city_input.text().strip()

        # Проверка на наличие хотя бы одного фильтра
        if not name and not age and not city:
            QMessageBox.warning(self, 'Предупреждение', 'Введите хотя бы один критерий для фильтрации')
            return

        # Создаем базовый запрос
        query = "SELECT * FROM records"
        filters = []
        parameters = []

        if name:
            filters.append("name LIKE ?")
            parameters.append(f"%{name}%")
        if age:
            filters.append("age = ?")
            parameters.append(int(age))
        if city:
            filters.append("city LIKE ?")
            parameters.append(f"%{city}%")

        # Объединяем условия, если они есть
        if filters:
            query += " WHERE " + " AND ".join(filters)

        self.logger.log(f"Выполняется запрос: {query} с параметрами: {parameters}")

        # Выполняем запрос с параметрами
        c.execute(query, parameters)
        filtered_results = c.fetchall()

        self.display_results(filtered_results)
    def perform_sort(self):
        sort_key = self.sort_combo.currentText()
        # Сортировка результатов
        if sort_key == "Имя":
            c.execute("SELECT * FROM records ORDER BY name")
        elif sort_key == "Возраст":
            c.execute("SELECT * FROM records ORDER BY age")
        elif sort_key == "Город":
            c.execute("SELECT * FROM records ORDER BY city")

        sorted_results = c.fetchall()

        self.display_results(sorted_results)

    def display_results(self, results):
        self.results_list.clear()
        if not results:
            self.logger.log("Записей не найдено.")
            self.results_list.addItem("Записей не найдено.")
        else:
            for record in results:
                result_text = f"{record[1]}, {record[2]}, {record[3]}"
                self.results_list.addItem(result_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SearchApp()
    ex.resize(700, 400)
    ex.show()
    sys.exit(app.exec_())