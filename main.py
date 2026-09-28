import os
import sys
import random
from qke import QKE
from xorcipher import XORCipher

# Main method for QKE.
# Demonstrates the QKE algorithm, logs output to demo_qke.txt.
def main():
    stream_lengths = [16, 256, 1024]
    output_file = "logs/demo_qke.txt"

    with open(output_file, 'w') as file:
        for length in stream_lengths:
            message = "Hello world!"
            alice = QKE("Alice", length)
            bob = QKE("Bob", length)

            # Alice generates the qubits and Bob measures the stream
            bob.measure(alice.generate())

            # Alice and Bob exchange polarizations
            alice.exchange(bob.pol)
            bob.exchange(alice.pol)

            # Alice and Bob
            public_indices, public_key = alice.sift()

            # Bob compares her public key, generates his private key.
            try:
                bob.derive(public_indices, public_key)
            except RuntimeError as e:
                print(f"Aborting Quantum Key Exchange: {e}")
                return

            # Compute parities and correct errors if present.
            alice.correct_errors(bob.compute_parities())
            bob.correct_errors(alice.compute_parities())

            # Alice encrypts the message and Bob decrypts it
            encrypted = XORCipher(alice.private_key).encrypt(message)
            decrypted = XORCipher(bob.private_key).decrypt(encrypted)

            # Output values
            log(f"[{length}][a][val]{alice.val}", file)
            log(f"[{length}][b][val]{bob.val}", file)
            log(f"[{length}][a][pol]{alice.pol}", file)
            log(f"[{length}][b][pol]{bob.pol}", file)
            log(f"[{length}][a][key][{alice.private_key}]", file)
            log(f"[{length}][b][key][{bob.private_key}]", file)

            # Verify message exchange
            log(f"[{length}][a][msg][{encrypted.hex()}]", file)
            log(f"[{length}] Original: \"{message}\"", file)
            log(f"[{length}] Received: \"{decrypted}\"", file)


# Prints to file and stdout.
#
# Param     [ln]    The line to log.
# Param     [file]  The file to output the log to.
def log(ln, file):
    if file is not None:
        print(ln, file=file)


# Entry point.
if __name__ == "__main__":
    main()
