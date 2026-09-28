from state import State

class Solver():
    def __init__(self):
        self.neighbors = [
            (4, 17), (16, 13), (8, 5), (12, 9),
            (17, 0), (2, 8), (22, 19), (10, 20),
            (5, 2), (3, 12), (20, 7), (14, 21),
            (9, 3), (1, 16), (21, 11), (18, 23),
            (13, 1), (0, 4), (23, 15), (6, 22),
            (7, 10), (11, 14), (19, 6), (15, 18)
        ]
        self.opposite = [0, 2, 1, 4, 3, 6, 5]
        self.sticker2rotation = [0, 0, 0, 0, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 0, 0, 0, 0]
        self.sticker2piece = [0, 1, 3, 2, 0, 3, 7, 4, 3, 2, 4, 5, 2, 1, 5, 6, 1, 0, 6, 7, 4, 5, 7, 6]

    def encode(self, state):
        if len(state) != 24:
            raise ValueError('Error')
        if state.count(0):
            raise ValueError('Unfilled colors')
        for i in range(1, 7):
            if state.count(i) != 4:
                raise ValueError('Colors not valid')

        target_faces = [self.opposite[state[22]], state[6], self.opposite[state[19]], self.opposite[state[6]], state[19], state[22]]

        state_encoded = [-1] * 8
        rotation_encoded = [-1] * 8

        for i in range(24):
            if state[i] == target_faces[0]:
                n1, n2 = self.neighbors[i]
                piece = self.sticker2piece[i]
                rotation = self.sticker2rotation[i]
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
                n1, n2 = self.neighbors[i]
                piece = self.sticker2piece[i]
                rotation = self.sticker2rotation[i]
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

        target_state = list(range(8))
        target_rotation = [0] * 8

        state_int = 0
        for s in state_encoded:
            state_int <<= 3
            state_int += s
        for r in rotation_encoded:
            state_int <<= 2
            state_int += r
        
        target_int = 0
        for s in target_state:
            target_int <<= 3
            target_int += s
        for r in target_rotation:
            target_int <<= 2
            target_int += r
        
        return State(state_int), State(target_int)

    def solve(self, state, target):
        state.R2()
        print(state.decode())
        return []


    def run(self, state):
        try:
            state, target = self.encode(state)
            solution = self.solve(state, target)
            return solution
        except ValueError as e:
            return f"Error: {e}"
        
def main():
    state = [6,1,3,1,4,5,3,5,1,6,2,4,3,5,2,6,4,1,2,6,3,5,2,4]
    solver = Solver()
    solution = solver.run(state)
    print(solution)

if __name__ == '__main__':
    main()
