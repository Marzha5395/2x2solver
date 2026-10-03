from state import State
from collections import deque

class Solver:
    NEIGHBORS = [ # index of the two neighbors of each of the 24 stickers
        (4, 17), (16, 13), (8, 5), (12, 9),
        (17, 0), (2, 8), (22, 19), (10, 20),
        (5, 2), (3, 12), (20, 7), (14, 21),
        (9, 3), (1, 16), (21, 11), (18, 23),
        (13, 1), (0, 4), (23, 15), (6, 22),
        (7, 10), (11, 14), (19, 6), (15, 18)
    ]
    OPPOSITE = [0, 2, 1, 4, 3, 6, 5]
    STICKER2PIECE = [0, 1, 3, 2, 0, 3, 7, 4, 3, 2, 4, 5, 2, 1, 5, 6, 1, 0, 6, 7, 4, 5, 7, 6]
    STICKER2ROTATION = [0, 0, 0, 0, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 0, 0, 0, 0]
    MOVES = ["R", "R2", "R'", "U", "U2", "U'", "F", "F2", "F'"]
    OPPOSITEMOVES = ["R'", "R2", "R", "U'", "U2", "U", "F'", "F2", "F"]
    OPPOSITEINDEX = [2, 1, 0, 5, 4, 3, 8, 7, 6]

    def encode(self, rawstate):
        # ========================================
        # Encodes the raw state into more compact
        # information with pieces and rotation
        # ========================================
        if len(rawstate) != 24:
            raise ValueError("State did not have 24 elements")
        if rawstate.count(0):
            raise ValueError("Unfilled colors, please fill in all colors before clicking solve")
        for i in range(1, 7):
            if rawstate.count(i) != 4:
                raise ValueError("Colors not valid, make sure there are 4 of each color")
            

        targetfaces = [self.OPPOSITE[rawstate[22]], rawstate[6], self.OPPOSITE[rawstate[19]], self.OPPOSITE[rawstate[6]], rawstate[19], rawstate[22]]

        pieces = [-1] * 8
        rotations = [-1] * 8

        # Loop over all stickers to check which piece is at that position
        for i in range(24):
            if rawstate[i] == targetfaces[0]:
                n1, n2 = self.NEIGHBORS[i]
                t1, t2 = [1, 4, 3, 2], [4, 3, 2, 1]
                piece = self.STICKER2PIECE[i]
                rotation = self.STICKER2ROTATION[i]
                for j in range(4):
                    if rawstate[n1] == targetfaces[t1[j]] and rawstate[n2] == targetfaces[t2[j]]:
                        pieces[piece] = j
                        rotations[piece] = rotation

            if rawstate[i] == targetfaces[5]:
                n1, n2 = self.NEIGHBORS[i]
                t1, t2 = [1, 2, 3, 4], [2, 3, 4, 1]
                piece = self.STICKER2PIECE[i]
                rotation = self.STICKER2ROTATION[i]
                for j in range(4):
                    if rawstate[n1] == targetfaces[t1[j]] and rawstate[n2] == targetfaces[t2[j]]:
                        pieces[piece] = j+4
                        rotations[piece] = rotation

        if sorted(pieces) != list(range(8)):
            raise ValueError("Invalid state, check that you entered the colors correctly")
        if sum(rotations) % 3 != 0:
            raise ValueError("Corner is twisted, check that you entered the colours correctly")
        
        return pieces, rotations

    def solve(self, state, target):
        # ========================================
        # Solves the cube given the state using
        # bidirectional BFS
        # Reconstructs solution and returns it 
        # as a list of MOVES
        # ========================================
        if state == target:
            raise ValueError("Cube already solved")

        # Initialize bidirectional BFS
        visited = {} # keep track of which states has already been visited
        bfs = deque()
        bfs.append(state)
        bfs.append(target)
        visited[state] = (0, 9) # (origin, lastmove)
        visited[target] = (1, 9) # (origin, lastmove)
        meetpoint = None

        # Run bidirectional BFS
        while bfs:
            currstate = bfs.popleft()
            origin, lastmove = visited[currstate]
            for move in range(9):
                if lastmove // 3 == move // 3: continue # if same move type as before (R/U/F)
                newstate = State(currstate.state)
                newstate.idx2move(move)
                if newstate not in visited:
                    bfs.append(newstate)
                    visited[newstate] = (origin, move)
                elif visited[newstate][0] + origin == 1:
                    meetpoint = newstate
                    finalmove = move
                    break

            if meetpoint is not None:
                break

        if meetpoint is None:
            raise ValueError("Solution not found")

        # Reconstruct solution
        solution = []
        if visited[meetpoint][0]:
            # Path from scramble
            backtrack = State(meetpoint.state)
            solution.append(self.MOVES[finalmove])
            backtrack.idx2move(self.OPPOSITEINDEX[finalmove])
            while visited[backtrack][1] < 9:
                solution.append(self.MOVES[visited[backtrack][1]])
                backtrack.idx2move(self.OPPOSITEINDEX[visited[backtrack][1]])
            solution.reverse()

            # Path from target
            backtrack = State(meetpoint.state)
            while visited[backtrack][1] < 9:
                solution.append(self.OPPOSITEMOVES[visited[backtrack][1]])
                backtrack.idx2move(self.OPPOSITEINDEX[visited[backtrack][1]])

        else:
            # Path from scramble
            backtrack = State(meetpoint.state)
            while visited[backtrack][1] < 9:
                solution.append(self.MOVES[visited[backtrack][1]])
                backtrack.idx2move(self.OPPOSITEINDEX[visited[backtrack][1]])
            solution.reverse()

            # Path from target
            backtrack = State(meetpoint.state)
            solution.append(self.OPPOSITEMOVES[finalmove])
            backtrack.idx2move(self.OPPOSITEINDEX[finalmove])
            while visited[backtrack][1] < 9:
                solution.append(self.OPPOSITEMOVES[visited[backtrack][1]])
                backtrack.idx2move(self.OPPOSITEINDEX[visited[backtrack][1]])

        return solution


    def run(self, rawstate):
        # ========================================
        # Run entire solver & returns solution
        # ========================================
        try:
            pieces, rotations = self.encode(rawstate)
            state = State(pieces=pieces, rotations=rotations)
            target = State(pieces=list(range(8)), rotations=[0]*8)
            solution = self.solve(state, target)
            return f"Solution found:\n{" ".join(solution)}"
        except ValueError as e:
            return f"Error: {e}"

