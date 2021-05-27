from PyQt5.QtWidgets import *


class Shows(QWidget):
    def __init__(self, obj=None, cnx=None):
        super().__init__()
        self.cnx = cnx
        self.obj = obj
        self.cursor = cnx.cursor(buffered=True)
        self.initUI(obj)

    def initUI(self, obj):
        x = 1200
        size = (80, 20)
        date_label = QLabel('Termin: ', self)
        date_label.move(1100, 60)
        self.date = QLineEdit(self)
        self.date.setText('YYYY.MM.DD HH.MM.SS')
        self.date.resize(140, 20)
        self.date.move(x, 60)

        th = ['Tak', 'Nie']
        three_label = QLabel('3D', self)
        three_label.move(1100, 90)
        self.three = QComboBox(self)
        self.three.addItems(th)
        self.three.move(x, 90)

        v = ['Dubbing', 'Napisy']
        version_label = QLabel('Wersja: ', self)
        version_label.move(1100, 120)
        self.version = QComboBox(self)
        self.version.addItems(v)
        self.version.move(x, 120)

        sale = []
        self.cursor.execute(('select * from sale'))
        for id_sali, miejsca in self.cursor:
            sale.append('{} - {} miejsc'.format(id_sali, miejsca))

        room_label = QLabel('Sala: ', self)
        room_label.move(1100, 150)
        self.room = QComboBox(self)
        self.room.addItems(sale)
        self.room.move(x, 150)

        ok_btn = QPushButton('OK', self)
        ok_btn.resize(50, 30)
        ok_btn.move(1170, 200)

        back_btn = QPushButton('Wróć', self)
        back_btn.resize(50, 30)
        back_btn.move(1230, 200)

        self.cursor.execute(('select * from filmy'))

        self.movies = QTableWidget(self)
        self.movies.setRowCount(self.cursor.rowcount)
        self.movies.setColumnCount(9)
        self.movies.setHorizontalHeaderLabels(['Id filmu', 'Tytuł', 'Reżyser', 'Ocena',
                                               'Kategoria wiekowa', 'Kategoria filmu',
                                               'Czas trwania', 'Rok produkcji', 'Kraj produkcji'])
        tytuly = []
        for (i, (id_filmu, tytul, rezyser, ocena, kat_wiek, kat_film,
                 czas, rok, kraj)) in enumerate(self.cursor):
            self.movies.setItem(i, 0, QTableWidgetItem(str(id_filmu)))
            self.movies.setItem(i, 1, QTableWidgetItem(tytul))
            tytuly.append(tytul)
            self.movies.setItem(i, 2, QTableWidgetItem(rezyser))
            self.movies.setItem(i, 3, QTableWidgetItem(str(ocena)))
            self.movies.setItem(i, 4, QTableWidgetItem(kat_wiek))
            self.movies.setItem(i, 5, QTableWidgetItem(kat_film))
            self.movies.setItem(i, 6, QTableWidgetItem(str(czas)))
            self.movies.setItem(i, 7, QTableWidgetItem(str(rok)))
            self.movies.setItem(i, 8, QTableWidgetItem(kraj))

        self.movies.selectRow(0)
        self.movies.move(10, 40)
        self.movies.resize(1050, 330)
        self.movies.resizeColumnsToContents()
        self.movies.setSelectionBehavior(QAbstractItemView.SelectRows)

        ok_btn.clicked.connect(self.ok_btn_click)
        back_btn.clicked.connect(self.back_btn_click)

        if obj is not None:
            (self.id_seansu, tytul, czas, kat_film, kat_wiek, termin, self.wolne, trzy_d, wersja, self.poprzednia_sala) = obj
            self.date.setText(termin.text())
            self.three.setCurrentIndex(th.index(trzy_d.text()))
            self.version.setCurrentIndex(v.index(wersja.text()))
            self.room.setCurrentIndex(int(self.poprzednia_sala.text()) - 1)
            self.movies.selectRow(tytuly.index(tytul.text()))
            self.setWindowTitle('Modyfikuj seans')

        else:
            self.setWindowTitle('Dodaj seans')

        self.setGeometry(300, 300, 1350, 400)

        self.show()

    def ok_btn_click(self):
        movie = self.movies.selectedItems()
        termin = self.date.text()
        trzy_d = self.three.currentText()
        wersja = self.version.currentText()
        sala = self.room.currentText()
        sala = sala.split()
        id_sali = int(sala[0])
        wolne_miejsca = int(sala[2])

        if termin == '':
            self.show_alert('Termin seansu nie może być pusty')
        else:
            if self.obj is None:
                data = termin[:10].split('.')
                data = data[0] + '-' + data[1] + '-' + data[2]
                godzina = termin[11:].split('.')
                godzina = godzina[0] + ':' + godzina[1] + ':' + godzina[2]
            else:
                data = termin[:10]
                godzina = termin[11:]
            if not self.check_number(data) or not self.check_number(godzina):
                self.show_alert('Data i godzina nie może zawierać liter')
            else:
                (id_filmu, tytul, rezyser, ocena, kat_wiek, kat_film,
                 czas, rok, kraj) = movie
                if self.obj is None:
                    self.task = ("insert into seanse(id_filmu, termin, id_sali, 3D, wolne_miejsca, wersja)"
                                 " values({}, '{} {}', {}, '{}', {}, '{}')".format(int(id_filmu.text()), data, godzina, id_sali, trzy_d, wolne_miejsca, wersja))
                else:
                    self.cursor.execute(('select liczba_miejsc from sale where id_sali={}'.format(self.poprzednia_sala.text())))
                    (calkowita,) = self.cursor
                    roznica = calkowita[0] - int(self.wolne.text())
                    self.task = (
                        "update seanse set id_filmu={}, termin='{} {}', id_sali={}, 3D='{}', wolne_miejsca={}, wersja='{}' where id_seansu={}".format(
                            int(id_filmu.text()), data, godzina, id_sali, trzy_d, wolne_miejsca - roznica, wersja, self.id_seansu
                        ))
                self.cursor.execute(self.task)
                self.cnx.commit()
                self.show_alert('Pomyślnie wykonano operację')
                self.close()
                """ self.cursor.execute(('select * from repertuar'))
                for (tytul, czas, kat_film, kat_wiek, termin, wolne, trzy_d, wersja, numer_sali) in self.cursor:
                    if id_sali == numer_sali:
                        if termin[:10] == data:
                            h = 0
                            if czas > 60:
                                h = czas // 60
                                czas = czas % 60
                            g = termin[11:]
                            m = int(g[3:5])
                            g = int(g[:2])
                            m += czas
                            g += h
                            if int(godzina[:2]) <"""



    def back_btn_click(self):
        self.close()

    def check_number(self, number):
        for i in number:
            numb = ord(i)
            if i == '-' or i == ':':
                continue
            if numb < 48 or numb > 57:
                return False
        return True

    def show_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()