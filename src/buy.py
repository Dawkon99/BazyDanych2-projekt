from PyQt5.QtWidgets import *
import datetime


class BuyWindow(QWidget):
    def __init__(self, cnx=None, obj=None):
        super().__init__()
        self.cnx = cnx
        self.obj = obj
        self.cursor = cnx.cursor()
        self.initUI()

    def initUI(self):
        (id_seansu, tytul, czas, kat_film, kat_wiek, termin, wolne, trzy_d, wersja, numer_sali) = self.obj
        label = QLabel('Seans: {} - {}'.format(tytul.text(), termin.text()), self)
        label.move(10, 5)

        price = ("select wartosc from ceny where typ='{}'")
        self.cursor.execute(price.format('normalny'))
        (self.norm_ticket, ) = self.cursor
        self.cursor.execute(price.format('ulgowy'))
        (self.ulg_ticket, ) = self.cursor
        self.cursor.execute(price.format('studencki'))
        (self.stud_ticket, ) = self.cursor

        self.norm = QLineEdit(self)
        self.norm.resize(80, 20)
        self.norm.move(170, 30)
        self.norm.setText('0')
        norm_label = QLabel('Bilety normalne ({} zł): '.format(self.norm_ticket[0]), self)
        norm_label.move(10, 30)

        self.ulg = QLineEdit(self)
        self.ulg.resize(80, 20)
        self.ulg.move(170, 90)
        self.ulg.setText('0')
        ulg_label = QLabel('Bilety ulgowe ({} zł): '.format(self.ulg_ticket[0]), self)
        ulg_label.move(10, 90)

        self.std = QLineEdit(self)
        self.std.resize(80, 20)
        self.std.move(170, 160)
        self.std.setText('0')
        std_label = QLabel('Bilety studenckie ({} zł): '.format(self.stud_ticket[0]), self)
        std_label.move(10, 160)

        buy_btn = QPushButton('Kup', self)
        buy_btn.resize(80, 30)
        buy_btn.move(20, 250)

        back_btn = QPushButton('Wróć', self)
        back_btn.resize(80, 30)
        back_btn.move(120, 250)

        back_btn.clicked.connect(self.back_button_click)
        buy_btn.clicked.connect(self.buy_button_click)

        self.setGeometry(400, 400, 350, 300)
        self.setWindowTitle('Kupno biletu')
        self.show()

    def back_button_click(self):
        self.close()

    def buy_button_click(self):
        (id_seansu, tytul, _, _, _, _, wolne, _, _, _) = self.obj
        norm = self.norm.text()
        ulg = self.ulg.text()
        stud = self.std.text()
        if not self.check_number(norm) or not self.check_number(ulg) or not self.check_number(stud):
            self.show_alert('Liczba biletów musi być liczbą dodatnią')
        elif int(wolne.text()) < int(norm) + int(ulg) + int(stud):
            self.show_alert('Brak wystarczającej liczby miejsc na seans')
        elif int(norm) < 0 or int(ulg) < 0 or int(stud) < 0:
            self.show_alert('Liczba biletów musi być liczbą dodatnią')
        else:
            date = datetime.datetime.now()
            hour, minute, second = date.hour, date.minute, date.second
            if len(str(hour)) == 1:
                hour = int('0' + str(hour))
            if len(str(minute)) == 1:
                minute = int('0' + str(minute))
            if len(str(second)) == 1:
                second = int('0' + str(second))
            suma = int(norm) * self.norm_ticket[0] + int(ulg) * self.ulg_ticket[0] + int(stud) * self.stud_ticket[0]
            task = ("insert into historia_transakcji(id_seansu, liczba_norm,"
                                 " liczba_ulg, liczba_stud, suma, data_transakcji)"
                                 " values({},{},{},{},{},'{}-{}-{} {}:{}:{}')".format(int(id_seansu), int(norm),
            int(ulg), int(stud), suma, date.year, date.month, date.day, hour, minute, second))
            self.cursor.execute(task)
            self.cnx.commit()
            self.show_alert('Zakupiono bilet na sumę {}zł'.format(suma))
            self.close()

    def show_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()

    def check_number(self, number):
        for i in number:
            numb = ord(i)
            if numb < 48 or numb > 57:
                return False
        return True
