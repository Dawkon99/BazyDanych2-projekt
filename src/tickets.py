from PyQt5.QtWidgets import *


class Tickets(QWidget):
    def __init__(self, cnx=None):
        super().__init__()
        self.cnx = cnx
        self.number = None
        self.cursor = cnx.cursor(buffered=True)
        self.initUI()

    def initUI(self):
        label = QLabel('Podaj numer transakcji: ', self)
        label.move(10, 20)

        self.number = QLineEdit(self)
        self.number.resize(50, 20)
        self.number.move(145, 18)

        ok_btn = QPushButton('OK', self)
        ok_btn.resize(50, 30)
        ok_btn.move(10, 60)

        back_btn = QPushButton('Wróć', self)
        back_btn.resize(50, 30)
        back_btn.move(110, 60)

        back_btn.clicked.connect(self.back_btn_click)
        ok_btn.clicked.connect(self.ok_btn_click)

        self.setGeometry(300, 300, 200, 100)
        self.setWindowTitle('Zwrot biletu')
        self.show()

    def back_btn_click(self):
        self.close()

    def ok_btn_click(self):
        try:
            value = int(self.number.text())
            ticket = ('Select * from historia_transakcji')
            self.cursor.execute(ticket)
            if self.cursor.rowcount == 0:
                alert = QMessageBox()
                alert.setText('Brak wierszy do wyświetlenia!')
                alert.exec_()
            for (i, (id, _, _, _, _, _, _)) in enumerate(self.cursor):
                if value == id:
                    self.cursor.execute('select suma from historia_transakcji where id_transakcji = {}'.format(value))
                    (suma,) = self.cursor
                    self.cursor.execute(('delete from historia_transakcji where id_transakcji = {}'.format(value)))
                    alert = QMessageBox()
                    alert.setText('Pomyślnie zwrócono bilet! Zwrócona kwota wynosi {} zł'.format(suma[0]))
                    alert.exec_()
                    self.cnx.commit()
                    break

                if i + 1 == self.cursor.rowcount:
                    alert = QMessageBox()
                    alert.setText('Błędny numer transakcji!')
                    alert.exec_()

        except:
            alert = QMessageBox()
            alert.setText('Niepoprawne dane! Numer biletu powinien być liczbą!')
            alert.exec_()


