from PyQt5.QtWidgets import *
from add_movie_window import AddMovieWindow


class AllMovies(QWidget):
    def __init__(self, cnx=None):
        super().__init__()
        self.add = None
        self.cursor = cnx.cursor(buffered=True)
        self.cnx = cnx
        self.movies = None
        self.initUI()

    def initUI(self):
        movs = QLabel('Filmy: ', self)
        movs.move(10, 10)

        add_btn = QPushButton('Dodaj film', self)
        add_btn.resize(100, 30)
        add_btn.move(1080, 30)

        del_btn = QPushButton('Usuń film', self)
        del_btn.resize(100, 30)
        del_btn.move(1080, 80)

        mod_btn = QPushButton('Zmodyfikuj film', self)
        mod_btn.resize(100, 30)
        mod_btn.move(1080, 130)

        back_btn = QPushButton('Wróć', self)
        back_btn.resize(100, 30)
        back_btn.move(1080, 180)

        reload_btn = QPushButton('Odśwież', self)
        reload_btn.resize(100, 30)
        reload_btn.move(1080, 230)

        self.cursor.execute(('select * from filmy'))

        self.movies = QTableWidget(self)
        self.movies.setRowCount(self.cursor.rowcount)
        self.movies.setColumnCount(9)
        self.movies.setHorizontalHeaderLabels(['Id filmu', 'Tytuł', 'Reżyser', 'Ocena',
                                               'Kategoria wiekowa', 'Kategoria filmu',
                                               'Czas trwania', 'Rok produkcji', 'Kraj produkcji'])

        for (i, (id_filmu, tytul, rezyser, ocena, kat_wiek, kat_film,
                 czas, rok, kraj)) in enumerate(self.cursor):
            self.movies.setItem(i, 0, QTableWidgetItem(str(id_filmu)))
            self.movies.setItem(i, 1, QTableWidgetItem(tytul))
            self.movies.setItem(i, 2, QTableWidgetItem(rezyser))
            self.movies.setItem(i, 3, QTableWidgetItem(str(ocena)))
            self.movies.setItem(i, 4, QTableWidgetItem(kat_wiek))
            self.movies.setItem(i, 5, QTableWidgetItem(kat_film))
            self.movies.setItem(i, 6, QTableWidgetItem(str(czas)))
            self.movies.setItem(i, 7, QTableWidgetItem(str(rok)))
            self.movies.setItem(i, 8, QTableWidgetItem(kraj))

        self.movies.move(10, 40)
        self.movies.resize(1063, 330)
        self.movies.resizeColumnsToContents()
        self.movies.setSelectionBehavior(QAbstractItemView.SelectRows)

        back_btn.clicked.connect(self.back_btn_click)
        add_btn.clicked.connect(self.add_btn_click)
        mod_btn.clicked.connect(self.mod_btn_click)
        del_btn.clicked.connect(self.del_btn_click)
        reload_btn.clicked.connect(self.reload_btn_click)

        self.setWindowTitle('Filmy')
        self.setGeometry(300, 300, 1200, 400)
        self.show()

    def back_btn_click(self):
        self.close()

    def add_btn_click(self):
        self.add = AddMovieWindow(cnx=self.cnx)

    def mod_btn_click(self):
        obj = self.movies.selectedItems()
        if len(obj) == 0:
            alert = QMessageBox()
            alert.setText("Do modyfikownia musi być wybrany jakiś film")
            alert.exec_()
        else:
            self.add = AddMovieWindow(cnx=self.cnx, obj=obj)

    def del_btn_click(self):
        if len(self.movies.selectedItems()) == 0:
            alert = QMessageBox()
            alert.setText("Do usunięcia musi być wybrany jakiś film")
            alert.exec_()
        else:
            (id_filmu, _, _, _, _, _, _, _, _) = self.movies.selectedItems()
            self.cursor.execute('delete from seanse where id_filmu = {}'.format(int(id_filmu.text())))
            self.cnx.commit()
            order = ("delete from filmy where id_filmu = {}".format(int(id_filmu.text())))
            self.cursor.execute(order)
            self.cnx.commit()
            alert = QMessageBox()
            alert.setText('Pomyślnie usunięto film!')
            alert.exec_()

    def reload_btn_click(self):
        self.close()
        super().__init__()
        self.initUI()
