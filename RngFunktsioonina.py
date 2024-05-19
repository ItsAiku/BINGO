import random

class Bingo:
    def __init__(self):
        self.drawn_numbers = set()

    def rng(self):
        if len(self.drawn_numbers) >= 75:
            print("Numbrid on valja jagatud!")
            return

        x = random.randint(1, 75)
        while x in self.drawn_numbers:
            x = random.randint(1, 75)
        
        self.drawn_numbers.add(x)

        if x <= 15:
            print("B", x)
        elif x <= 30:
            print("I", x)
        elif x <= 45:
            print("N", x)
        elif x <= 60:
            print("G", x)
        elif x <= 75:
            print("O", x)
        
rng = Bingo()

# Et numbreid Loosida copypasta shelli rng.rng()