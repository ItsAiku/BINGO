import sys  # Vajalik QT jaoks
import random

# Kõik kasutatavad UI impordid.
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QPushButton, QWidget, QLabel, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import QTimer, Qt

class Bingo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bingo")  # Seadista akna pealkiri
        self.setGeometry(100, 100, 700, 800)  # Seadista akna suurus

        self.setStyleSheet("background-color: #333; color: #fff;")  # Kohandatud stiil paremaks väljanägemiseks

        self.KeskmineVidin = QWidget(self)
        self.setCentralWidget(self.KeskmineVidin)
        
        # Loo grid-paigutus
        self.Paigutus = QGridLayout()
        self.KeskmineVidin.setLayout(self.Paigutus)

        # Bingo nupud
        self.BingoNupud1 = {}
        self.BingoNupud2 = {}
        self.rows1 = {i: set() for i in range(1, 6)}
        self.rows2 = {i: set() for i in range(1, 6)}
        self.BingoLaud(self.BingoNupud1, self.rows1, 0)
        self.BingoLaud(self.BingoNupud2, self.rows2, 7)

        self.List = QListWidget()
        self.Paigutus.addWidget(self.List, 0, 10, 14, 5)
        self.List.setMinimumSize(100, 600)
        self.List.setStyleSheet("background-color: #2A2A2A; color: #fff;")
        
        # Silt numbrite kuulutamiseks
        self.TeadeSilt = QLabel("", self)
        self.TeadeSilt.setAlignment(Qt.AlignCenter)
        self.Paigutus.addWidget(self.TeadeSilt, 6, 0, 1, 5)

        # Võimalike numbrite loend
        self.VoimalikudNumbrid = list(range(1, 76))
        random.shuffle(self.VoimalikudNumbrid)
        
        self.VarasemadNumbrid = list()

        self.Nupp = QPushButton("Näita Numbrid", self)
        self.Nupp.clicked.connect(self.TeataNumber)
        self.Nupp.setEnabled(True)
        self.Paigutus.addWidget(self.Nupp, 13, 0, 1, 5)

        # Nupp võidutingimuste kontrollimiseks
        self.WinNupp = QPushButton("Kontrolli Võit", self)
        self.WinNupp.clicked.connect(self.KontrolliVoit)
        self.Paigutus.addWidget(self.WinNupp, 14, 0, 1, 5)

        # Nupp reeglite näitamiseks
        self.ReeglidNupp = QPushButton("Näita Reeglid", self)
        self.ReeglidNupp.clicked.connect(self.NaitaReeglid)
        self.Paigutus.addWidget(self.ReeglidNupp, 15, 0, 1, 5)

        # Demorežiimi muutujad ja silt
        self.demo_reziim = False
        self.demo_silt = QLabel("Demorežiim", self)
        self.demo_silt.setAlignment(Qt.AlignCenter)
        self.demo_silt.setStyleSheet("font-size: 15px; color: lightblue;")
        self.demo_silt.setVisible(False)
        self.Paigutus.addWidget(self.demo_silt, 12, 0, 1, 5)
            
    def BingoLaud(self, BingoNupud, rows, start_row):
        # Kõige tõhusam viis
        Vahemikud = {
            'B': (1, 15),
            'I': (16, 30),
            'N': (31, 45),
            'G': (46, 60),
            'O': (61, 75),
        }
                
        for Veerg, (Taht, (Algus, Lopp)) in enumerate(Vahemikud.items()):
            # Lisa veergude pealkirjad, nt B I N G O
            Pealkiri = QLabel(Taht, self)
            Pealkiri.setAlignment(Qt.AlignCenter)
            self.Paigutus.addWidget(Pealkiri, start_row, Veerg)
            for Rida in range(1, 6):
                Num = random.randint(Algus, Lopp)
                while Num in BingoNupud:
                    Num = random.randint(Algus, Lopp)
                Nupp = QPushButton(str(Num), self)
                Nupp.clicked.connect(self.NuppEvent)
                Nupp.setStyleSheet("background-color: #555; color: white;")
                
                BingoNupud[Num] = Nupp
                self.Paigutus.addWidget(Nupp, start_row + Rida, Veerg)
                
                # Jälgi positsioone võidutingimuste kontrollimiseks
                rows[Rida].add(Num)

    def NuppEvent(self):
        Nupp = self.sender()
        if Nupp.styleSheet() == "background-color: yellow; color: black;":
            Nupp.setStyleSheet("background-color: #555; color: white;")
        else:
            Nupp.setStyleSheet("background-color: yellow; color: black;")

    def TeataNumber(self):
        if self.VoimalikudNumbrid:
            Number = self.VoimalikudNumbrid.pop(0)
                    
            symbol = ""
            
            if Number <= 15:
                symbol = "B"
            elif Number <= 30:
                symbol = "I"
            elif Number <= 45:
                symbol = "N"
            elif Number <= 60:
                symbol = "G"
            elif Number <= 75:
                symbol = "O"
                
            self.VarasemadNumbrid.insert(0, f"{symbol} {Number}")
            QListWidgetItem(f"{symbol} {Number}", self.List)
            self.TeadeSilt.setText(f"Number: {symbol} {Number}")

            if self.demo_reziim:
                self.KontrolliNumber(Number)

    def KontrolliNumber(self, number):
        if number in self.BingoNupud1:
            self.BingoNupud1[number].click()
        if number in self.BingoNupud2:
            self.BingoNupud2[number].click()

    def KontrolliVoit(self):
        drawn_numbers = set(int(num.split()[1]) for num in self.VarasemadNumbrid)

        # Märgi kõik märkimata nupud ja eemalda valesti märgitud nupud
        for number, button in self.BingoNupud1.items():
            if number in drawn_numbers and button.styleSheet() != "background-color: yellow; color: black;":
                button.setStyleSheet("background-color: yellow; color: black;")
            elif number not in drawn_numbers and button.styleSheet() == "background-color: yellow; color: black;":
                button.setStyleSheet("background-color: red; color: white;")

        for number, button in self.BingoNupud2.items():
            if number in drawn_numbers and button.styleSheet() != "background-color: yellow; color: black;":
                button.setStyleSheet("background-color: yellow; color: black;")
            elif number not in drawn_numbers and button.styleSheet() == "background-color: yellow; color: black;":
                button.setStyleSheet("background-color: red; color: white;")

        win_conditions1 = 0
        win_conditions2 = 0

        for key in self.rows1:
            if self.rows1[key].issubset(drawn_numbers):
                win_conditions1 += 1

        for key in self.rows2:
            if self.rows2[key].issubset(drawn_numbers):
                win_conditions2 += 1

        if win_conditions1 > 0 or win_conditions2 > 0:
            self.show_winner(f"Ühel mängulaual on {max(win_conditions1, win_conditions2)} rida täidetud")

    def show_winner(self, win_type):
        QMessageBox.information(self, "Võit", f"Sa võitsid! ({win_type})")
        # Ära taaskäivita mängu, luba kasutajal edasi mängida

    def reset_game(self):
        self.VoimalikudNumbrid = list(range(1, 76))
        random.shuffle(self.VoimalikudNumbrid)
        self.VarasemadNumbrid.clear()
        self.List.clear()  # Tühjenda tõmmatud numbrite loend
        for num, btn in self.BingoNupud1.items():
            btn.setStyleSheet("background-color: #555; color: white;")
        for num, btn in self.BingoNupud2.items():
            btn.setStyleSheet("background-color: #555; color: white;")
        self.rows1 = {i: set() for i in range(1, 6)}
        self.rows2 = {i: set() for i in range(1, 6)}
        self.BingoLaud(self.BingoNupud1, self.rows1, 0)
        self.BingoLaud(self.BingoNupud2, self.rows2, 7)

    def NaitaReeglid(self):
        rules = (
            "Bingo Mängureeglid:\n"
            "1. Märgi oma kaardil kuulutatud numbrid.\n"
            "2. Võida, kui saad täis ühe või mitu järgmistest:\n"
            "   - Ühe rea\n"
            "3. Kui märgid numbreid valesti, saad uuesti vajutades need maha võtta.\n"
            "4. Mäng jätkub pärast esimest võitu."
        )
        QMessageBox.information(self, "Reeglid", rules)

    def Demo(self):
        self.demo_reziim = True
        self.demo_silt.setVisible(True)
        self.Nupp.setEnabled(False)
        self.Taimer = QTimer(self)
        self.Taimer.timeout.connect(self.TeataNumber)
        self.Taimer.start(100)

App = QApplication(sys.argv)
App.setStyle("Fusion")
Aken = Bingo()

Aken.show()
# Aken.Demo()  # demorežiim
sys.exit(App.exec_())
