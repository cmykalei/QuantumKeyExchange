import hashlib

# xorcipher.py
# Provides instance of a XORCipher which encrypts and decrypts data.
class XORCipher:

    # Constructor.
    def __init__(self, key: str):
        if not key:
            raise ValueError("Key must not be empty.")
        else:
            self.private_key = self._convert(key)


    # Converts a string to bytes.
    #
    # Param     [key]  The key string to convert.
    # Returns   The string, to a multiple of 8 to represent a byte.
    def _convert(self, key: str) -> bytes:
        if not key:
            raise ValueError("Key must not be empty")
        elif not all(c in ('0', '1') for c in key):
            raise ValueError("Key must be a binary containing 0's or 1's.")
        else:
            key_bytes = []
            for i in range(0, len(key), 8):  # Step 8 up to end of key
                chunk = key[i:i+8]           # Get 8 key bits
                value = int(chunk, 2)        # Convert binary to int
                key_bytes.append(value)      # Append int to list

            return bytes(key_bytes)          # Convert list of ints to bytes


    # Performs XOR on data with respect to the key.
    #
    # Param     [data]      The str of data to XOR.
    # Returns   The data as bytes, flipped with respect to the keys.
    def _xor(self, data: bytes) -> bytes:
        key_length = len(self.private_key)
        result = bytearray()
        for index, b in enumerate(data):
            key_byte = self.private_key[index % key_length]
            xor_byte = b ^ key_byte
            result.append(xor_byte)

        return bytes(result)


    # Calls XOR function on the plain text to encrypt it.
    #
    # Param     [plain_text]    The plain text to encrypt with XOR.
    # Returns   The encrypted text, as bytes with respect to the key.
    def encrypt(self, plain_text: str) -> bytes:
        if not self.private_key:
            raise ValueError("Shared key must be created before encrypting.")
        else:
            length = len(self.private_key)
            if length < int(len(plain_text) * 8):
                print(f"Sender: Warning: Key is too short ({length}) to guarantee security.")

            plain_bytes = plain_text.encode('utf-8')
            cipher_text = self._xor(plain_bytes)

            return cipher_text


    # Calls XOR function on the cipher text to decrypt it.
    #
    # Param     [cipher_text]    The cipher text to decrypt with XOR.
    # Returns   The decrypted text, as a string with respect to the key.
    def decrypt(self, cipher_text: bytes) -> str:
        if not self.private_key:
            raise ValueError("Shared key must be created before encrypting.")
        else:
            length = len(self.private_key)
            if length < len(cipher_text):
                print(f"Receiver: Warning: Key is too short ({length}) to guarantee security.")

            plain_bytes = self._xor(cipher_text)
            plain_text = plain_bytes.decode('utf-8', errors='replace')

            return plain_text

