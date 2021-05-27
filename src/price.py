from PyQt5.QtWidgets import *


class Price_window(QWidget):
    def __init__(self, cnx=None):
        super().__init__()
        self.cursor = cnx.cursor()
        self.cnx = cnx
        self.myInitUI()

    def myInitUI(self):
        norm_label = QLabel('Cena biletu normalnego', self)
        norm_label.move(10, 30)
        self.norm = QLineEdit(self)
        self.norm.resize(40, 20)
        self.norm.move(160, 30)
        self.cursor.execute(("select wartosc from ceny where typ='normalny'"))
        (cena,) = self.cursor
        self.norm.setText(str(cena[0]))

        ulg_label = QLabel('Cena biletu ulgowego', self)
        ulg_label.move(10, 70)
        self.ulg = QLineEdit(self)
        self.ulg.resize(40, 20)
        self.ulg.move(160, 70)

        self.cursor.execute(("select wartosc from ceny where typ='ulgowy'"))
        (cena,) = self.cursor
        self.ulg.setText(str(cena[0]))


        stud_label = QLabel('Cena biletu studenckiego', self)
        stud_label.move(10, 110)
        self.stud = QLineEdit(self)
        self.stud.resize(40, 20)
        self.stud.move(160, 110)

        self.cursor.execute(("select wartosc from ceny where typ='studencki'"))
        (cena,) = self.cursor
        self.stud.setText(str(cena[0]))

        ok_btn = QPushButton('Ok', self)
        ok_btn.resize(50, 30)
        ok_btn.move(10, 150)

        back_btn = QPushButton('Wróć', self)
        back_btn.resize(50, 30)
        back_btn.move(100, 150)

        ok_btn.clicked.connect(self.ok_btn_click)
        back_btn.clicked.connect(self.back_btn_click)

        self.setGeometry(300, 300, 250, 220)
        self.setWindowTitle('Zmiana cen')
        self.show()

    def ok_btn_click(self):
        norm =  self.norm.text()
        ulg = self.ulg.text()
        stud = self.stud.text()

        if norm=='' or ulg=='' or stud=='':
            self.show_alert('Wszystkie pola muszą być wypełnione')
        elif not self.check_number(norm) or not self.check_number(ulg) or not self.check_number(stud):
            self.show_alert('W cenach mogą występować jedynie cyfry')
        else:
            self.cursor.execute(("update ceny set wartosc={} where typ='normalny'".format(int(norm))))
            self.cnx.commit()
            self.cursor.execute(("update ceny set wartosc={} where typ='ulgowy'".format(int(ulg))))
            self.cnx.commit()
            self.cursor.execute(("update ceny set wartosc={} where typ='studemcki'".format(int(stud))))
            self.cnx.commit()
            self.show_alert('Pomyślnie zmmieniono ceny')
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

    def back_btn_click(self):
        self.close()