from coder import Coder

class Decoder:
    def __init__(self):
        self.coder = Coder()
        self.table = self.coder.transition_table
        self.num_states = self.coder.num_states
        self.shift = self.coder.shift

    def euclidean(self, rx, expected):
        distance = 0
        for r, e in zip(rx, expected):
            expected_signal = 1 if e == 1 else -1
            distance += (r - expected_signal) ** 2
        return distance

    def decode(self, received):
        num_steps = len(received) // 3
        msg_len = num_steps - (self.shift - 1)
        INF = float('inf')
        metrics = [INF] * self.num_states
        metrics[0] = 0
        predecessors = []
        decided_bits = []

        for step in range(num_steps):
            rx = received[step * 3: step * 3 + 3]
            new_metrics = [INF] * self.num_states
            pred = [0] * self.num_states
            bits = [0] * self.num_states

            for state in range(self.num_states):
                if metrics[state] == INF:
                    continue
                for bit in (0, 1):
                    next_state, out_bits = self.table[(state, bit)]
                    branch_metric = self.euclidean(rx, out_bits)
                    cost = metrics[state] + branch_metric
                    if cost < new_metrics[next_state]:
                        new_metrics[next_state] = cost
                        pred[next_state] = state
                        bits[next_state] = bit
            metrics = new_metrics
            predecessors.append(pred)
            decided_bits.append(bits)
        # state = 0
        # decoded = []
        # for step in range(num_steps - 1, -1, -1):
        #     bit = decided_bits[step][state]
        #     decoded.append(bit)
        #     state = predecessors[step][state]
        # decoded.reverse()
        state = metrics.index(min(metrics))
        decoded = []
        for step in range(num_steps - 1, -1, -1):
            bit = decided_bits[step][state]
            decoded.append(bit)
            state = predecessors[step][state]
        decoded.reverse()
        return decoded[:msg_len]
