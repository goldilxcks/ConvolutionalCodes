"""Simulation of convolutional code with AWGN channel."""
import random
import math
import matplotlib.pyplot as plt

from coder import Coder
from decoder import Decoder


def add_awgn(bits, snr_db):
    """Adds AWGN noise to bits and returns received hard bits."""
    result = []

    snr_linear = 10 ** (snr_db / 10)
    sigma = math.sqrt(1 / (2 * snr_linear))

    for bit in bits:
        signal = 1 if bit == 1 else -1

        noise = random.gauss(0, sigma)
        noisy_signal = signal + noise

        if noisy_signal > 0:
            result.append(1)
        else:
            result.append(0)

    return result


def ber(original, decoded):
    """Counts bit error rate."""
    errors = 0

    for bit1, bit2 in zip(original, decoded):
        if bit1 != bit2:
            errors += 1

    return errors / len(original)


def simulate_coded(snr_db, msg_len=100, tests=100):
    """Simulates coded transmission through AWGN channel."""
    coder = Coder()
    decoder = Decoder()

    total_ber = 0

    for _ in range(tests):
        msg = []

        for _ in range(msg_len):
            msg.append(random.randint(0, 1))

        encoded = coder.encode(msg)
        damaged = add_awgn(encoded, snr_db)
        decoded = decoder.decode(damaged)

        total_ber += ber(msg, decoded)

    return total_ber / tests


def simulate_uncoded(snr_db, msg_len=100, tests=100):
    """Simulates uncoded transmission through AWGN channel."""
    total_ber = 0

    for _ in range(tests):
        msg = []

        for _ in range(msg_len):
            msg.append(random.randint(0, 1))

        damaged = add_awgn(msg, snr_db)

        total_ber += ber(msg, damaged)

    return total_ber / tests


if __name__ == "__main__":
    snr_values = [-2, 0, 1, 2, 3, 4, 5, 6]

    coded = []
    uncoded = []

    for snr in snr_values:
        coded_ber = simulate_coded(snr)
        uncoded_ber = simulate_uncoded(snr)

        coded.append(coded_ber)
        uncoded.append(uncoded_ber)

        print(f"SNR = {snr} dB | coded BER = {coded_ber} | uncoded BER = {uncoded_ber}")

    plt.plot(snr_values, coded, marker="o", label="coded")
    plt.plot(snr_values, uncoded, marker="o", label="uncoded")

    plt.xlabel("SNR, dB")
    plt.ylabel("BER")
    plt.title("BER vs SNR for AWGN channel")
    plt.legend()
    plt.grid()
    plt.show()
