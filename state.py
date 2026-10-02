class State():
    PSHIFTS = [37, 34, 31, 28, 25, 22, 19, 16]
    RSHIFTS = [14, 12, 10, 8, 6, 4, 2, 0]
    __slots__ = 'state',
    
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
        mask = (1 << n_bits) - 1
        self.state &= ~(mask << pos)
        self.state |= (value & mask) << pos

    def read(self, pos, n_bits):
        mask = (1 << n_bits) - 1
        return (self.state >> pos) & mask

    def encode(self, pieces, rotations):
        state = 0
        for p in pieces:
            state <<= 3
            state += p
        for r in rotations:
            state <<= 2
            state += r
        return state

    def decode(self):
        state = self.state
        pieces, target = [], []
        for i in range(8):
            target.append(state & 0b11)
            state >>= 2
        for i in range(8):
            pieces.append(state & 0b111)
            state >>= 3
        return pieces[::-1], target[::-1]

    def move(self, pieces, n_turns, twist=False):

        p_val = [self.read(self.PSHIFTS[p], 3) for p in pieces]
        r_val = [self.read(self.RSHIFTS[p], 2) for p in pieces]

        for _ in range(n_turns):
            p_val = p_val[-1:] + p_val[:-1]
            r_val = r_val[-1:] + r_val[:-1]
        if twist:
            r_val = [(r_val[i] + i%2 + 1) % 3 for i in range(len(r_val))]

        for i in range(len(p_val)):
            self.modify(self.PSHIFTS[pieces[i]], 3, p_val[i])
        
        for i in range(len(r_val)):
            self.modify(self.RSHIFTS[pieces[i]], 2, r_val[i])

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
