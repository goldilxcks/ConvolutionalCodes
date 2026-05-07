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
        result.append(noisy_signal)
    return result


def ber(original, decoded):
    """Counts bit error rate."""
    errors = 0
    for bit1, bit2 in zip(original, decoded):
        if bit1 != bit2:
            errors += 1
    return errors / len(original)


def simulate_coded(ebno_db, msg_len=100, tests=100):
    """Simulates coded transmission through AWGN channel."""
    coder = Coder()
    decoder = Decoder()
    rate = 1/3
    total_ber = 0
    snr_db = ebno_db + 10 * math.log10(rate)
    for _ in range(tests):
        msg = []
        for _ in range(msg_len):
            msg.append(random.randint(0, 1))
        encoded = coder.encode(msg)
        damaged = add_awgn(encoded, snr_db)
        decoded = decoder.decode(damaged)
        total_ber += ber(msg, decoded)
    return total_ber / tests


def simulate_uncoded(ebno_db, msg_len=5000, tests=1000):
    """Simulates uncoded transmission through AWGN channel."""
    total_errors = 0
    snr_linear = 10 ** (ebno_db / 10)
    sigma = math.sqrt(1 / (2 * snr_linear))

    for _ in range(tests):
        msg = [random.randint(0, 1) for _ in range(msg_len)]
        for bit in msg:
            signal = 1 if bit == 1 else -1
            noisy = signal + random.gauss(0, sigma)
            received = 1 if noisy > 0 else 0
            if received != bit:
                total_errors += 1
    return total_errors / (msg_len * tests)


if __name__ == "__main__":
    ebno_values = [-2, -1, 0, 0.5, 1, 1.5, 2, 3, 4, 5, 6]
    coded = []
    uncoded = []

    for ebno in ebno_values:
        coded_ber = simulate_coded(ebno)
        uncoded_ber = simulate_uncoded(ebno)
        coded.append(coded_ber)
        uncoded.append(uncoded_ber)
        print(f"SNR = {ebno} dB | coded BER = {coded_ber} | uncoded BER = {uncoded_ber}")

    plt.figure(figsize=(10, 6))
    plt.semilogy(ebno_values, coded, 'b-o', linewidth=2, label="Coded")
    plt.semilogy(ebno_values, uncoded, 'r--s', linewidth=2, label="Uncoded")
    plt.xlabel("$E_b/N_0$ (dB)")
    plt.ylabel("Bit Error Rate")
    plt.title("Порівняння ефективності: Coded vs Uncoded (AWGN)")
    plt.grid(True, which="both", linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()
