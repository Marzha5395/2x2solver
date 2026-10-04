"""
Specifikation för uppgift 2x2solver (egenpåhittad uppgift)

Uppgiften går ut på att användaren matar in färgerna på en
2x2 Rubik's kub med standard färgschema. Programmet söker
sedan efter den kortaste lösningen till just det tillståndet
och skriver ut lösningen.

Datastruktur: Ett State-objekt som representerar kubens tillstånd
där varje objekt har instansvariabeln:
    state: ett ~40 bitars heltal som lagrar positionen (3 bitar) och
    rotationen (2 bitar) för samtliga 8 hörnbitar.

Dessutom används ett Solver-objekt för att omvandla kubens råa
tillstånd av en lista med 24 heltal till ett State-objekt,
samt för att hitta den kortaste lösningen lösning.

Algoritm:
I kronologisk ordning sker följande:
1 - Användaren matar in färgen på samtliga 24 klistermärken via
    terminalen eller det grafiska användargränssnittet.
2 - Den råa listan med 24 färger skickas genom metoden "encode",
    som komprimerar det till två listor "pieces" och "rotations"
    som sedan omvandlas till State-objekt.
3 - En dubbelriktad breadth first search (BFS) körs mellan det
    nuvarande tillståndet och det lösta tillståndet tills båda
    båda sökningarna möts i en gemensam punkt
4 - Lösningen spåras tillbaka och en lista "solution" av drag
    konstureras och returneras.
5 - Listan med drag skrivs ut i terminalen eller det grafiska
    användargränssnittet.
"""

class State:
    # skapa self.state utifrån state eller pieces och rotations
    def __init__(self, state=0, pieces=None, rotations=None):
        pass

    # läser ut n_bits bitar vid position pos
    def read(self, pos, n_bits):
        pass

    # sätter n_bits bits vid position pos till value
    def modify(self, pos, n_bits, value):  
        pass

    # roterar bitarna n_turns medurs
    def move(self, pieces, n_turns, twists):  
        pass

    # koda pieces och rotations till self.state
    def encode(self, pieces, rotations):
        pass

    # avkoda self.state till pieces och rotations
    def decode(self):
        pass


class Solver:
    # kodar det råa tillståndet till två listor pieces och rotations
    def encode(self, rawstate):
        pass

    # löser kuber i givet dess tillstånd mha dubbelriktad BFS
    # rekonstruerar och returnerar lösningen
    def solve(self, state, target):
        pass

    # kör hela lösaren, encode + solve
    def run(self, rawstate):
        pass


class App:
    # bygg upp själva fönstret och knappar i __init__
    def __init__(self):
        pass

    # återställer fönstret till initiala tillståndet
    def reset(self):
        pass

    # byt det aktiverade klistermärket på kuben till id
    def activate(self, id):
        pass

    # placerar färgen color på det aktiverade klistermärket
    def placecolor(self, color):
        pass

    # kallar på lösaren och visar lösningen i det grafiska användargränssnittet
    def solve(self):
        pass

# introduktion och läsa kubens råa tillstånd
def intro():
    pass

def main():
    try:
        rawstate = intro()
        solver = Solver()
        solution = solver.run(rawstate)
        print(f"{solution}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
