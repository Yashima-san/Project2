import sys
import logging
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QListWidget, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Database:
    def __init__(self):
        self.data = [
            {"id": 1, "name": "Иван", "age": 25, "city": "Москва"},
            {"id": 2, "name": "Мария", "age": 30, "city": "Санкт-Петербург"},
            {"id": 3, "name": "Петр", "age": 22, "city": "Казань"},
            {"id": 4, "name": "Анна", "age": 28, "city": "Екатеринбург"},
            {"id": 5, "name": "Ирина", "age": 35, "city": "Москва"},
        ]

    def search(self, name=None, age=None, city=None):
        results = self.data
        if name:
            results = [record for record in results if name.lower() in record["name"].lower()]
        if age is not None:
            results = [record for record in results if record["age"] == age]
        if city:
            results = [record for record in results if city.lower() in record["city"].lower()]

        return results

    def sort_results(self, results, sort_key):
        if not results:
            logging.warning("Попытка сортировать пустой список результатов.")
            return []
        key_mapping = {
            "Имя": "name",
            "Возраст": "age",
            "Город": "city"
        }
        sort_key_mapping = key_mapping.get(sort_key)
        if sort_key_mapping is None:
            logging.error(f"Несуществующий ключ сортировки: {sort_key}")
            return results
        return sorted(results, key=lambda x: x[sort_key_mapping])


class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Сортировка, фильтрация и поиск данных")

        layout = QVBoxLayout()

        # Set font
        font = QFont("Helvetica", 16)
        self.setFont(font)

        # Set background color
        self.setStyleSheet("background-color: #f0f0f0;")

        # Input fields
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Введите имя')

        self.age_input = QLineEdit(self)
        self.age_input.setPlaceholderText('Введите возраст')

        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText('Введите город')

        # Buttons
        self.filter_button = QPushButton('Фильтровать', self)
        self.filter_button.clicked.connect(self.perform_filter)

        self.sort_button = QPushButton('Сортировать', self)
        self.sort_button.clicked.connect(self.perform_sort)

        self.search_button = QPushButton('Поиск', self)
        self.search_button.clicked.connect(self.perform_search)

        # ComboBox for sorting
        self.sort_combo = QComboBox(self)
        self.sort_combo.addItems(["Имя", "Возраст", "Город"])

        self.results_list = QListWidget(self)

        # Set styles for widgets
        self.name_input.setStyleSheet("font-size: 16px; padding: 5px;")
        self.age_input.setStyleSheet("font-size: 16px; padding: 5px;")
        self.city_input.setStyleSheet("font-size: 16px; padding: 5px;")
        self.sort_combo.setStyleSheet("font-size: 16px; padding: 5px;")
        self.filter_button.setStyleSheet("font-size: 16px; background-color: #2196F3; color: white;")
        self.search_button.setStyleSheet("font-size: 16px; background-color: #FF9800; color: white;")
        self.sort_button.setStyleSheet("font-size: 16px; background-color: #4CAF50; color: white;")
        self.results_list.setStyleSheet("font-size: 16px; background-color: white;")

        layout.addWidget(self.name_input)
        layout.addWidget(self.age_input)
        layout.addWidget(self.city_input)
        layout.addWidget(self.filter_button)
        layout.addWidget(self.search_button)  # Add search button
        layout.addWidget(self.sort_button)
        layout.addWidget(self.sort_combo)
        layout.addWidget(self.results_list)

        self.setLayout(layout)

        self.filtered_results = []  # хранит результаты фильтрации

    def perform_filter(self):
        name = self.name_input.text().strip() or None
        age_input = self.age_input.text().strip()
        city = self.city_input.text().strip() or None

        age = int(age_input) if age_input.isdigit() else None

        # Выполнение фильтрации
        self.filtered_results = self.db.search(name=name, age=age, city=city)
        logging.info(f"Результаты фильтрации: {self.filtered_results}")

        # Обновление результата
        self.update_results_list()

        # Очистка вводимых данных после фильтрации
        self.name_input.clear()
        self.age_input.clear()
        self.city_input.clear()

    def perform_search(self):
        # Используем perform_filter для поиска
        self.perform_filter()

    def perform_sort(self):
        sort_key = self.sort_combo.currentText()
        sorted_results = self.db.sort_results(self.filtered_results, sort_key)
        logging.info(f"Результаты сортировки по ключу '{sort_key}': {sorted_results}")

        # Обновление результата
        self.update_results_list(sorted_results)

    def update_results_list(self, results=None):
        # Очистка предыдущих результатов
        self.results_list.clear()

        if results is None:
            results = self.filtered_results

        if results:
            for record in results:
                result_text = f"{record['name']}, {record['age']}, {record['city']}"
                self.results_list.addItem(result_text)
        else:
            self.results_list.addItem("Записи не найдены.")
            logging.info("Записи не найдены.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SearchApp()
    ex.resize(700, 400)
    ex.show()
    sys.exit(app.exec_())