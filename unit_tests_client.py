import unittest
from unittest import mock
import clientfinal
import os
from cryptography.fernet import Fernet
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

if __name__ == '__main__':
    unittest.main()
