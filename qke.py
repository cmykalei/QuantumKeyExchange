import random
from qubit import Qubit
from xorcipher import XORCipher

# qke.py
# Provides functions to perform the Quantum Key Exchange protocol.
class QKE:

    # Constructor.
    def __init__(self, name: str, stream_length: int):
        if stream_length < 16:
            raise ValueError(f"{name}: Stream length must be greater than 16.")
        else:
            self.name = name            # The name of the party, for debugging.
            self.n = stream_length      # The amount of qubits in this exchange.
            self.val = []               # The values of the qubits.
            self.pol = []               # The polarization values of the qubits.
            self.mask = []              # The mask containing matches.
            self.raw_key = []           # The raw private key.
            self.public_key = None      # The portion of key to compare.
            self.private_key = None     # The private key used for encryption.

            # As per the spec, a length of 16 is allowed but I think it should be higher.
            if stream_length < 256:
                print(f"{self.name}: Warning: Key won't be secure if stream length is less than 256.")


    # Generates Qubits for the exchange.
    #
    # Returns   The list of qubits generated. Pretend it's a stream.
    def generate(self) -> list[Qubit]:
        if self.val:
            raise RuntimeError(f"{self.name}: Qubits should not be regenerated for the same exchange.")
        else:
            stream = []
            for _ in range(self.n):
                v = random.randint(0, 1)
                p = random.randint(0, 1)
                self.val.append(v)
                self.pol.append(p)
                stream.append(Qubit(v, p))

            return stream


    # Receives transmitted Qbuits, measuring polarizations.
    #
    # Param     [stream]    The stream of qubits to measure.
    # Returns   The list of measurements, the polarizations.
    def measure(self, stream: list[Qubit]) -> list[int]:
        if self.val:
            raise RuntimeError(f"{self.name}: Qubits should not be measured twice in the same exchange.")
        else:
            for qubit in stream:
                p = random.randint(0, 1)
                v = qubit.measure(p)
                self.val.append(v)
                self.pol.append(p)

            return self.pol


    # Exchange polarizations with the other party.
    #
    # Param     [pol]   The other party's polarization list.
    def exchange(self, pol: list[int]):
        if len(self.pol) != len(pol):
            raise RuntimeError(f"{self.name}: Eavesdropping detected! Mismatch in the amount of Qubits exchanged.")
        else:
            self.mask = [i for i, (a, b) in enumerate(zip(self.pol, pol)) if a == b]


    # Generates subset of key with indices of matches.
    #
    # Returns   The list of matching indices and the sifted public key.
    def sift(self) -> tuple[list[int], str]:
        if not self.mask:
            raise RuntimeError(f"{self.name}: Polarization lists must be exchanged before deriving keys.")
        elif self.public_key or self.private_key:
            raise RuntimeError(f"{self.name}: A public key should not be extracted from the same measurements.")
        else:
            upper = min(len(self.mask), 72) # At least 72 remaining qubits is preferred.
            lower = int(upper * 0.2)
            public_indices = random.sample(self.mask, min(lower, upper))

            self.raw_key = [self.val[i] for i in self.mask if i not in public_indices]
            self.public_key = ''.join(str(self.val[i]) for i in public_indices)

            return public_indices, self.public_key


    # Computes the parities to support error correction.
    #
    # Param     [block_size]    The block size, set to 8 bits.
    # Returns   The list of parities for error correction.
    def compute_parities(self, block_size: int = 8) -> list[int]:
        parities = []
        for i in range(0, len(self.raw_key), block_size):
            block = self.raw_key[i:i+block_size]
            parities.append(sum(block) % 2)

        return parities


    # Performs error correction on parities.
    #
    # Param     [parities]  The list of parities to correct.
    def correct_errors(self, parities: list[int], block_size: int = 8):
        for i in range(len(parities)):
            first = i * block_size
            last = first + block_size

            block = self.raw_key[first:last]
            parity = sum(block) % 2

            if parity != parities[i]:
                for j in range(first, min(last, len(self.raw_key))):
                    self.raw_key[j] ^= 1

        self.private_key = ''.join(map(str, self.raw_key))


    # Derive a final private key uses the public values.
    #
    # Param     [public_indices]    The list of indices where a match was found.
    # Param     [public_key]        The other's public key to verifiy.
    def derive(self, public_indices: list[int], public_key: str, parities: list[int] = None):
        if not self.mask:
            raise RuntimeError(f"{self.name}: Polarization lists must be exchanged before deriving keys.")
        elif self.public_key or self.private_key:
            raise RuntimeError(f"{self.name}: A private key should not be derived from the same measurements.")
        else:
            expected_key = ''.join(str(self.val[i]) for i in public_indices)
            if public_key != expected_key:
                raise RuntimeError(f"Eavesdropping detected! Expected [{expected_key}] but received [{public_key}]")
            else:
                self.raw_key = [self.val[i] for i in self.mask if i not in public_indices]

