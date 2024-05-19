
import random

class bingo:
    def rng(self):
        x = random.randint(1,75)
        if x <= 15:
            print( "B",x)
        elif x <= 30:
            print( "I",x)
        elif x <= 45:
            print( "N",x)
        elif x <= 60:
            print( "G",x) 
        elif x <= 75:
            print( "O",x) 
      
        
        
rng=bingo()
rng.rng()
