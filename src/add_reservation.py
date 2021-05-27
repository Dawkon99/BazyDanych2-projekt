from PyQt5.QtWidgets import *


class AddReservation(QWidget):
    def __init__(self, obj=None, cnx=None):
        super().__init__()
        self.cnx = cnx
        self.cursor = cnx.cursor(buffered=True)
        self.obj = obj
        self.initUI(obj)

    def initUI(self, obj):
        shows_label = QLabel('Seanse', self)
        shows_label.move(10, 10)

        self.cursor.execute(('select * from seanse'))

        self.shows = QTableWidget(self)
        self.shows.setColumnCount(7)
        self.shows.setRowCount(self.cursor.rowcount)
        movies_list = []
        self.shows.setHorizontalHeaderLabels(['Id seanu', 'Tytuł', 'Termin', 'Sala', '3D',
                                         'Wolne miejsca', 'Wersja'])

        for (i, (id_seansu, id_filmu, termin, wolne_miejsca, obraz, wersja, sala)) in enumerate(self.cursor):
            self.shows.setItem(i, 0, QTableWidgetItem(str(id_seansu)))
            movies_list.append(id_filmu)
            self.shows.setItem(i, 2, QTableWidgetItem(str(termin)))
            self.shows.setItem(i, 3, QTableWidgetItem(str(wolne_miejsca)))
            self.shows.setItem(i, 4, QTableWidgetItem(str(obraz)))
            self.shows.setItem(i, 5, QTableWidgetItem(str(wersja)))
            self.shows.setItem(i, 6, QTableWidgetItem(str(sala)))

        self.shows.move(10, 30)
        for i, id_f in enumerate(movies_list):
            self.cursor.execute(('select tytul from filmy where id_filmu = {}'.format(id_f)))
            (title,) = self.cursor
            self.shows.setItem(i, 1, QTableWidgetItem(str(title[0])))
        self.shows.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.shows.resizeColumnsToContents()
        self.shows.setSelectionBehavior(QAbstractItemView.SelectRows)

        first_name_label = QLabel('Imię: ', self)
        first_name_label.move(750, 30)
        self.first_name = QLineEdit(self)
        self.first_name.resize(100, 20)
        self.first_name.move(855, 30)

        last_name_label = QLabel('Nazwisko: ', self)
        last_name_label.move(750, 70)
        self.last_name = QLineEdit(self)
        self.last_name.resize(100, 20)
        self.last_name.move(855, 70)

        norm_label = QLabel('Bilety normalne: ', self)
        norm_label.move(750, 110)
        self.norm = QLineEdit(self)
        self.norm.resize(100, 20)
        self.norm.move(855, 110)

        ulg_label = QLabel('Bilety ulgowe: ', self)
        ulg_label.move(750, 150)
        self.ulg = QLineEdit(self)
        self.ulg.resize(100, 20)
        self.ulg.move(855, 150)

        std_label = QLabel('Bilety studenckie: ', self)
        std_label.move(750, 190)
        self.std = QLineEdit(self)
        self.std.resize(100, 20)
        self.std.move(855, 190)

        ok_btn = QPushButton('OK', self)
        ok_btn.resize(80, 30)
        ok_btn.move(750, 230)

        back_btn = QPushButton('Wróć', self)
        back_btn.resize(80, 30)
        back_btn.move(850, 230)

        back_btn.clicked.connect(self.back_btn_click)
        ok_btn.clicked.connect(self.ok_btn_click)

        self.shows.selectRow(0)
        self.norm.setText('0')
        self.std.setText('0')
        self.ulg.setText('0')

        if obj is not None:
            (id_r, imie, nazwisko, id_seansu, norm, ulg, stud) = obj
            a = int(id_seansu.text())
            self.first_name.setText(imie.text())
            self.last_name.setText(nazwisko.text())
            # Nazwa i godzina seansu na podstawie id seansu
            self.shows.selectRow(a - 1)
            self.norm.setText(norm.text())
            self.ulg.setText(ulg.text())
            self.std.setText(stud.text())
            self.setWindowTitle('Modyfikacja rezerwacji')
        else:
            self.setWindowTitle('Dodaj rezerwację')

        self.setGeometry(300, 300, 970, 500)
        self.show()

    def back_btn_click(self):
        self.close()

    def ok_btn_click(self):
        imie = self.first_name.text()
        nazwisko = self.last_name.text()

        (id_seansu, _, _, _, _, wolne, _) = self.shows.selectedItems()
        norm = self.norm.text()
        ulg = self.ulg.text()
        stud = self.std.text()

        if int(wolne.text()) == 0:
            self.show_alert('Brak wolnych miejsc na wybrany seans')
        elif not self.check_number(norm) or not self.check_number(ulg) or not self.check_number(stud):
            self.show_alert('Liczba biletów musi być liczbą!!')
        elif int(wolne.text()) - int(norm) - int(ulg) - int(stud) < 0:
            self.show_alert('Brak wystarczającej liczby miejsc na wybrany seans')
        elif not self.check_char(imie):
            self.show_alert('Imię może zawierać tylko litery')
        elif len(imie) == 0:
            self.show_alert('Nie podano imienia')
        elif not self.check_char(nazwisko):
            self.show_alert('Nazwisko może zawierać tylko litery')
        elif len(nazwisko) == 0:
            self.show_alert('Nie podano nazwiska')
        elif self.obj is not None:
            (id_r, _, _, _, _, _, _) = self.obj
            order = ("update rezerwacje set imie = '{}', nazwisko = '{}', id_seansu = {},"
                     "liczba_norm = {}, liczba_ulg = {}, liczba_stud = {}"
                     " where id_rezerwacji = {}".format(imie, nazwisko, int(id_seansu.text()),
                                                        int(norm), int(ulg), int(stud), int(id_r.text())))
            self.show_alert('Pomyślnie zmodyfikowano rezerwację!')
            self.cursor.execute(order)
            self.cnx.commit()
            self.close()
        else:
            order = ("insert into rezerwacje(imie, nazwisko, id_seansu, liczba_norm, liczba_ulg, liczba_stud)"
                     " values ('{}', '{}', {}, {}, {}, {})".format(imie, nazwisko, int(id_seansu.text()),
                                                                   int(norm), int(ulg), int(stud)))
            self.show_alert('Pomyślnie dodano rezerwację!')
            self.cursor.execute(order)
            self.cnx.commit()
            self.close()

    def check_char(self, text):
        for i in text:
            char = ord(i)
            if char < 65 or 90 < char < 97 or char > 122:
                return False
        return True

    def check_number(self, number):
        for i in number:
            numb = ord(i)
            if numb < 48 or numb > 57:
                return False
        return True

    def show_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.exec()
