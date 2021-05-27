from PyQt5.QtWidgets import *


class AddMovieWindow(QWidget):
    def __init__(self, obj=None, cnx=None):
        super().__init__()
        self.cnx = cnx
        self.cursor = cnx.cursor()
        self.order = ''
        self.initUI(obj)

    def initUI(self, obj):
        cat = ['brak', '7', '12', '16', '18']
        title_label = QLabel('Tytuł: ', self)
        title_label.move(10, 10)
        self.title = QLineEdit(self)
        self.title.resize(80, 20)
        self.title.move(150, 10)

        director_label = QLabel('Reżyser: ', self)
        director_label.move(10, 40)
        self.director = QLineEdit(self)
        self.director.resize(80, 20)
        self.director.move(150, 40)

        rating_label = QLabel('Ocena: ', self)
        rating_label.move(10, 70)
        self.rating = QLineEdit(self)
        self.rating.resize(80, 20)
        self.rating.move(150, 70)

        category_label = QLabel('Kategoria wiekowa: ', self)
        category_label.move(10, 100)
        self.category = QComboBox(self)
        self.category.addItems(cat)
        self.category.move(150, 100)

        movie_category_label = QLabel('Kategoria filmowa', self)
        movie_category_label.move(10, 130)
        self.movie_category = QLineEdit(self)
        self.movie_category.resize(80, 20)
        self.movie_category.move(150, 130)

        duration_label = QLabel('Czas trwania', self)
        duration_label.move(10, 160)
        self.duration = QLineEdit(self)
        self.duration.resize(80, 20)
        self.duration.move(150, 160)

        year_label = QLabel('Rok produkcji', self)
        year_label.move(10, 190)
        self.year = QLineEdit(self)
        self.year.resize(80, 20)
        self.year.move(150, 190)

        country_label = QLabel('Kraj produkcji', self)
        country_label.move(10, 220)
        self.country = QLineEdit(self)
        self.country.resize(80, 20)
        self.country.move(150, 220)

        ok_btn = QPushButton('OK', self)
        ok_btn.resize(60, 30)
        ok_btn.move(10, 270)

        back_btn = QPushButton('Wróć', self)
        back_btn.resize(60, 30)
        back_btn.move(150, 270)

        ok_btn.clicked.connect(self.ok_btn_click)
        back_btn.clicked.connect(self.back_btn_click)

        if obj is not None:
            (id_filmu, tytul, rezyser, ocena, kat_wiek, kat_film, czas, rok, kraj) = obj
            self.title.setText(tytul.text())
            self.director.setText(rezyser.text())
            self.rating.setText(ocena.text())
            self.category.setCurrentIndex(cat.index(kat_wiek.text()))
            self.movie_category.setText(kat_film.text())
            self.duration.setText(czas.text())
            self.year.setText(rok.text())
            self.country.setText(kraj.text())
            self.setWindowTitle('Modyfikacja filmu')
            self.order = "Update filmy set tytul='{}', rezyser='{}', ocena={}, kategoria_wiekowa='{}'," \
                         "kategoria_filmowa='{}', czas_trwania={}, rok_produkcji={}, kraj_produkcji='{}'" \
                         "where id_filmu=" + id_filmu.text()
        else:
            self.setWindowTitle('Dodanie filmu')
            self.rating.setText('0')
            self.category.setCurrentIndex(0)
            self.duration.setText('0')
            self.year.setText('0')
            self.order = "insert into filmy(tytul, rezyser, ocena, kategoria_wiekowa, kategoria_filmowa, " \
                         "czas_trwania, rok_produkcji, kraj_produkcji) values ('{}', '{}', {}, '{}', '{}', {}, {}, '{}')"

        self.setGeometry(300, 300, 250, 320)
        self.show()

    def back_btn_click(self):
        self.close()

    def ok_btn_click(self):
        tytul = self.title.text()
        rezyser = self.director.text()
        ocena = self.rating.text()
        kat_wiek = self.category.currentText()
        kat_film = self.movie_category.text()
        czas = self.duration.text()
        rok = self.year.text()
        kraj = self.country.text()

        if tytul == '' or rezyser=='' or ocena=='' or kat_wiek=='' or kat_film=='' or czas=='' or rok=='' or kraj=='':
            self.show_alert('Wszystkie pola muszą być wypełnione')
        elif not self.check_char(rezyser):
            self.show_alert('W polu reżyser nie mogą być liczby')
        elif not self.check_number(ocena, float=True):
            self.show_alert('Ocena musi być liczbą')
        elif ',' in ocena:
            self.show_alert("Ocena powinna mieć .(kropkę) jako rozdzielenie części całkowitych i dziesiętnych")
        elif float(ocena) < 0 or float(ocena) > 10:
            self.show_alert('Ocena musi być liczbą z zakresu 0 - 10')
        elif not self.check_number(rok):
            self.show_alert('rok musi być liczbą całkowitą z zakresu 1900-9999')
        elif int(rok) > 9999 or int(rok) < 1900:
            self.show_alert('Rok musi być liczbą z zakresu 1900-9999')
        elif not self.check_number(czas):
            self.show_alert('Czas trwania musi być liczbą całkowitą z zakresu 1-999')
        elif int(czas) > 999 or int(czas) < 1:
            self.show_alert('Czas trwania musi być liczbą całkowitą z zakresu 1-999')
        elif not self.check_char(kraj):
            self.show_alert('Kraj produkcji nie może zawierać cyfr')
        elif not self.check_char(kat_film):
            self.show_alert('Kategoria filmowa nie może zawierać cyfr')
        else:
            self.cursor.execute(self.order.format(tytul, rezyser, float(ocena), kat_wiek, kat_film, int(czas), int(rok), kraj))
            self.cnx.commit()
            self.show_alert('Pomyślnie wykonano akcję na filmie')
            self.close()

    def check_char(self, text):
        for i in text:
            char = ord(i)
            if i == ' ':
                continue
            if char < 65 or 90 < char < 97 or char > 122:
                return False
        return True

    def check_number(self, number, float=False):
        for i in number:
            numb = ord(i)
            if float:
                if i == ',' or i == '.':
                    continue
            if numb < 48 or numb > 57:
                return False
            if not float:
                if i == '.' or i == ',':
                    return False
        return True

    def show_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.exec()
