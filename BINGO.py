import sys # Seda on vaja QT Jaoks, https://stackoverflow.com/questions/45508090/what-is-the-necessity-of-sys-exitapp-exec-in-pyqt
import random

# Kõik siin UI importid, mida me kasutame.
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QPushButton, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import QTimer, Qt

class Bingo(QMainWindow):
    def __init__(self):
        super().__init__()

        # Kõik QT dokumentatsiooni leiab siit kui millegi pärast on vaja midagi muuta - https://doc.qt.io/qt-5/

        self.setWindowTitle("Bingo") # Paneme akna tiitli
        self.setGeometry(100, 100, 350, 400) # Paneme akna suuruse min ja max

        self.setStyleSheet("background-color: #333; color: #fff;") # Ilus oleks teha enda stiili kui lihtsalt jätta selle tavaliseks.

        self.KeskmineVidin = QWidget(self)
        self.setCentralWidget(self.KeskmineVidin)
        
        # Loome ruudustiku paigutuse
        self.Paigutus = QGridLayout()
        self.KeskmineVidin.setLayout(self.Paigutus)

        # Bingo nupud
        self.BingoNupud = {}
        self.BingoLaud()

        # Silt numbrite teatamiseks
        self.TeadeSilt = QLabel("", self)
        self.TeadeSilt.setAlignment(Qt.AlignCenter)
        self.Paigutus.addWidget(self.TeadeSilt, 6, 0, 1, 5) # Rida: 6, Veerg: 0, ReaVahe: 1, VeergVahe: 5.

        # Võimalike numbrite nimekiri
        self.VoimalikudNumbrid = list(range(1, 76))
        random.shuffle(self.VoimalikudNumbrid)

        self.Nupp = QPushButton("Näita Numbrid", self)
        self.Nupp.clicked.connect(self.TeataNumber)
        self.Nupp.setEnabled(True)
        self.Paigutus.addWidget(self.Nupp, 8, 0, 1, 5)

        # Demorežiimi muutuja ja label
        # See on ainult klassi jaoks näitus kuna reaalsuses me jäämegi neid numbreid kohmetult genereerima.
        self.demo_reziim = False
        self.demo_silt = QLabel("Demorežiim", self)
        self.demo_silt.setAlignment(Qt.AlignCenter)
        self.demo_silt.setStyleSheet("font-size: 15px; color: lightblue;")
        self.demo_silt.setVisible(False)
        self.Paigutus.addWidget(self.demo_silt, 7, 0, 1, 5)

    def BingoLaud(self):

        # https://www.w3schools.com/python/ref_dictionary_items.asp
        # Kõige effektiivsem viis. 
        Vahemikud = {
            'B': (1, 15),
            'I': (16, 30),
            'N': (31, 45),
            'G': (46, 60),
            'O': (61, 75),
        }

        for Veerg, (Taht, (Algus, Lopp)) in enumerate(Vahemikud.items()):
            # Lisame veerunimekirja, ehk siis B I N G O
            Pealkiri = QLabel(Taht, self)
            Pealkiri.setAlignment(Qt.AlignCenter)
            self.Paigutus.addWidget(Pealkiri, 0, Veerg)
            for Rida in range(1, 6):
                Num = random.randint(Algus, Lopp)
                while Num in self.BingoNupud:
                    Num = random.randint(Algus, Lopp)
                Nupp = QPushButton(str(Num), self)
                Nupp.clicked.connect(self.NuppEvent)
                Nupp.setStyleSheet("background-color: #555; color: white;")
                self.BingoNupud[Num] = Nupp
                self.Paigutus.addWidget(Nupp, Rida, Veerg)

    def NuppEvent(self):
        Nupp = self.sender()
        Nupp.setStyleSheet("background-color: yellow; color: black;")
        self.KontrolliVoit()

    def TeataNumber(self):
        if self.VoimalikudNumbrid:
            Number = self.VoimalikudNumbrid.pop(0)
            self.TeadeSilt.setText(f"Number: {Number}")

            # Kuna kui sa ei kasuta demoreziimi, siis insta crash sellepärast 
            # et see ei eksisteeri ja ainult define-itakse demos ise :)
            if self.demo_reziim:
                self.KontrolliNumber(Number)
        else:

            # Kuna kui sa ei kasuta demoreziimi, siis insta crash sellepärast 
            # et see ei eksisteeri ja ainult define-itakse demos ise :)
            if self.demo_reziim:
                self.Taimer.stop()

            self.TeadeSilt.setText("Mäng läbi")

    def KontrolliNumber(self, number):
        if number in self.BingoNupud:
            self.BingoNupud[number].click()

    def KontrolliVoit(self):
        for Rida in range(1, 6):
            if all(self.Paigutus.itemAtPosition(Rida, Veerg).widget().styleSheet() == "background-color: yellow; color: black;" for Veerg in range(5)):
                QMessageBox.information(self, "Võit!", "Clapped BINGO, ez")

                # Kuna kui sa ei kasuta demoreziimi, siis insta crash sellepärast 
                # et see ei eksisteeri ja ainult define-itakse demos ise :)
                if self.demo_reziim:
                    self.Taimer.stop()

    def Demo(self):
        self.demo_reziim = True
        self.demo_silt.setVisible(True)
        self.Nupp.setEnabled(False) # Me ei taha et kasutaja häiriks seda demoreziimi, sest miks me tahaks :D
        self.Taimer = QTimer(self)
        self.Taimer.timeout.connect(self.TeataNumber)
        self.Taimer.start(500)

App = QApplication(sys.argv)
App.setStyle("Fusion") # Armastan seda QT theme-i, mashallah https://doc.qt.io/qt-6.5/qtquickcontrols-fusion.html
Aken = Bingo()

Aken.show()
# Aken.Demo() # demoreziim
sys.exit(App.exec_()) # https://stackoverflow.com/questions/45508090/what-is-the-necessity-of-sys-exitapp-exec-in-pyqt
