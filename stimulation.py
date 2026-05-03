import random
import matplotlib.pyplot as plt
from coder import Coder
from decoder import Decoder


def add_errors(bits, error_probability=0.1):
    """Фуекція яка рандомно додає помилки"""
    result = []
    for bit in bits:
        if random.random() < error_probability:
            result.append(1 - bit)
        else:
            result.append(bit)
    return result


def ber(original, decoded):
    errors = sum(a != b for a, b in zip(original, decoded))
    return errors / len(original)


def simulate(error_probability, msg_len=100, tests=100):
    coder = Coder()
    decoder = Decoder()
    total_ber = 0

    for _ in range(tests):
        msg = [random.randint(0, 1) for _ in range(msg_len)]
        encoded = coder.encode(msg)
        damaged = add_errors(encoded, error_probability)
        decoded = decoder.decode(damaged)

        total_ber += ber(msg, decoded)

    return total_ber / tests


def simulate_uncoded(error_probability, msg_len=100, tests=100):
    total_ber = 0

    for _ in range(tests):
        msg = [random.randint(0, 1) for _ in range(msg_len)]
        damaged = add_errors(msg, error_probability)

        total_ber += ber(msg, damaged)

    return total_ber / tests


if __name__ == "__main__":
    error_probs = [0.01, 0.03, 0.05, 0.1, 0.15, 0.2]
    coded = []
    uncoded = []
    for p in error_probs:
        coded.append(simulate(p))
        uncoded.append(simulate_uncoded(p))
    plt.plot(error_probs, coded, marker='o', label='coded')
    plt.plot(error_probs, uncoded, marker='o', label='uncoded')

    plt.xlabel("error probability")
    plt.ylabel("BER")
    plt.legend()
    plt.grid()
    plt.show()
