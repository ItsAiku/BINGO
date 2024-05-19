import random


B1 = 0
B2 = 0
B3 = 0
B4 = 0
B5 = 0

numbrid_B = [i for i in range(1, 15)]
B1 = random.choice(numbrid_B)
numbrid_B.remove(B1)
B2 = random.choice(numbrid_B)
numbrid_B.remove(B2)
B3 = random.choice(numbrid_B)
numbrid_B.remove(B3)
B4 = random.choice(numbrid_B)
numbrid_B.remove(B4)
B5 = random.choice(numbrid_B)
numbrid_B.remove(B5)

#I rea genereerimine
I1 = 0
I2 = 0
I3 = 0
I4 = 0
I5 = 0

numbrid_I = [i for i in range(16, 30)]
I1 = random.choice(numbrid_I)
numbrid_I.remove(I1)
I2 = random.choice(numbrid_I)
numbrid_I.remove(I2)
I3 = random.choice(numbrid_I)
numbrid_I.remove(I3)
I4 = random.choice(numbrid_I)
numbrid_I.remove(I4)
I5 = random.choice(numbrid_I)
numbrid_I.remove(I5)

#N rea genereerimine
N1 = 0
N2 = 0
N3 = 0
N4 = 0
N5 = 0

numbrid_N = [i for i in range(31, 45)]
N1 = random.choice(numbrid_N)
numbrid_N.remove(N1)
N2 = random.choice(numbrid_N)
numbrid_N.remove(N2)
N3 = random.choice(numbrid_N)
numbrid_N.remove(N3)
N4 = random.choice(numbrid_N)
numbrid_N.remove(N4)
N5 = random.choice(numbrid_N)
numbrid_N.remove(N5)
#G rea genereerimine
G1 = 0
G2 = 0
G3 = 0
G4 = 0
G5 = 0

numbrid_G = [i for i in range(46, 60)]
G1 = random.choice(numbrid_G)
numbrid_G.remove(G1)
G2 = random.choice(numbrid_G)
numbrid_G.remove(G2)
G3 = random.choice(numbrid_G)
numbrid_G.remove(G3)
G4 = random.choice(numbrid_G)
numbrid_G.remove(G4)
G5 = random.choice(numbrid_G)
numbrid_G.remove(G5)

#O rea genereerimine
O1 = 0
O2 = 0
O3 = 0
O4 = 0
O5 = 0

numbrid_O = [i for i in range(61, 75)]
O1 = random.choice(numbrid_O)
numbrid_O.remove(O1)
O2 = random.choice(numbrid_O)
numbrid_O.remove(O2)
O3 = random.choice(numbrid_O)
numbrid_O.remove(O3)
O4 = random.choice(numbrid_O)
numbrid_O.remove(O4)
O5 = random.choice(numbrid_O)
numbrid_O.remove(O5)


print("--B--")

print(B1)
print(B2)
print(B3)
print(B4)
print(B5)

print("--I--")

print(I1)
print(I2)
print(I3)
print(I4)
print(I5)

print("--N--")

print(N1)
print(N2)
print(N3)
print(N4)
print(N5)

print("--G--")

print(G1)
print(G2)
print(G3)
print(G4)
print(G5)

print("--O--")

print(O1)
print(O2)
print(O3)
print(O4)
print(O5)
print("--------")


    