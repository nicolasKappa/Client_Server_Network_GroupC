import unittest
from unittest.mock import Mock, patch
import os
import serverfinal

class ServerFinalTests(unittest.TestCase):

    def setUp(self):
        # Create a key file for testing
        with open("test_key.key", "wb") as key_file:
            key_file.write(b"test_key")

    def tearDown(self):
        # Remove the key file if it exists after each test
        os.remove("test_key.key")

    def test_receive_and_decrypt_data(self):
        print("Testing receive_and_decrypt_data function...")
        # Mock the socket and other dependencies
        mock_socket = Mock()
        mock_key = b'secret_key'
        encrypted_data = b'EncryptedData'
        decrypted_data = b'DecryptedData'

        # Mock the recv method of the socket to return the encrypted data
        mock_socket.recv.return_value = encrypted_data

        # Mock the serverfinal.Fernet.decrypt method
        with patch('serverfinal.Fernet') as mock_fernet:
            mock_fernet.return_value.decrypt.return_value = decrypted_data

            # Call the function to be tested
            result = serverfinal.receive_and_decrypt_data(mock_socket, mock_key)

            # Assertions
            self.assertEqual(result, decrypted_data)
            mock_socket.recv.assert_called_once_with(1024)
            mock_fernet.assert_called_once_with(mock_key)
            mock_fernet.return_value.decrypt.assert_called_once_with(encrypted_data)
        
        print("receive_and_decrypt_data test successful!")

    def test_deserialize_data(self):
        print("Testing deserialize_data function...")
        # Test the deserialize_data function
        serialized_data = b'\x80\x03}q\x00(X\x03\x00\x00\x00keyq\x01X\x05\x00\x00\x00valueq\x02u.'
        expected_data = {'key': 'value'}

        result = serverfinal.deserialize_data(serialized_data)

        self.assertEqual(result, expected_data)
        print("deserialize_data test successful!")

 
if __name__ == '__main__':
    unittest.main()

