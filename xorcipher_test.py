import unittest
from xorcipher import XORCipher

# xorcipher_test.py
# Unit test for xorcipher.py
class XORCipherTest(unittest.TestCase):

    VALID_KEY="01010101"
    INVALID_KEY="02020202"
    VALID_TEXT="Plain text"

    # Verifies init function creates XORCipher instance.
    def test_init(self):
        """Test valid initialization of XORCipher instance"""
        xorcipher = XORCipher(self.VALID_KEY)
        self.assertIsInstance(xorcipher, XORCipher)


    # Verifies init function exception with invalid (empty) key.
    def test_empty_key(self):
        """Test invalid initialization raises ValueError when empty key"""
        with self.assertRaises(ValueError):
            XORCipher(self.INVALID_KEY)


    # Verifies encrypt function exception with empty plain text.
    #
    # If given an empty string, then encrypt should return empty bytes.
    def test_empty_plain_text(self):
        """Test encryption returns no bytes if plain text is empty"""
        xorcipher = XORCipher(self.VALID_KEY)
        encrypted = xorcipher.encrypt("")
        self.assertEqual(encrypted, b"")


    # Verifies decrypt function exception with empty cipher text.
    #
    # If given empty bytes, then decrypt should return empty an string.
    def test_empty_cipher_text(self):
        """Test decryption returns empty string if no bytes"""
        xorcipher = XORCipher(self.VALID_KEY)
        decrypted = xorcipher.decrypt(b"")
        self.assertEqual(decrypted, "")


    # Verifies xor function with valid encryption.
    #
    # If plain text is encrypted,
    # Then the encrypted bytes should not match the plain text as bytes.
    def test_xor_encrypt(self):
        """Test encrypted bytes are not equal to the plain text as bytes"""
        xorcipher = XORCipher(self.VALID_KEY)
        plain_text = self.VALID_TEXT
        cipher_text = xorcipher.encrypt(plain_text)
        self.assertNotEqual(cipher_text, plain_text.encode())


    # Verifies xor function with valid decryption.
    #
    # If plain text is encrypted,
    # Then the decrypted text should match the plain text.
    def test_xor_decrypt(self):
        """Test decrypted text equals original plain text"""
        xorcipher = XORCipher(self.VALID_KEY)
        plain_text = self.VALID_TEXT
        cipher_text = xorcipher.encrypt(plain_text)
        decrypted = xorcipher.decrypt(cipher_text)
        self.assertEqual(decrypted, plain_text)


    # Proof that reusing the same key leaks information.
    #
    # If two plain text messages are encrypted,
    # And the same key is used to XOR,
    # Then parts of the message will be revealed.
    def test_key_reuse_vulnerability(self):
        xorcipher = XORCipher(self.VALID_KEY)
        message_a = "hello"
        message_b = "world"
        encrypted_a = xorcipher.encrypt(message_a)
        encrypted_b = xorcipher.encrypt(message_b)
        xor_ciphered = bytes(a ^ b for a, b in zip(encrypted_a, encrypted_b))
        xor_original = bytes(a ^ b for a, b in zip(message_a.encode(), message_b.encode()))
        self.assertEqual(xor_ciphered, xor_original)


# Entry point.
if __name__ == '__main__':
    with open("logs/test_xorcipher.txt", "w") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.defaultTestLoader.discover('.', pattern='*_test.py')
        unittest.main(testRunner=runner, exit=False)
