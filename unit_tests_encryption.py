import unittest
import os
from cryptography.fernet import Fernet
from encryption import write_key, decrypt
from encryption import load_key
from encryption import encrypt


class testEncryption(unittest.TestCase):

    def setUp(self):
        # Create a key file for testing
        with open("key.key", "wb") as key_file:
            key_file.write(b"test_key")
            # Create a test file
        with open("test_file.txt", "w") as test_file:
            test_file.write("Test data")
    def tearDown(self):
        # Remove the key file if it exists after each test
        if os.path.exists("key.key"):
            os.remove("key.key")
        if os.path.exists("test_file.txt"):
            os.remove("test_file.txt")

    def test_write_key(self):
        # Create a key file for testing
        with open("key.key", "wb") as key_file:
            key_file.write(b"test_key")

        # Call the function that will generate a key and save it to a file
        write_key()

        # Check whether the key file was created
        self.assertTrue(os.path.exists("key.key"))

        # Check whether the key file is not empty and saved to a file
        self.assertTrue(os.path.getsize("key.key") > 0)

        # Clean up the key file after the test
        os.remove("key.key")

    def test_load_key(self):
        # Call the function
        key = load_key()

        # Check whether the correct key was loaded
        expected_key = b"test_key"
        self.assertEqual(expected_key, key)

        # Remove the key file after the test
        os.remove("key.key")

    def test_encrypt(self):
        # Generate a test key
        test_key = Fernet.generate_key()

        # Call the function
        encrypt("test_file.txt", test_key)

        # Read the encrypted file
        with open("test_file.txt", "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()

        # Check if the file data is encrypted
        self.assertNotEqual(encrypted_data, b"Test data")

    def test_decrypt(self):
        # Generate a test key
        test_key = Fernet.generate_key()

        # Encrypt the test file
        encrypt("test_file.txt", test_key)

        # Call the function
        decrypt("test_file.txt", test_key)

        # Read the decrypted file
        with open("test_file.txt", "rb") as decrypted_file:
            decrypted_data = decrypted_file.read()

        # Check if the file data is decrypted correctly
        self.assertEqual(decrypted_data, b"Test data")


if __name__ == '__main__':
    unittest.main()
