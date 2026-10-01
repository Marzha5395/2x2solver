from state import State
from collections import deque
import random

COLOR2INT = {
    "W":1,
    "Y":2,
    "R":3,
    "O":4,
    "B":5,
    "G":6,
}

class Solver():
    NEIGHBORS = [
        (4, 17), (16, 13), (8, 5), (12, 9),
        (17, 0), (2, 8), (22, 19), (10, 20),
        (5, 2), (3, 12), (20, 7), (14, 21),
        (9, 3), (1, 16), (21, 11), (18, 23),
        (13, 1), (0, 4), (23, 15), (6, 22),
        (7, 10), (11, 14), (19, 6), (15, 18)
    ]
    OPPOSITE = [0, 2, 1, 4, 3, 6, 5]
    STICKER2ROTATION = [0, 0, 0, 0, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 0, 0, 0, 0]
    STICKER2PIECE = [0, 1, 3, 2, 0, 3, 7, 4, 3, 2, 4, 5, 2, 1, 5, 6, 1, 0, 6, 7, 4, 5, 7, 6]
    MOVES = ["R", "R2", "R'", "U", "U2", "U'", "F", "F2", "F'"]
    OPPOSITEMOVES = ["R'", "R2", "R", "U'", "U2", "U", "F'", "F2", "F"]

    def __init__(self):
        pass

    def encode(self, state):
        if len(state) != 24:
            raise ValueError('Error')
        if state.count(0):
            raise ValueError('Unfilled colors')
        for i in range(1, 7):
            if state.count(i) != 4:
                raise ValueError('Colors not valid')

        target_faces = [self.OPPOSITE[state[22]], state[6], self.OPPOSITE[state[19]], self.OPPOSITE[state[6]], state[19], state[22]]

        state_encoded = [-1] * 8
        rotation_encoded = [-1] * 8

        for i in range(24):
            if state[i] == target_faces[0]:
                n1, n2 = self.NEIGHBORS[i]
                piece = self.STICKER2PIECE[i]
                rotation = self.STICKER2ROTATION[i]
                if state[n1] == target_faces[1] and state[n2] == target_faces[4]:
                    state_encoded[piece] = 0
                    rotation_encoded[piece] = rotation
                if state[n1] == target_faces[4] and state[n2] == target_faces[3]:
                    state_encoded[piece] = 1
                    rotation_encoded[piece] = rotation
                if state[n1] == target_faces[3] and state[n2] == target_faces[2]:
                    state_encoded[piece] = 2
                    rotation_encoded[piece] = rotation
                if state[n1] == target_faces[2] and state[n2] == target_faces[1]:
                    state_encoded[piece] = 3
                    rotation_encoded[piece] = rotation

            if state[i] == target_faces[5]:
                n1, n2 = self.NEIGHBORS[i]
                piece = self.STICKER2PIECE[i]
                rotation = self.STICKER2ROTATION[i]
                if state[n1] == target_faces[1] and state[n2] == target_faces[2]:
                    state_encoded[piece] = 4
                    rotation_encoded[piece] = rotation
                if state[n1] == target_faces[2] and state[n2] == target_faces[3]:
                    state_encoded[piece] = 5
                    rotation_encoded[piece] = rotation
                if state[n1] == target_faces[3] and state[n2] == target_faces[4]:
                    state_encoded[piece] = 6
                    rotation_encoded[piece] = rotation
                if state[n1] == target_faces[4] and state[n2] == target_faces[1]:
                    state_encoded[piece] = 7
                    rotation_encoded[piece] = rotation

        if state_encoded.count(-1):
            raise ValueError('State invalid')
        if sum(rotation_encoded) % 3 != 0:
            raise ValueError('Corner is twisted')
        
        return state_encoded, rotation_encoded

    def solve(self, state, target):
        if state == target:
            raise ValueError("Cube already solved")
        visited = {}
        bfs = deque()
        bfs.append(state)
        bfs.append(target)
        visited[state] = (0, 9) # (origin, lastmove)
        visited[target] = (1, 9) # (origin, lastmove)
        meetpoint = None

        while bfs:
            currstate = bfs.popleft()
            origin, lastmove = visited[currstate]
            if lastmove // 3 != 0:
                newstate0 = State(currstate.state)
                newstate0.R()
                if newstate0 not in visited:
                    bfs.append(newstate0)
                    visited[newstate0] = (origin, 0)
                elif visited[newstate0][0] + origin == 1:
                    meetpoint = newstate0
                    finalmove = 0
                    break

                newstate1 = State(currstate.state)
                newstate1.R2()
                if newstate1 not in visited:
                    bfs.append(newstate1)
                    visited[newstate1] = (origin, 1)
                elif visited[newstate1][0] + origin == 1:
                    meetpoint = newstate1
                    finalmove = 1
                    break

                newstate2 = State(currstate.state)
                newstate2.Rp()
                if newstate2 not in visited:
                    bfs.append(newstate2)
                    visited[newstate2] = (origin, 2)
                elif visited[newstate2][0] + origin == 1:
                    meetpoint = newstate2
                    finalmove = 2
                    break
            
            if lastmove // 3 != 1:
                newstate3 = State(currstate.state)
                newstate3.U()
                if newstate3 not in visited:
                    bfs.append(newstate3)
                    visited[newstate3] = (origin, 3)
                elif visited[newstate3][0] + origin == 1:
                    meetpoint = newstate3
                    finalmove = 3
                    break

                newstate4 = State(currstate.state)
                newstate4.U2()
                if newstate4 not in visited:
                    bfs.append(newstate4)
                    visited[newstate4] = (origin, 4)
                elif visited[newstate4][0] + origin == 1:
                    meetpoint = newstate4
                    finalmove = 4
                    break

                newstate5 = State(currstate.state)
                newstate5.Up()
                if newstate5 not in visited:
                    bfs.append(newstate5)
                    visited[newstate5] = (origin, 5)
                elif visited[newstate5][0] + origin == 1:
                    meetpoint = newstate5
                    finalmove = 5
                    break
                
            if lastmove // 3 != 2:
                newstate6 = State(currstate.state)
                newstate6.F()
                if newstate6 not in visited:
                    bfs.append(newstate6)
                    visited[newstate6] = (origin, 6)
                elif visited[newstate6][0] + origin == 1:
                    meetpoint = newstate6
                    finalmove = 6
                    break

                newstate7 = State(currstate.state)
                newstate7.F2()
                if newstate7 not in visited:
                    bfs.append(newstate7)
                    visited[newstate7] = (origin, 7)
                elif visited[newstate7][0] + origin == 1:
                    meetpoint = newstate7
                    finalmove = 7
                    break

                newstate8 = State(currstate.state)
                newstate8.Fp()
                if newstate8 not in visited:
                    bfs.append(newstate8)
                    visited[newstate8] = (origin, 8)
                elif visited[newstate8][0] + origin == 1:
                    meetpoint = newstate8
                    finalmove = 8
                    break

        if meetpoint is None:
            raise ValueError('Solution not found')

        solution = []
        if visited[meetpoint][0]:
            backtrack = State(meetpoint.state)
            solution.append(self.MOVES[finalmove])
            if finalmove == 0: backtrack.Rp()
            if finalmove == 1: backtrack.R2()
            if finalmove == 2: backtrack.R()
            if finalmove == 3: backtrack.Up()
            if finalmove == 4: backtrack.U2()
            if finalmove == 5: backtrack.U()
            if finalmove == 6: backtrack.Fp()
            if finalmove == 7: backtrack.F2()
            if finalmove == 8: backtrack.F()
            while visited[backtrack][1] < 9:
                solution.append(self.MOVES[visited[backtrack][1]])
                if visited[backtrack][1] == 0: backtrack.Rp()
                elif visited[backtrack][1] == 1: backtrack.R2()
                elif visited[backtrack][1] == 2: backtrack.R()
                elif visited[backtrack][1] == 3: backtrack.Up()
                elif visited[backtrack][1] == 4: backtrack.U2()
                elif visited[backtrack][1] == 5: backtrack.U()
                elif visited[backtrack][1] == 6: backtrack.Fp()
                elif visited[backtrack][1] == 7: backtrack.F2()
                elif visited[backtrack][1] == 8: backtrack.F()
            backtrack = State(meetpoint.state)
            solution.reverse()
            while visited[backtrack][1] < 9:
                solution.append(self.OPPOSITEMOVES[visited[backtrack][1]])
                if visited[backtrack][1] == 0: backtrack.Rp()
                elif visited[backtrack][1] == 1: backtrack.R2()
                elif visited[backtrack][1] == 2: backtrack.R()
                elif visited[backtrack][1] == 3: backtrack.Up()
                elif visited[backtrack][1] == 4: backtrack.U2()
                elif visited[backtrack][1] == 5: backtrack.U()
                elif visited[backtrack][1] == 6: backtrack.Fp()
                elif visited[backtrack][1] == 7: backtrack.F2()
                elif visited[backtrack][1] == 8: backtrack.F()
        else:
            backtrack = State(meetpoint.state)
            while visited[backtrack][1] < 9:
                solution.append(self.MOVES[visited[backtrack][1]])
                if visited[backtrack][1] == 0: backtrack.Rp()
                elif visited[backtrack][1] == 1: backtrack.R2()
                elif visited[backtrack][1] == 2: backtrack.R()
                elif visited[backtrack][1] == 3: backtrack.Up()
                elif visited[backtrack][1] == 4: backtrack.U2()
                elif visited[backtrack][1] == 5: backtrack.U()
                elif visited[backtrack][1] == 6: backtrack.Fp()
                elif visited[backtrack][1] == 7: backtrack.F2()
                elif visited[backtrack][1] == 8: backtrack.F()
            backtrack = State(meetpoint.state)
            solution.reverse()
            solution.append(self.OPPOSITEMOVES[finalmove])
            if finalmove == 0: backtrack.Rp()
            if finalmove == 1: backtrack.R2()
            if finalmove == 2: backtrack.R()
            if finalmove == 3: backtrack.Up()
            if finalmove == 4: backtrack.U2()
            if finalmove == 5: backtrack.U()
            if finalmove == 6: backtrack.Fp()
            if finalmove == 7: backtrack.F2()
            if finalmove == 8: backtrack.F()
            while visited[backtrack][1] < 9:
                solution.append(self.OPPOSITEMOVES[visited[backtrack][1]])
                if visited[backtrack][1] == 0: backtrack.Rp()
                elif visited[backtrack][1] == 1: backtrack.R2()
                elif visited[backtrack][1] == 2: backtrack.R()
                elif visited[backtrack][1] == 3: backtrack.Up()
                elif visited[backtrack][1] == 4: backtrack.U2()
                elif visited[backtrack][1] == 5: backtrack.U()
                elif visited[backtrack][1] == 6: backtrack.Fp()
                elif visited[backtrack][1] == 7: backtrack.F2()
                elif visited[backtrack][1] == 8: backtrack.F()

        return solution


    def scramble(self, n=11):
        state = State(pieces=list(range(8)), rotation=[0]*8)
        last = None
        for _ in range(n):
            face = random.choice([f for f in "RUF" if f != last])
            getattr(state, face + random.choice(["", "2", "p"]))()
            last = face
        pieces, rotation = state.decode()
        faces = [1, 5, 3, 6, 4, 2]
        sides = [(1, 4), (4, 3), (3, 2), (2, 1), (1, 2), (2, 3), (3, 4), (4, 1)]
        colors = [0] * 24
        for i in range(24):
            piece, rot = pieces[self.STICKER2PIECE[i]], rotation[self.STICKER2PIECE[i]]
            if self.STICKER2ROTATION[i] == rot:
                n1, n2 = self.NEIGHBORS[i]
                colors[i] = faces[0 if piece < 4 else 5]
                colors[n1], colors[n2] = faces[sides[piece][0]], faces[sides[piece][1]]
        return colors

    def run(self, state):
        try:
            pieces, rotation = self.encode(state)
            state = State(pieces=pieces, rotation=rotation)
            target = State(pieces=list(range(8)), rotation=[0]*8)
            solution = self.solve(state, target)
            return f"Solution found:\n{" ".join(solution)}"
        except ValueError as e:
            return f"Error: {e}"
        
