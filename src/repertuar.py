from PyQt5.QtWidgets import *
from buy import BuyWindow
from show import Shows


class RepertuarWindow(QWidget):
    def __init__(self, cnx=None):
        super().__init__()
        self.buy = None
        self.add = None
        self.cursor = cnx.cursor(buffered=True)
        self.cnx = cnx
        self.initUI()

    def initUI(self):
        btn_size = (130, 30)

        buy_btn = QPushButton('Kup bilet', self)
        buy_btn.resize(*btn_size)
        buy_btn.move(1040, 30)

        add_btn = QPushButton('Dodaj seans', self)
        add_btn.resize(*btn_size)
        add_btn.move(1040, 100)

        reload_btn = QPushButton('Odśwież', self)
        reload_btn.resize(*btn_size)
        reload_btn.move(1040, 170)

        mod_btn = QPushButton('Zmodyfikuj seans', self)
        mod_btn.resize(*btn_size)
        mod_btn.move(1040, 240)

        back_btn = QPushButton('Wróć', self)
        back_btn.resize(80, 40)
        back_btn.move(1040, 310)

        label = QLabel('Repertuar', self)
        label.move(20, 20)

        self.cursor.execute(('select * from repertuar'))

        self.shows = QTableWidget(self)
        self.shows.setColumnCount(9)
        self.shows.setRowCount(self.cursor.rowcount)
        self.shows.setHorizontalHeaderLabels(['Tytuł', 'Czas trwania', 'Kategoria filmowa',
                                              'Kat wiekowa', 'Termin', 'Wolne miejsca', '3D',
                                              'Wersja', 'Sala'])

        for (i, (tytul, czas, kat_film, kat_wiek, termin, wolne, trzy_d, wersja, numer_sali)) in enumerate(self.cursor):
            self.shows.setItem(i, 0, QTableWidgetItem(tytul))
            self.shows.setItem(i, 1, QTableWidgetItem(str(czas)))
            self.shows.setItem(i, 2, QTableWidgetItem(kat_film))
            self.shows.setItem(i, 3, QTableWidgetItem(kat_wiek))
            self.shows.setItem(i, 4, QTableWidgetItem(str(termin)))
            self.shows.setItem(i, 5, QTableWidgetItem(str(wolne)))
            self.shows.setItem(i, 6, QTableWidgetItem(trzy_d))
            self.shows.setItem(i, 7, QTableWidgetItem(wersja))
            self.shows.setItem(i, 8, QTableWidgetItem(str(numer_sali)))

        self.shows.move(10, 10)
        self.shows.resize(970, 350)

        self.shows.resizeColumnsToContents()
        self.shows.setSelectionBehavior(QAbstractItemView.SelectRows)

        buy_btn.clicked.connect(self.buy_button_click)
        back_btn.clicked.connect(self.back_button_click)
        add_btn.clicked.connect(self.add_button_click)
        mod_btn.clicked.connect(self.mod_button_click)
        reload_btn.clicked.connect(self.reload_btn_click)

        self.setGeometry(400, 400, 1200, 400)
        self.setWindowTitle('Repertuar')
        self.show()

    def buy_button_click(self):
        obj = self.shows.selectedItems()
        if len(obj) != 0:
            self.cursor.execute(("select id_seansu from seanse where id_sali={} and termin='{}'".format(int(obj[8].text()), obj[4].text())))
            (id_seansu,) = self.cursor
            objt = (id_seansu[0], *obj)
            self.buy = BuyWindow(cnx=self.cnx, obj=objt)
        else:
            alert = QMessageBox()
            alert.setText('Nie wybrano żadnego seansu')
            alert.exec_()

    def back_button_click(self):
        self.close()

    def add_button_click(self):
        self.add = Shows(cnx=self.cnx)

    def mod_button_click(self):
        obj = self.shows.selectedItems()
        self.cursor.execute(("select id_seansu from seanse where id_sali={} and termin='{}'".format(int(obj[8].text()), obj[4].text())))
        (id_seansu,) = self.cursor
        objt = (id_seansu[0], *obj)
        self.add = Shows(cnx=self.cnx, obj=objt)

    def reload_btn_click(self):
        self.close()
        super().__init__()
        self.initUI()


