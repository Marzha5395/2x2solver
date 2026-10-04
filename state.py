class State:
    PSHIFTS = [37, 34, 31, 28, 25, 22, 19, 16] # number of shifts on state to access piece information about the i:th piece
    RSHIFTS = [14, 12, 10, 8, 6, 4, 2, 0] # number of shifts on state to access rotation information about the i:th piece
    __slots__ = "state",
    
    def __init__(self, state=0, pieces=None, rotations=None):
        if pieces is None or rotations is None: self.state = state
        else: self.state = self.encode(pieces, rotations)

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, value):
        if isinstance(value, State):
            return self.state == value.state
        return NotImplemented
    
    def modify(self, pos, n_bits, value):
        # ========================================
        # Helper function
        # Set the n_bits bits at pos to value
        # ========================================
        mask = (1 << n_bits) - 1
        self.state &= ~(mask << pos)
        self.state |= (value & mask) << pos

    def read(self, pos, n_bits):
        # ========================================
        # Helper function
        # Read the n_bits bits at position pos
        # ========================================
        mask = (1 << n_bits) - 1
        return (self.state >> pos) & mask

    def encode(self, pieces, rotations):
        # ========================================
        # Encode pieces and rotation into large
        # integer self.state
        # ========================================
        state = 0
        for p in pieces:
            state <<= 3
            state += p
        for r in rotations:
            state <<= 2
            state += r
        return state

    def decode(self):
        # ========================================
        # Decode self.state to lists pieces and
        # rotations (for debugging)
        # ========================================
        state = self.state
        pieces, rotations = [], []
        for i in range(8):
            rotations.append(state & 0b11)
            state >>= 2
        for i in range(8):
            pieces.append(state & 0b111)
            state >>= 3
        return pieces[::-1], rotations[::-1]

    def move(self, pieces, n_turns, twist=False):
        # ========================================
        # Helper function
        # Turns pieces clockwise by n_turns
        # ========================================

        pval = [self.read(self.PSHIFTS[p], 3) for p in pieces] # current value of all relevant pieces
        rval = [self.read(self.RSHIFTS[p], 2) for p in pieces] # current rotation of all relevant pieces

        for _ in range(n_turns):
            pval = pval[-1:] + pval[:-1]
            rval = rval[-1:] + rval[:-1]
        if twist:
            rval = [(rval[i] + i%2 + 1) % 3 for i in range(len(rval))]

        for i in range(len(pval)):
            self.modify(self.PSHIFTS[pieces[i]], 3, pval[i])
        
        for i in range(len(rval)):
            self.modify(self.RSHIFTS[pieces[i]], 2, rval[i])

    # ========================================
    # Define each of the nine standard moves
    # ========================================
    def R(self):
        self.move([2, 1, 6, 5], 1, twist=True)
    def R2(self):
        self.move([2, 1, 6, 5], 2, twist=False)
    def Rp(self):
        self.move([2, 1, 6, 5], 3, twist=True)

    def U(self):
        self.move([0, 1, 2, 3], 1, twist=False)
    def U2(self):
        self.move([0, 1, 2, 3], 2, twist=False)
    def Up(self):
        self.move([0, 1, 2, 3], 3, twist=False)

    def F(self):
        self.move([3, 2, 5, 4], 1, twist=True)
    def F2(self):
        self.move([3, 2, 5, 4], 2, twist=False)
    def Fp(self):
        self.move([3, 2, 5, 4], 3, twist=True)

    def idx2move(self, idx):
        # ========================================
        # Performs move based on index
        # ========================================
        assert 0 <= idx <= 8
        if idx == 0: self.R()
        if idx == 1: self.R2()
        if idx == 2: self.Rp()
        if idx == 3: self.U()
        if idx == 4: self.U2()
        if idx == 5: self.Up()
        if idx == 6: self.F()
        if idx == 7: self.F2()
        if idx == 8: self.Fp()
