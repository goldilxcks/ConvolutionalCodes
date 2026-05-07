class Coder:
    def __init__(self):
        self.shift = 3
        self.num_states = 4
        self.transition_table = self.build_table()

    def build_table(self):
        table = {}
        #проходимо крізь усі можливі стани (від 00 до 11 у двійковій системі)
        for state in range(self.num_states):
            for bit in [0, 1]:
                next_state = (bit << 1) | (state >> 1)
                reg = [bit, (state >> 1) & 1, state & 1]
                out1 = reg[0] ^ reg[1] ^ reg[2]
                out2 = reg[1] ^ reg[2]
                out3 = reg[0] ^ reg[2]
                table[(state, bit)] = (next_state, (out1, out2, out3))
        return table

    def encode(self, bits):
        bits_full = bits + [0] * (self.shift - 1)
        result = []
        state = 0
        for b in bits_full:
            next_state, out_bits = self.transition_table[(state, b)]
            result.extend(out_bits)
            state = next_state
        return result
