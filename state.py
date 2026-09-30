class State():
    PSHIFTS = [37, 34, 31, 28, 25, 22, 19, 16]
    RSHIFTS = [14, 12, 10, 8, 6, 4, 2, 0]
    __slots__ = 'state',
    
    def __init__(self, state=0, pieces=None, rotation=None):
        if pieces is None or rotation is None: self.state = state
        else: self.state = self.encode(pieces, rotation)

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

    def encode(self, pieces, rotation):
        state = 0
        for p in pieces:
            state <<= 3
            state += p
        for r in rotation:
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

        p1 = self.read(self.PSHIFTS[pieces[0]], 3)
        p2 = self.read(self.PSHIFTS[pieces[1]], 3)
        p3 = self.read(self.PSHIFTS[pieces[2]], 3)
        p4 = self.read(self.PSHIFTS[pieces[3]], 3)

        r1 = self.read(self.RSHIFTS[pieces[0]], 2)
        r2 = self.read(self.RSHIFTS[pieces[1]], 2)
        r3 = self.read(self.RSHIFTS[pieces[2]], 2)
        r4 = self.read(self.RSHIFTS[pieces[3]], 2)

        for _ in range(n_turns):
            p1, p2, p3, p4 = p4, p1, p2, p3
            r1, r2, r3, r4 = r4, r1, r2, r3
        if twist:
            r1 = (r1+1)%3
            r2 = (r2+2)%3
            r3 = (r3+1)%3
            r4 = (r4+2)%3

        self.modify(self.PSHIFTS[pieces[0]], 3, p1)
        self.modify(self.PSHIFTS[pieces[1]], 3, p2)
        self.modify(self.PSHIFTS[pieces[2]], 3, p3)
        self.modify(self.PSHIFTS[pieces[3]], 3, p4)
        
        self.modify(self.RSHIFTS[pieces[0]], 2, r1)
        self.modify(self.RSHIFTS[pieces[1]], 2, r2)
        self.modify(self.RSHIFTS[pieces[2]], 2, r3)
        self.modify(self.RSHIFTS[pieces[3]], 2, r4)

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
