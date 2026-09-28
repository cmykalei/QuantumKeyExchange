import unittest
import random
from qke import QKE
from qubit import Qubit
from xorcipher import XORCipher

# qke_test.py
# Unit test for qubit.py
class QKETest(unittest.TestCase):

    # Constructor for test.
    def setUp(self):
        self.stream_length = 256 # Any lower and it's not secure.
        self.alice = QKE("Alice", self.stream_length)
        self.bob = QKE("Bob", self.stream_length)
        self.eve = QKE("Eve", self.stream_length)


    # Verify valid stream length.
    def test_init_valid_stream_length_correct(self):
        self.assertEqual(self.alice.n, self.stream_length)
        self.assertEqual(self.bob.n, self.stream_length)


    # Verify invalid stream length exception.
    def test_init_invalid_stream_length_raises_error(self):
        with self.assertRaises(ValueError):
            QKE("Alice", -1)
            QKE("Bob", 0)


    # Verify valid qubit generation.
    #
    # If the qubits were generated,
    # Then the length of the A lists should match the stream length,
    # And the A values and polarizations should be either 0's or 1's
    def test_generate_correct(self):
        self.alice.generate()

        # The length of all lists should equal the stream length
        self.assertEqual(len(self.alice.val), self.stream_length)
        self.assertEqual(len(self.alice.pol), self.stream_length)

        # The values and polarizations should be either 0 or 1
        for v in self.alice.val:
            self.assertTrue(v == 0 or v == 1)
        for p in self.alice.pol:
            self.assertTrue(p == 0 or p == 1)


    # Verify invalid qubit measurement.
    def test_measure_raises_error(self):
        qubit_stream = self.alice.generate()
        with self.assertRaises(RuntimeError):
            self.alice.measure(qubit_stream)


    # Verify valid qubit measurement.
    #
    # If the qubits were generated and measured,
    # Then the lengths of measurements should be the same,
    # And the B values and polarizations should be either 0's or 1's
    def test_measure_correct(self):
        qubit_stream = self.alice.generate()
        self.bob.measure(qubit_stream)

        # They should have the same length of values
        self.assertEqual(len(self.alice.pol), len(self.bob.pol))
        self.assertEqual(len(self.alice.val), len(self.bob.val))

        # The values and polarizations should be either 0 or 1
        for v in self.bob.val:
            self.assertTrue(v == 0 or v == 1)
        for p in self.bob.pol:
            self.assertTrue(p == 0 or p == 1)


    # Verify messages exchanged are equal after decryption.
    def test_message_exchange(self):
        qubit_stream = self.alice.generate()
        self.bob.measure(qubit_stream)

        self.alice.exchange(self.bob.pol)
        self.bob.exchange(self.alice.pol)

        public_indices, public_key = self.alice.sift()
        self.bob.derive(public_indices, public_key)

        # Compute parities and correct errors if present.
        self.alice.correct_errors(self.bob.compute_parities())
        self.bob.correct_errors(self.alice.compute_parities())

        message = "Hello world!"
        encrypted = XORCipher(self.alice.private_key).encrypt(message)
        decrypted = XORCipher(self.bob.private_key).decrypt(encrypted)

        print(f"Original = {message}")
        print(f"Received = {decrypted}")

        self.assertEqual(message, decrypted)


    # Verify error is raised when qubits are intercepted.
    #
    # Note that true randomness is required, so to make
    # sure that the qubits are changed I've just done this
    # manually.
    #
    # What's interesting is that when I used the measure
    # function the test was inconsistently raising an
    # error or not. Another reason could be because
    # a stream length of 16 is too short.
    def test_eavesdrop_detected(self):
        qubit_stream = self.alice.generate()

        for qubit in qubit_stream:
            if qubit.value == 0 or qubit.polarization == 0:
                qubit.set(1,1)
            else:
                qubit.set(0,0)

        self.bob.measure(qubit_stream)
        self.alice.exchange(self.bob.pol)
        self.bob.exchange(self.alice.pol)

        public_indices, public_key = self.alice.sift()

        # Might not raise if stream length is too low.
        with self.assertRaises(RuntimeError):
            self.bob.derive(public_indices, public_key)


    # Verify message isn't read even if attacker has intercepted.
    #
    # If Eve manages to generate a key with Alice's qubits,
    # Then that key won't allow her to read the message.
    def test_eavesdrop_fails(self):
        qubit_stream = self.alice.generate()

        self.bob.measure(qubit_stream)

        self.alice.exchange(self.bob.pol)
        self.bob.exchange(self.alice.pol)

        self.eve.measure(qubit_stream.copy())
        self.eve.exchange(self.alice.pol)

        public_indices, public_key = self.alice.sift()
        self.bob.derive(public_indices, public_key)

        # Compute parities and correct errors if present.
        self.alice.correct_errors(self.bob.compute_parities())
        self.bob.correct_errors(self.alice.compute_parities())

        # This will also fail or pass depending on stream length.
        with self.assertRaises(RuntimeError):
            self.eve.derive(public_indices, public_key)

            message = "Hello world!"
            encrypted = XORCipher(alice.private_key).encrypt(message)

            decrypted = XORCipher(bob.private_key).decrypt(encrypted)
            corrupted = XORCipher(eve.private_key).decrypt(encrypted)

            print(f"Decrypted = {decrypted}")
            print(f"Corrupted = {corrupted}")

            self.assertTrue(decrypted != corrupted)


# Entry point.
if __name__ == '__main__':
    with open("logs/test_qke.txt", "w") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.defaultTestLoader.discover('.', pattern='*_test.py')
        unittest.main(testRunner=runner, exit=False)
