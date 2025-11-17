from domain.interfaces.ciper_interface import CipherInterface

class SubstitutionCipher(CipherInterface):
    def __init__(self):
        # Hardcoded cipher mapping
        self.original = "abcdefghijklmnopqrstuvwxyz0123456789"
        self.substitution = "zy9876543210xwvutsrqponmlkjihgfedcba"

        # Create the cipher and reverse cipher dictionaries
        self.cipher = dict(zip(self.original, self.substitution))
        self.reverse_cipher = dict(zip(self.substitution, self.original))

    def encrypt(self, message):
        """Encrypt the given message using the substitution cipher."""
        encrypted_message = ''.join(self.cipher.get(c, c) for c in message)
        return encrypted_message

    def decrypt(self, encrypted_message):
        """Decrypt the given message using the reverse substitution cipher."""
        decrypted_message = ''.join(self.reverse_cipher.get(c, c) for c in encrypted_message)
        return decrypted_message