def main():
    introtext = """
    Welcome to 2x2solver! Enter the state of the cube in the following format:

                +---+---+
                | A | B |
                |---|---|
                | C | D |
                +---+---+
    +---+---+   +---+---+   +---+---+   +---+---+
    | E | F |   | I | J |   | M | N |   | Q | R |
    |---|---|   |---|---|   |---|---|   |---|---|
    | G | H |   | K | L |   | O | P |   | T | S |
    +---+---+   +---+---+   +---+---+   +---+---+
                +---+---+
                | U | V |
                |---|---|
                | W | X |
                +---+---+

    U face: A B C D
    L face: E F G H
    F face: I J K L
    R face: M N O P
    B face: Q R S T
    D face: U V W X

    Each of the stickers should be represented with a single character:
    White: W
    Yellow: Y
    Red: R
    Orange: O
    Blue: B
    Green: G

    Please enter the state of your cube:
    """
    print(introtext)

    state = []
    for f in ["U", "L", "F", "R", "B", "D"]:
        try:
            face = "".join(input(f"{f} face: ").split()).upper()
            assert len(face) == 4
            for s in face:
                state.append(COLOR2INT[s])
        except:
            print("Invalid input")
            return

    solver = Solver()
    solution = solver.run(state)
    print(f"{solution}")

if __name__ == "__main__":
    main()
