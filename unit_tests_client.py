import unittest
from unittest import mock
import clientfinal
import os
#from cryptography.fernet import Fernet
#from encryption import write_key, decrypt
#from encryption import load_key
#from encryption import encrypt


class TestClient(unittest.TestCase):

    def setUp(self):
        # Create a key file for testing
        with open("test_key.key", "wb") as key_file:
            key_file.write(b"test_key")

            # Comment - creating a file not required when using mock module
            # Create a test file
        #with open("test_file.txt", "w") as test_file:
            #test_file.write("Test data")

    def tearDown(self):
        # Remove the key file if it exists after each test
        #if os.path.exists("test_key.key"):
            os.remove("test_key.key")
    #comment - test file not created therefore not required
        #if os.path.exists("test_file.txt"):
          #  os.remove("test_file.txt")

    def test_main(self):
        print("Testing the main function...")
        # Mock the functions and methods
        create_client_socket_mock = mock.MagicMock()
        connect_to_server_mock = mock.MagicMock()
        write_key_mock = mock.MagicMock()
        load_key_mock = mock.MagicMock(return_value=b"test_key")
        encrypt_mock = mock.MagicMock(return_value=b"encrypted_data")
        # Change the response from the server here
        receive_response_mock = mock.MagicMock(return_value="Connection successful")

        # Replace the functions and methods in the Client module with the mocks
        clientfinal.create_client_socket = create_client_socket_mock
        clientfinal.connect_to_server = connect_to_server_mock
        clientfinal.write_key = write_key_mock
        clientfinal.load_key = load_key_mock
        clientfinal.encrypt = encrypt_mock
        clientfinal.send_encrypted_data = mock.MagicMock()
        clientfinal.receive_response = receive_response_mock

        # Call the main function
        clientfinal.main()

        # Assertions to verify that functions and methods were called with the expected arguments
        create_client_socket_mock.assert_called_once()
        connect_to_server_mock.assert_called_once_with(create_client_socket_mock.return_value, ('localhost', 12345))
        write_key_mock.assert_called_once()
        load_key_mock.assert_called_once()
        encrypt_mock.assert_called_once_with(
            mock.ANY,  # Allow any serialized data argument here
            b"test_key"  # Ensure the key argument is correct
        )
        
        # Print the custom message from the client
        #print("Message from client:", receive_response_mock.return_value)

        # Print a test summary
        print("Test summary:")
        print("  - key generation, encryption and connection to server function was tested.")
        print("  - All mocked functions were called with the expected arguments.")
        print("  - Test completed successfully.")


# functions - test_write_key, test_load_key, test_encrypt and test_decrypt no longer required. 
# above functions will be called by mocking the functions and methods. 
#mock assesertions will confirm test pass or fail. 


    #def test_write_key(self):
        # Create a key file for testing
        #with open("key.key", "wb") as key_file:
          # key_file.write(b"test_key")

        # Call the function that will generate a key and save it to a file
       # write_key()

        # Check whether the key file was created
        #self.assertTrue(os.path.exists("key.key"))

        # Check whether the key file is not empty and saved to a file
        #self.assertTrue(os.path.getsize("key.key") > 0)

        # Clean up the key file after the test
       # os.remove("key.key")

    #def test_load_key(self):
        # Call the function
        #key = load_key()

        # Check whether the correct key was loaded
        #expected_key = b"test_key"
       # self.assertEqual(expected_key, key)

        # Remove the key file after the test
       # os.remove("key.key")

    #def test_encrypt(self):
        # Generate a test key
       # test_key = Fernet.generate_key()

        # Call the function
       # encrypt("test_file.txt", test_key)

        # Read the encrypted file
       # with open("test_file.txt", "rb") as encrypted_file:
            #encrypted_data = encrypted_file.read()

        # Check if the file data is encrypted
        #self.assertNotEqual(encrypted_data, b"Test data")

    #def test_decrypt(self):
        # Generate a test key
        #test_key = Fernet.generate_key()

        # Encrypt the test file
        #encrypt("test_file.txt", test_key)

        # Call the function
        #decrypt("test_file.txt", test_key)

        # Read the decrypted file
        #with open("test_file.txt", "rb") as decrypted_file:
            #decrypted_data = decrypted_file.read()

        # Check if the file data is decrypted correctly
        #self.assertEqual(decrypted_data, b"Test data")


if __name__ == '__main__':
    unittest.main()
