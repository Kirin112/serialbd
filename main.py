import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QStackedWidget, QPushButton, QLineEdit
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('test.ui', self)
        self.con = sqlite3.connect('serial.sqlite')
        self.pushButton.clicked.connect(self.update_result)
        # self.lineEdit = QLineEdit(self)
        # self.lineEdit_5 = QLineEdit(self)
        # self.lineEdit_6 = QLineEdit(self)

    def update_result(self):
        # name = self.lineEdit.text()
        # year = self.lineEdit5.text()
        # country = self.lineEdit6.text()


        try:
            cursor = self.con.cursor()
            result = cursor.execute("SELECT id FROM genres WHERE name = ?", (self.comboBox.currentText(),)).fetchall()
            print(result)
            cursor.execute("""INSERT INTO
                                        serials (name, genre, episodes, seasons, year, country, score)
                                        VALUES(?, ?, ?, ?, ?, ?, ?)""",
                        (name := self.lineEdit.text(), genre := result[0][0], episodes := self.spinBox.text(), seasons := self.spinBox_2.text(), year := self.lineEdit_5.text(), country := self.lineEdit_6.text(), score := self.horizontalSlider.value())).fetchall()
            self.con.commit()
            print("Данные успешно добавлены в базу данных!")
        except sqlite3.Error as e:
            print("Произошла ошибка при добавлении данных в базу данных:", e)
        finally:
            cursor.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())