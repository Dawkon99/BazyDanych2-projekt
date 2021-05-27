import sys
from main_window import Window
from PyQt5.QtWidgets import QApplication
import mysql.connector


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    cnx = mysql.connector.connect(user='Dawid', password='makao',
                                  host='localhost', database='kasa biletowa - projekt')
    win = Window(cnx=cnx)
    sys.exit(app.exec_())
