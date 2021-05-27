from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class History(QWidget):
    def __init__(self, cnx=None):
        super().__init__()
        self.cursor = cnx.cursor(buffered=True)
        self.initUI()

    def initUI(self):
        label = QLabel('Transakcje: ', self)
        label.move(10, 10)

        history_select = ('select * from historia_transakcji')
        self.cursor.execute(history_select)

        history = QTableWidget(self)
        history.setColumnCount(7)
        history.setRowCount(self.cursor.rowcount)
        history.setHorizontalHeaderLabels(['Id transakcji', 'Id seansu', 'Bilety normalne',
                                           'Bilety ulgowe', 'Bilety studenckie', 'suma', 'Data transakcji'])
        for (i, (id_transakcji, id_seansu, liczba_norm, liczba_ulg, liczba_stud,
                 suma, data_transakcji)) in enumerate(self.cursor):
            history.setItem(i, 0, QTableWidgetItem(str(id_transakcji)))
            history.setItem(i, 1, QTableWidgetItem(str(id_seansu)))
            history.setItem(i, 2, QTableWidgetItem(str(liczba_norm)))
            history.setItem(i, 3, QTableWidgetItem(str(liczba_ulg)))
            history.setItem(i, 4, QTableWidgetItem(str(liczba_stud)))
            history.setItem(i, 5, QTableWidgetItem(str(suma)))
            history.setItem(i, 6, QTableWidgetItem(str(data_transakcji)))

        history.move(10, 35)
        history.resize(720, 150)

        history.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        history.resizeColumnsToContents()
        history.setSelectionBehavior(QAbstractItemView.SelectRows)
        history.setFont(QFont('Calibri', 9))

        back_btn = QPushButton('Wróć', self)
        back_btn.resize(80, 30)
        back_btn.move(500, 200)

        back_btn.clicked.connect(self.back_btn_click)

        self.setGeometry(300, 300, 740, 300)
        self.setWindowTitle('Historia Transakcji')
        self.show()

    def back_btn_click(self):
        self.close()
