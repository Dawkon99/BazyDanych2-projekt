from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from repertuar import RepertuarWindow
from movies import AllMovies
from tickets import Tickets
from reservation import Reservations
from history import History
from price import Price_window
import datetime


class Window(QWidget):
    def __init__(self, cnx=None):
        super().__init__()
        self.cnx = cnx
        self.cursor = cnx.cursor()
        self.date_and_time = None
        self.top = None
        self.rep = None
        self.mov = None
        self.price = None
        self.tickets = None
        self.reser = None
        self.hist = None
        self.initUI()

    def initUI(self):
        btn_size = (130, 50)
        top_5_select = ('SELECT * from top_5')
        rep_btn = QPushButton('Repertuar', self)
        rep_btn.resize(*btn_size)
        rep_btn.move(500, 50)

        fil_btn = QPushButton('Wszystkie filmy', self)
        fil_btn.resize(*btn_size)
        fil_btn.move(500, 120)

        tick_btn = QPushButton('Zwróć bilet', self)
        tick_btn.resize(*btn_size)
        tick_btn.move(500, 190)

        reser_btn = QPushButton('Rezerwacje', self)
        reser_btn.resize(*btn_size)
        reser_btn.move(500, 300)

        hist_btn = QPushButton('Historia transakcji', self)
        hist_btn.resize(*btn_size)
        hist_btn.move(500, 370)

        rld_btn = QPushButton('Odśwież', self)
        rld_btn.resize(*btn_size)
        rld_btn.move(500, 440)

        price_btn = QPushButton('Zmień ceny', self)
        price_btn.resize(*btn_size)
        price_btn.move(500, 510)

        now = datetime.datetime.now()
        self.date_and_time = QLabel(str(now.date()) + ' ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second), self)

        self.date_and_time.move(30, 20)

        top_label = QLabel('Najwyżej oceniane filmy:', self)
        top_label.move(30, 300)

        top = QTableWidget(self)
        top.setRowCount(5)
        top.setColumnCount(4)

        self.cursor.execute(top_5_select)

        top.setHorizontalHeaderLabels(['Tytuł', 'Kraj produkcji', 'Rok produkcji', 'Ocena'])
        for (i, (title, country, year, rate)) in enumerate(self.cursor):
            top.setItem(i, 0, QTableWidgetItem(title))
            top.setItem(i, 1, QTableWidgetItem(country))
            top.setItem(i, 2, QTableWidgetItem(str(year)))
            top.setItem(i, 3, QTableWidgetItem(str(rate)))
        top.move(20, 325)
        top.resize(460, 220)
        top.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        top.resizeColumnsToContents()
        top.setSelectionBehavior(QAbstractItemView.SelectRows)
        top.setFont(QFont('Calibri', 9))

        rep_btn.clicked.connect(self.rep_btn_click)
        fil_btn.clicked.connect(self.fil_btn_click)
        tick_btn.clicked.connect(self.ticket_btn_click)
        reser_btn.clicked.connect(self.reser_btn_click)
        hist_btn.clicked.connect(self.hist_btn_click)
        rld_btn.clicked.connect(self.reload_btn_click)
        price_btn.clicked.connect(self.price_btn_click)

        self.setGeometry(300, 300, 650, 600)
        self.setWindowTitle('Kasa Biletowa')
        self.show()

    def price_btn_click(self):
        self.price = Price_window(cnx=self.cnx)

    def rep_btn_click(self):
        self.rep = RepertuarWindow(cnx=self.cnx)

    def fil_btn_click(self):
        self.mov = AllMovies(cnx=self.cnx)

    def ticket_btn_click(self):
        self.tickets = Tickets(cnx=self.cnx)

    def reser_btn_click(self):
        self.reser = Reservations(cnx=self.cnx)

    def hist_btn_click(self):
        self.hist = History(cnx=self.cnx)

    def reload_btn_click(self):
        self.close()
        super().__init__()
        self.initUI()
