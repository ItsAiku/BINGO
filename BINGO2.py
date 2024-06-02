import sys  # Needed for QT
import random

# All the UI imports we are using.
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QPushButton, QWidget, QLabel, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import QTimer, Qt

class Bingo(QMainWindow):
    def __init__(self):
        super().__init__()

        # All QT documentation can be found here if you need to change anything - https://doc.qt.io/qt-5/

        self.setWindowTitle("Bingo")  # Set window title
        self.setGeometry(100, 100, 350, 400)  # Set window size

        self.setStyleSheet("background-color: #333; color: #fff;")  # Custom styles for better look

        self.KeskmineVidin = QWidget(self)
        self.setCentralWidget(self.KeskmineVidin)
        
        # Create grid layout
        self.Paigutus = QGridLayout()
        self.KeskmineVidin.setLayout(self.Paigutus)

        # Bingo buttons
        self.BingoNupud = {}
        self.rows = {i: set() for i in range(1, 6)}
        self.cols = {i: set() for i in range(5)}
        self.diag1 = set()
        self.diag2 = set()
        self.BingoLaud()

        self.List = QListWidget()
        self.Paigutus.addWidget(self.List, 0, 10, 9, 5)
        self.List.setMinimumSize(100, 300)
        self.List.setStyleSheet("background-color: #2A2A2A; color: #fff;")
        
        # Label for announcing numbers
        self.TeadeSilt = QLabel("", self)
        self.TeadeSilt.setAlignment(Qt.AlignCenter)
        self.Paigutus.addWidget(self.TeadeSilt, 6, 0, 1, 5)

        # List of possible numbers
        self.VoimalikudNumbrid = list(range(1, 76))
        random.shuffle(self.VoimalikudNumbrid)
        
        self.VarasemadNumbrid = list()

        self.Nupp = QPushButton("Näita Numbrid", self)
        self.Nupp.clicked.connect(self.TeataNumber)
        self.Nupp.setEnabled(True)
        self.Paigutus.addWidget(self.Nupp, 8, 0, 1, 5)

        # Button to check for winning conditions
        self.WinNupp = QPushButton("Kontrolli Võit", self)
        self.WinNupp.clicked.connect(self.KontrolliVoit)
        self.Paigutus.addWidget(self.WinNupp, 9, 0, 1, 5)

        # Demo mode variable and label
        self.demo_reziim = False
        self.demo_silt = QLabel("Demorežiim", self)
        self.demo_silt.setAlignment(Qt.AlignCenter)
        self.demo_silt.setStyleSheet("font-size: 15px; color: lightblue;")
        self.demo_silt.setVisible(False)
        self.Paigutus.addWidget(self.demo_silt, 7, 0, 1, 5)
            
    def BingoLaud(self):
        # Most efficient way
        Vahemikud = {
            'B': (1, 15),
            'I': (16, 30),
            'N': (31, 45),
            'G': (46, 60),
            'O': (61, 75),
        }
                
        for Veerg, (Taht, (Algus, Lopp)) in enumerate(Vahemikud.items()):
            # Add column titles, i.e., B I N G O
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
                
                # Track the positions for winning condition checks
                self.rows[Rida].add(Num)
                self.cols[Veerg].add(Num)
                if Rida == Veerg + 1:
                    self.diag1.add(Num)
                if Rida + Veerg == 5:
                    self.diag2.add(Num)

    def NuppEvent(self):
        Nupp = self.sender()
        Nupp.setStyleSheet("background-color: yellow; color: black;")
        self.KontrolliVoit()

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
        if number in self.BingoNupud:
            self.BingoNupud[number].click()

    def KontrolliVoit(self):
        drawn_numbers = set(int(num.split()[1]) for num in self.VarasemadNumbrid)

        # Mark all unmarked buttons
        for number, button in self.BingoNupud.items():
            if number in drawn_numbers and button.styleSheet() != "background-color: yellow; color: black;":
                button.setStyleSheet("background-color: yellow; color: black;")

        # Check for winning conditions
        for key in self.rows:
            if self.rows[key].issubset(drawn_numbers):
                self.show_winner("Rida")
                return
        #Voidab Ainult Ridadega
        #for key in self.cols:
        #    if self.cols[key].issubset(drawn_numbers):
        #        self.show_winner("Veerg")
        #        return

        #if self.diag1.issubset(drawn_numbers):
        #    self.show_winner("Diagonaal 1")
        #    return
        
        #if self.diag2.issubset(drawn_numbers):
        #    self.show_winner("Diagonaal 2")
        #    return

    def show_winner(self, win_type):
        QMessageBox.information(self, "Võit", f"Sa võitsid! ({win_type})")
        self.reset_game()

    def reset_game(self):
        self.VoimalikudNumbrid = list(range(1, 76))
        random.shuffle(self.VoimalikudNumbrid)
        self.VarasemadNumbrid.clear()
        self.List.clear()  # Clear the drawn numbers list
        for num, btn in self.BingoNupud.items():
            btn.setStyleSheet("background-color: #555; color: white;")
        self.rows = {i: set() for i in range(1, 6)}
        self.cols = {i: set() for i in range(5)}
        self.diag1.clear()
        self.diag2.clear()
        self.BingoLaud()

    def Demo(self):
        self.demo_reziim = True
        self.demo_silt.setVisible(True)
        self.Nupp.setEnabled(False)
        self.Taimer = QTimer(self)
        self.Taimer.timeout.connect(self.TeataNumber)
        self.Taimer.start(500)

App = QApplication(sys.argv)
App.setStyle("Fusion")  # I love this QT theme, mashallah https://doc.qt.io/qt-6.5/qtquickcontrols-fusion.html
Aken = Bingo()

Aken.show()
# Aken.Demo()  # demo mode
sys.exit(App.exec_())  # https://stackoverflow.com/questions/45508090/what-is-the-necessity-of-sys-exitapp-exec-in-pyqt
