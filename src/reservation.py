from PyQt5.QtWidgets import *
from add_reservation import AddReservation


class Reservations(QWidget):
    def __init__(self, cnx=None):
        super().__init__()
        self.cnx = cnx
        self.cursor = cnx.cursor(buffered=True)
        self.add = None
        self.reser = None
        self.initUI()

    def initUI(self):
        label = QLabel('Rezerwacje: ', self)
        label.move(10, 10)

        self.cursor.execute(('select * from rezerwacje'))

        self.reser = QTableWidget(self)
        self.reser.setColumnCount(7)
        self.reser.setRowCount(self.cursor.rowcount)
        self.reser.setHorizontalHeaderLabels(['Numer rezerwacji', 'Imię', 'Nazwisko', 'Numer seansu',
                                         'Bilety normalne', 'Bilety ulgowe', 'Bilety studenckie'])

        for (i, (id_rezerwacji, imie, nazwisko, id_seansu, norm, ulg,
                 stud)) in enumerate(self.cursor):
            self.reser.setItem(i, 0, QTableWidgetItem(str(id_rezerwacji)))
            self.reser.setItem(i, 1, QTableWidgetItem(imie))
            self.reser.setItem(i, 2, QTableWidgetItem(nazwisko))
            self.reser.setItem(i, 3, QTableWidgetItem(str(id_seansu)))
            self.reser.setItem(i, 4, QTableWidgetItem(str(norm)))
            self.reser.setItem(i, 5, QTableWidgetItem(str(ulg)))
            self.reser.setItem(i, 6, QTableWidgetItem(str(stud)))

        self.reser.resize(730, 300)
        self.reser.move(10, 40)

        self.reser.resizeColumnsToContents()
        self.reser.setSelectionBehavior(QAbstractItemView.SelectRows)

        add_btn = QPushButton('Dodaj rezerwację', self)
        add_btn.resize(130, 30)
        add_btn.move(770, 20)

        del_btn = QPushButton('Usuń rezerwację', self)
        del_btn.resize(130, 30)
        del_btn.move(770, 70)

        mod_btn = QPushButton('Modyfikuj rezerwację', self)
        mod_btn.resize(130, 30)
        mod_btn.move(770, 120)

        back_btn = QPushButton('Wróć', self)
        back_btn.resize(130, 30)
        back_btn.move(770, 170)

        reload_btn = QPushButton('Odśwież', self)
        reload_btn.resize(130, 30)
        reload_btn.move(770, 220)

        back_btn.clicked.connect(self.back_btn_click)
        add_btn.clicked.connect(self.add_btn_click)
        mod_btn.clicked.connect(self.mod_btn_click)
        del_btn.clicked.connect(self.del_btn_click)
        reload_btn.clicked.connect(self.reload_btn_click)

        self.setGeometry(300, 300, 920, 400)
        self.setWindowTitle('Rezerwacje')
        self.show()

    def back_btn_click(self):
        self.close()

    def add_btn_click(self):
        self.add = AddReservation(cnx=self.cnx)

    def mod_btn_click(self):
        obj = self.reser.selectedItems()
        self.add = AddReservation(obj=obj, cnx=self.cnx)

    def del_btn_click(self):
        (id_rezerwacji, _, _, _, _, _, _) = self.reser.selectedItems()
        order = ('delete from rezerwacje where id_rezerwacji = {}'.format(int(id_rezerwacji.text())))
        self.cursor.execute(order)
        self.cnx.commit()
        alert = QMessageBox()
        alert.setText('Pomyślnie usunięto rezerwację!')
        alert.exec_()

    def reload_btn_click(self):
        self.close()
        super().__init__()
        self.initUI()
