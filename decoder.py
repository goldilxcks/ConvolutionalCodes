from coder import Coder


class Decoder:
    def __init__(self):
        self.coder = Coder()
        self.table = self.coder.transition_table
        self.num_states = self.coder.num_states
        self.shift = self.coder.shift

        self.reverse_table = {s: [] for s in range(self.num_states)}
        for (state, bit), (next_state, out_bits) in self.table.items():
            self.reverse_table[next_state].append((state, bit, out_bits))

    def hamming(self, a, b):
        return sum(x != y for x, y in zip(a, b))

    def decode(self, received: list[int]) -> list[int]:
        num_steps = len(received) // 3
        msg_len = num_steps - (self.shift - 1)   

        INF = float('inf')

        path_metric = {s: (INF, []) for s in range(self.num_states)}
        path_metric[0] = (0, [])   
        for step in range(num_steps):
            rx = tuple(received[step * 3: step * 3 + 3])
            new_metric = {s: (INF, []) for s in range(self.num_states)}

            for state in range(self.num_states):
                curr_m, curr_path = path_metric[state]
                if curr_m == INF:
                    continue

                for bit in (0, 1):
                    next_state, out_bits = self.table[(state, bit)]
                    cost = curr_m + self.hamming(rx, out_bits)

                    if cost < new_metric[next_state][0]:
                        new_metric[next_state] = (cost, curr_path + [bit])

            path_metric = new_metric

        best_metric, best_path = path_metric[0]
        return best_path[:msg_len]



coder = Coder()
msg = [1, 0, 1, 1]
encoded = coder.encode(msg)
decoder = Decoder()
print(decoder.decode(encoded))
