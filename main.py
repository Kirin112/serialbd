#check

import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('test.ui', self)
        self.con = sqlite3.connect('serial.sqlite')
        self.pushButton.clicked.connect(self.add_serial)
        self.pushButton_3.clicked.connect(self.delete_serial)
        self.pushButton_4.clicked.connect(self.update_serial)

        self.show_serials()

        self.page_2 = self.stackedWidget.findChild(QWidget, 'page_2')
        self.layout_page_2 = QVBoxLayout(self.page_2)

        # Создаем QScrollArea и устанавливаем QVBoxLayout внутри него
        self.scroll_area = QScrollArea(self.page_2)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        # Устанавливаем QScrollArea вместо layout_page_2 на странице page_2
        self.layout_page_2.addWidget(self.scroll_area)

        # Добавляем чекбоксы на страницу page_2
        self.add_checkboxes_to_page()

    def add_checkboxes_to_page(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT id, name FROM serials")
            serials = cursor.fetchall()

            for serial_id, name in serials:
                label = QLabel(f"{name} (ID: {serial_id})")
                checkbox_planned = QCheckBox("Планирую посмотреть")
                checkbox_watched = QCheckBox("Просмотрено")
                checkbox_watching = QCheckBox("Смотрю")

                checkbox_planned.serial_id = serial_id
                checkbox_watched.serial_id = serial_id
                checkbox_watching.serial_id = serial_id

                checkbox_planned.stateChanged.connect(self.checkbox_changed)
                checkbox_watched.stateChanged.connect(self.checkbox_changed)
                checkbox_watching.stateChanged.connect(self.checkbox_changed)

                self.scroll_layout.addWidget(label)
                self.scroll_layout.addWidget(checkbox_planned)
                self.scroll_layout.addWidget(checkbox_watched)
                self.scroll_layout.addWidget(checkbox_watching)

        except sqlite3.Error as e:
            print("Произошла ошибка при получении данных из базы данных:", e)

        finally:
            cursor.close()

    def checkbox_changed(self, state):
        checkbox = self.sender()
        serial_id = checkbox.serial_id

        if checkbox.isChecked():
            if checkbox.text() == "Планирую посмотреть":
                self.planned.append(serial_id)
            elif checkbox.text() == "Просмотрено":
                self.watched.append(serial_id)
            elif checkbox.text() == "Смотрю":
                self.watching.append(serial_id)
        else:
            if checkbox.text() == "Планирую посмотреть":
                self.planned.remove(serial_id)
            elif checkbox.text() == "Просмотрено":
                self.watched.remove(serial_id)
            elif checkbox.text() == "Смотрю":
                self.watching.remove(serial_id)

        # Обновляем базу данных с новыми списками
        cursor = self.con.cursor()
        cursor.execute("UPDATE users SET planned=?, watched=?, watching=?", (
        ",".join(map(str, self.planned)), ",".join(map(str, self.watched)), ",".join(map(str, self.watching))))
        self.con.commit()
        cursor.close()

    def add_serial(self):
        try:
            cursor = self.con.cursor()
            result = cursor.execute("SELECT id FROM genres WHERE name = ?", (self.comboBox.currentText(),)).fetchall()
            cursor.execute("""INSERT INTO
                                        serials (name, genre, episodes, seasons, year, country, score)
                                        VALUES(?, ?, ?, ?, ?, ?, ?)""",
                        (name := self.lineEdit.text(), genre := result[0][0], episodes := self.spinBox.text(), seasons := self.spinBox_2.text(), year := self.lineEdit_5.text(), country := self.lineEdit_6.text(), score := self.horizontalSlider.value())).fetchall()
            self.con.commit()
            print("Данные успешно добавлены в базу данных!")
            QMessageBox.information(self, "Успех", "Данные успешно добавлены в базу данных!")
            self.show_serials()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при добавлении данных в базу данных: {e}")
        finally:
            cursor.close()

    def delete_serial(self):
        try:
            cursor = self.con.cursor()
            name = self.lineEdit_3.text()
            cursor.execute("DELETE FROM serials WHERE name = ?", (name,))
            self.con.commit()
            print(f"Запись с названием '{name}' успешно удалена из базы данных!")
            QMessageBox.information(self, "Успех", f"Запись с названием '{name}' успешно удалена из базы данных!")
            self.show_serials()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при удалении данных из базы данных: {e}")
        finally:
            cursor.close()

    def update_serial(self):
        try:
            cursor = self.con.cursor()
            new_genre = cursor.execute("SELECT id FROM genres WHERE name = ?", (self.comboBox.currentText(),)).fetchall()
            new_episodes = self.spinBox.value()
            new_seasons = self.spinBox_2.value()
            new_year = self.lineEdit_5.text()
            new_country = self.lineEdit_6.text()
            new_score = self.horizontalSlider.value()

            name = self.lineEdit.text()

            cursor.execute("""UPDATE serials
                              SET genre = ?, episodes = ?, seasons = ?, year = ?, country = ?, score = ?
                              WHERE name = ?""",
                           (new_genre[0][0], new_episodes, new_seasons, new_year, new_country, new_score, name))
            self.con.commit()

            print(f"Запись с названием '{name}' успешно обновлена в базе данных!")
            QMessageBox.information(self, "Успех", f"Запись с названием '{name}' успешно обновлена в базе данных!")
            self.show_serials()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при обновлении данных в базе данных: {e}")

        finally:
            cursor.close()

    def show_serials(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT name, genre, episodes, seasons, year, country, score FROM serials")
            serials = cursor.fetchall()

            self.tableWidget_2.setRowCount(len(serials))
            self.tableWidget_2.setColumnCount(7)

            self.tableWidget_2.setHorizontalHeaderLabels(["Название", "Жанр", "Эпизоды", "Сезоны", "Год", "Страна", "Рейтинг"])

            for row, serial in enumerate(serials):
                for col, data in enumerate(serial):
                    item = QTableWidgetItem(str(data))
                    self.tableWidget_2.setItem(row, col, item)

        except sqlite3.Error as e:
            print("Произошла ошибка при получении данных из базы данных:", e)

        finally:
            cursor.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())