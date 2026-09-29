class State():
    PSHIFTS = [37, 34, 31, 28, 25, 22, 19, 16]
    RSHIFTS = [14, 12, 10, 8, 6, 4, 2, 0]
    __slots__ = 'state',
    
    def __init__(self, state_int):
        self.state = state_int

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

    def decode(self):
        state_int = self.state
        state, target = [], []
        for i in range(8):
            target.append(state_int & 0b11)
            state_int >>= 2
        for i in range(8):
            state.append(state_int & 0b111)
            state_int >>= 3
        return state[::-1], target[::-1]

    def R(self):

        p1 = self.read(self.PSHIFTS[2], 3)
        p2 = self.read(self.PSHIFTS[1], 3)
        p3 = self.read(self.PSHIFTS[6], 3)
        p4 = self.read(self.PSHIFTS[5], 3)

        r1 = self.read(self.RSHIFTS[2], 2)
        r2 = self.read(self.RSHIFTS[1], 2)
        r3 = self.read(self.RSHIFTS[6], 2)
        r4 = self.read(self.RSHIFTS[5], 2)

        self.modify(self.PSHIFTS[2], 3, p4)
        self.modify(self.PSHIFTS[1], 3, p1)
        self.modify(self.PSHIFTS[6], 3, p2)
        self.modify(self.PSHIFTS[5], 3, p3)
        
        self.modify(self.RSHIFTS[2], 2, (r4+1)%3)
        self.modify(self.RSHIFTS[1], 2, (r1+2)%3)
        self.modify(self.RSHIFTS[6], 2, (r2+1)%3)
        self.modify(self.RSHIFTS[5], 2, (r3+2)%3)

    def R2(self):

        p1 = self.read(self.PSHIFTS[2], 3)
        p2 = self.read(self.PSHIFTS[1], 3)
        p3 = self.read(self.PSHIFTS[6], 3)
        p4 = self.read(self.PSHIFTS[5], 3)

        r1 = self.read(self.RSHIFTS[2], 2)
        r2 = self.read(self.RSHIFTS[1], 2)
        r3 = self.read(self.RSHIFTS[6], 2)
        r4 = self.read(self.RSHIFTS[5], 2)

        self.modify(self.PSHIFTS[2], 3, p3)
        self.modify(self.PSHIFTS[1], 3, p4)
        self.modify(self.PSHIFTS[6], 3, p1)
        self.modify(self.PSHIFTS[5], 3, p2)
        
        self.modify(self.RSHIFTS[2], 2, r3)
        self.modify(self.RSHIFTS[1], 2, r4)
        self.modify(self.RSHIFTS[6], 2, r1)
        self.modify(self.RSHIFTS[5], 2, r2)

    def Rp(self):

        p1 = self.read(self.PSHIFTS[2], 3)
        p2 = self.read(self.PSHIFTS[1], 3)
        p3 = self.read(self.PSHIFTS[6], 3)
        p4 = self.read(self.PSHIFTS[5], 3)

        r1 = self.read(self.RSHIFTS[2], 2)
        r2 = self.read(self.RSHIFTS[1], 2)
        r3 = self.read(self.RSHIFTS[6], 2)
        r4 = self.read(self.RSHIFTS[5], 2)

        self.modify(self.PSHIFTS[2], 3, p2)
        self.modify(self.PSHIFTS[1], 3, p3)
        self.modify(self.PSHIFTS[6], 3, p4)
        self.modify(self.PSHIFTS[5], 3, p1)
        
        self.modify(self.RSHIFTS[2], 2, (r2+1)%3)
        self.modify(self.RSHIFTS[1], 2, (r3+2)%3)
        self.modify(self.RSHIFTS[6], 2, (r4+1)%3)
        self.modify(self.RSHIFTS[5], 2, (r1+2)%3)

    def U(self):

        p1 = self.read(self.PSHIFTS[0], 3)
        p2 = self.read(self.PSHIFTS[1], 3)
        p3 = self.read(self.PSHIFTS[2], 3)
        p4 = self.read(self.PSHIFTS[3], 3)

        r1 = self.read(self.RSHIFTS[0], 2)
        r2 = self.read(self.RSHIFTS[1], 2)
        r3 = self.read(self.RSHIFTS[2], 2)
        r4 = self.read(self.RSHIFTS[3], 2)

        self.modify(self.PSHIFTS[0], 3, p4)
        self.modify(self.PSHIFTS[1], 3, p1)
        self.modify(self.PSHIFTS[2], 3, p2)
        self.modify(self.PSHIFTS[3], 3, p3)
        
        self.modify(self.RSHIFTS[0], 2, r4)
        self.modify(self.RSHIFTS[1], 2, r1)
        self.modify(self.RSHIFTS[2], 2, r2)
        self.modify(self.RSHIFTS[3], 2, r3)

    def U2(self):

        p1 = self.read(self.PSHIFTS[0], 3)
        p2 = self.read(self.PSHIFTS[1], 3)
        p3 = self.read(self.PSHIFTS[2], 3)
        p4 = self.read(self.PSHIFTS[3], 3)

        r1 = self.read(self.RSHIFTS[0], 2)
        r2 = self.read(self.RSHIFTS[1], 2)
        r3 = self.read(self.RSHIFTS[2], 2)
        r4 = self.read(self.RSHIFTS[3], 2)

        self.modify(self.PSHIFTS[0], 3, p3)
        self.modify(self.PSHIFTS[1], 3, p4)
        self.modify(self.PSHIFTS[2], 3, p1)
        self.modify(self.PSHIFTS[3], 3, p2)
        
        self.modify(self.RSHIFTS[0], 2, r3)
        self.modify(self.RSHIFTS[1], 2, r4)
        self.modify(self.RSHIFTS[2], 2, r1)
        self.modify(self.RSHIFTS[3], 2, r2)
    
    def Up(self):

        p1 = self.read(self.PSHIFTS[0], 3)
        p2 = self.read(self.PSHIFTS[1], 3)
        p3 = self.read(self.PSHIFTS[2], 3)
        p4 = self.read(self.PSHIFTS[3], 3)

        r1 = self.read(self.RSHIFTS[0], 2)
        r2 = self.read(self.RSHIFTS[1], 2)
        r3 = self.read(self.RSHIFTS[2], 2)
        r4 = self.read(self.RSHIFTS[3], 2)

        self.modify(self.PSHIFTS[0], 3, p2)
        self.modify(self.PSHIFTS[1], 3, p3)
        self.modify(self.PSHIFTS[2], 3, p4)
        self.modify(self.PSHIFTS[3], 3, p1)
        
        self.modify(self.RSHIFTS[0], 2, r2)
        self.modify(self.RSHIFTS[1], 2, r3)
        self.modify(self.RSHIFTS[2], 2, r4)
        self.modify(self.RSHIFTS[3], 2, r1)

    def F(self):

        p1 = self.read(self.PSHIFTS[3], 3)
        p2 = self.read(self.PSHIFTS[2], 3)
        p3 = self.read(self.PSHIFTS[5], 3)
        p4 = self.read(self.PSHIFTS[4], 3)

        r1 = self.read(self.RSHIFTS[3], 2)
        r2 = self.read(self.RSHIFTS[2], 2)
        r3 = self.read(self.RSHIFTS[5], 2)
        r4 = self.read(self.RSHIFTS[4], 2)

        self.modify(self.PSHIFTS[3], 3, p4)
        self.modify(self.PSHIFTS[2], 3, p1)
        self.modify(self.PSHIFTS[5], 3, p2)
        self.modify(self.PSHIFTS[4], 3, p3)
        
        self.modify(self.RSHIFTS[3], 2, (r4+1)%3)
        self.modify(self.RSHIFTS[2], 2, (r1+2)%3)
        self.modify(self.RSHIFTS[5], 2, (r2+1)%3)
        self.modify(self.RSHIFTS[4], 2, (r3+2)%3)

    def F2(self):

        p1 = self.read(self.PSHIFTS[3], 3)
        p2 = self.read(self.PSHIFTS[2], 3)
        p3 = self.read(self.PSHIFTS[5], 3)
        p4 = self.read(self.PSHIFTS[4], 3)

        r1 = self.read(self.RSHIFTS[3], 2)
        r2 = self.read(self.RSHIFTS[2], 2)
        r3 = self.read(self.RSHIFTS[5], 2)
        r4 = self.read(self.RSHIFTS[4], 2)

        self.modify(self.PSHIFTS[3], 3, p3)
        self.modify(self.PSHIFTS[2], 3, p4)
        self.modify(self.PSHIFTS[5], 3, p1)
        self.modify(self.PSHIFTS[4], 3, p2)
        
        self.modify(self.RSHIFTS[3], 2, r3)
        self.modify(self.RSHIFTS[2], 2, r4)
        self.modify(self.RSHIFTS[5], 2, r1)
        self.modify(self.RSHIFTS[4], 2, r2)

    def Fp(self):

        p1 = self.read(self.PSHIFTS[3], 3)
        p2 = self.read(self.PSHIFTS[2], 3)
        p3 = self.read(self.PSHIFTS[5], 3)
        p4 = self.read(self.PSHIFTS[4], 3)

        r1 = self.read(self.RSHIFTS[3], 2)
        r2 = self.read(self.RSHIFTS[2], 2)
        r3 = self.read(self.RSHIFTS[5], 2)
        r4 = self.read(self.RSHIFTS[4], 2)

        self.modify(self.PSHIFTS[3], 3, p2)
        self.modify(self.PSHIFTS[2], 3, p3)
        self.modify(self.PSHIFTS[5], 3, p4)
        self.modify(self.PSHIFTS[4], 3, p1)
        
        self.modify(self.RSHIFTS[3], 2, (r2+1)%3)
        self.modify(self.RSHIFTS[2], 2, (r3+2)%3)
        self.modify(self.RSHIFTS[5], 2, (r4+1)%3)
        self.modify(self.RSHIFTS[4], 2, (r1+2)%3)