def intro():
    # ========================================
    # Introduction, read raw state from input
    # ========================================
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
    | G | H |   | K | L |   | O | P |   | S | T |
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
    White: w
    Yellow: y
    Red: r
    Orange: o
    Blue: b
    Green: g

    Please enter the state of your cube:
    """
    print(introtext)
    
    faces = ["U", "L", "F", "R", "B", "D"]
    color2int = {"w":1, "y":2, "r":3, "o":4, "b":5, "g":6}

    # Read input
    rawstate = []
    for f in faces:
        face = "".join(input(f"{f} face: ").split()).lower()
        if len(face) != 4:
            raise ValueError("Enter exactly 4 colors per face")
        for s in face:
            if s not in color2int.keys():
                raise ValueError("Invalid character, enter only w/y/r/o/b/g")
            rawstate.append(color2int[s])
    return rawstate


def main():
    try:
        rawstate = intro()
        # rawstate = [6, 1, 3, 1, 4, 5, 3, 5, 1, 6, 2, 4, 3, 5, 2, 6, 4, 1, 2, 6, 3, 5, 2, 4] # hard coded state for debugging
        # rawstate = [1, 4, 1, 6, 5, 4, 4, 4, 6, 2, 6, 6, 3, 1, 1, 3, 5, 3, 5, 5, 2, 3, 2, 2] # hard coded state for debugging
        solver = Solver()
        solution = solver.run(rawstate)
        print(f"{solution}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
