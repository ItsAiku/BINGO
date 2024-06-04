import sys  # Vajalik QT jaoks
import random

# Kõik kasutatavad UI impordid.
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QPushButton, QWidget, QLabel, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import QTimer, Qt

class Bingo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bingo")  # Seadista akna pealkiri
        self.setGeometry(100, 100, 350, 400)  # Seadista akna suurus

        self.setStyleSheet("background-color: #333; color: #fff;")  # Kohandatud stiil paremaks väljanägemiseks

        self.KeskmineVidin = QWidget(self)
        self.setCentralWidget(self.KeskmineVidin)
        
        # Loo grid-paigutus
        self.Paigutus = QGridLayout()
        self.KeskmineVidin.setLayout(self.Paigutus)

        # Bingo nupud
        self.BingoNupud = {}
        self.rows = {i: set() for i in range(1, 6)}
        self.BingoLaud()

        self.List = QListWidget()
        self.Paigutus.addWidget(self.List, 0, 10, 9, 5)
        self.List.setMinimumSize(100, 300)
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
        self.Paigutus.addWidget(self.Nupp, 8, 0, 1, 5)

        # Nupp võidutingimuste kontrollimiseks
        self.WinNupp = QPushButton("Kontrolli Võit", self)
        self.WinNupp.clicked.connect(self.KontrolliVoit)
        self.Paigutus.addWidget(self.WinNupp, 9, 0, 1, 5)

        # Nupp reeglite näitamiseks
        self.ReeglidNupp = QPushButton("Näita Reeglid", self)
        self.ReeglidNupp.clicked.connect(self.NaitaReeglid)
        self.Paigutus.addWidget(self.ReeglidNupp, 10, 0, 1, 5)

        # Demorežiimi muutujad ja silt
        self.demo_reziim = False
        self.demo_silt = QLabel("Demorežiim", self)
        self.demo_silt.setAlignment(Qt.AlignCenter)
        self.demo_silt.setStyleSheet("font-size: 15px; color: lightblue;")
        self.demo_silt.setVisible(False)
        self.Paigutus.addWidget(self.demo_silt, 7, 0, 1, 5)
            
    def BingoLaud(self):
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
                
                # Jälgi positsioone võidutingimuste kontrollimiseks
                self.rows[Rida].add(Num)

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
            
            self.KontrolliVoit()  # Check for win conditions after announcing the number

    def KontrolliNumber(self, number):
        if number in self.BingoNupud:
            self.BingoNupud[number].click()

    def KontrolliVoit(self):
        drawn_numbers = set(int(num.split()[1]) for num in self.VarasemadNumbrid)
        
        # Märgi kõik märkimata nupud ja eemalda valesti märgitud nupud
        for number, button in self.BingoNupud.items():
            if number in drawn_numbers and button.styleSheet() != "background-color: yellow; color: black;":
                button.setStyleSheet("background-color: yellow; color: black;")
            elif number not in drawn_numbers and button.styleSheet() == "background-color: yellow; color: black;":
                button.setStyleSheet("background-color: #555; color: white;")

        win_conditions = 0

        for key in self.rows:
            if self.rows[key].issubset(drawn_numbers):
                win_conditions += 1

        balls_drawn = len(self.VarasemadNumbrid)

        if balls_drawn <= 10 and win_conditions >= 1:
            self.show_winner("1 rida täidetud 10 kuuliga!")
            self.reset_game()
        elif balls_drawn <= 20 and win_conditions >= 2:
            self.show_winner("2 rida täidetud 20 kuuliga!")
            self.reset_game()
        elif balls_drawn <= 30 and win_conditions >= 3:
            self.show_winner("3 rida täidetud 30 kuuliga!")
            self.reset_game()
        elif balls_drawn <= 40 and win_conditions >= 4:
            self.show_winner("4 rida täidetud 40 kuuliga!")
            self.reset_game()
        elif balls_drawn <= 50 and win_conditions >= 5:
            self.show_winner("5 rida täidetud 50 kuuliga!")
            self.reset_game()
        elif balls_drawn >= 50:
            self.show_winner("Kahjuks ei õnnestunud võita 50 kuuliga.")
            self.reset_game()

    def show_winner(self, win_type):
        QMessageBox.information(self, "Võit", f"Sa võitsid! ({win_type})")
        # Ära taaskäivita mängu, luba kasutajal edasi mängida

    def reset_game(self):
        self.VoimalikudNumbrid = list(range(1, 76))
        random.shuffle(self.VoimalikudNumbrid)
        self.VarasemadNumbrid.clear()
        self.List.clear()  # Tühjenda tõmmatud numbrite loend
        for num, btn in self.BingoNupud.items():
            btn.setStyleSheet("background-color: #555; color: white;")
        self.rows = {i: set() for i in range(1, 6)}
        self.BingoLaud()

    def NaitaReeglid(self):
        rules = (
            "Bingo Mängureeglid:\n"
            "1. Märgi oma kaardil kuulutatud numbrid.\n"
            "2. Võida, kui saad täis ühe või mitu järgmistest:\n"
            "   - Ühe rea 10 kuuliga\n"
            "   - Kaks rida 20 kuuliga\n"
            "   - Kolm rida 30 kuuliga\n"
            "   - Neli rida 40 kuuliga\n"
            "   - Kõik viis rida 50 kuuliga\n"
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
Aken.Demo()  # demorežiim
sys.exit(App.exec_())
