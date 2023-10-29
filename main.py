import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QStackedWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('test.ui', self)
        self.con = sqlite3.connect('serial.sqlite')
        self.pushButton.clicked.connect(self.add_serial)
        self.pushButton_3.clicked.connect(self.delete_serial)
        self.pushButton_4.clicked.connect(self.update_serial)

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

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при обновлении данных в базе данных: {e}")

        finally:
            cursor.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())