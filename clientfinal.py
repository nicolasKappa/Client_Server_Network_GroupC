import socket
import pickle
from cryptography.fernet import Fernet
import sys

def create_client_socket():
    """Create and return a socket object for the client. 
        Created fucntion for socket to enable unit testing using magic mock
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client_socket

def connect_to_server(client_socket, server_address):
    """
    Connect to the server using the provided socket and server address.
    Created fucntion for socket to enable unit testing using magic mock

    """
    client_socket.connect(server_address)

   # server_address = ('localhost', 12345)
   # client_socket.connect(server_address)

def write_key():
    """
    Generate a cryptographic key and save it to a file.

    This function generates a Fernet key and saves it to a file named 'key.key' in binary format.
    Generating a key and saving it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def write_key(key_filename="key.key"):
    """
    Generate a cryptographic key and save it to a file.
    This function generates a Fernet key and saves it to a specified file in binary format.
    """
    key = Fernet.generate_key()
    with open(key_filename, "wb") as key_file:
        key_file.write(key)
   #return open("key.key", "rb").read()

# Generate and write a new key
#write_key()

# Load the previously generated key and print it
#key = load_key()
#print(f"Fernet Key: {key.hex()}")
#write_key()

def load_key(key_filename="key.key"):
    """
    Load the cryptographic key from the specified file.

    Returns:
        bytes: The Fernet key loaded from the file.
    """
    return open(key_filename, "rb").read()

def encrypt(data, key):
    """
    Encrypt data using a Fernet key.

    Args:
        data (bytes): The data to be encrypted.
        key (bytes): The Fernet key used for encryption.

    Returns:
            bytes: The encrypted data.
    """
    f = Fernet(key)
    encrypted_data = f.encrypt(data)
    return encrypted_data

def send_encrypted_data(client_socket, encrypted_data):
    """
    Send encrypted data to the server using the provided socket.

    Args:
        client_socket (socket.socket): The client socket object.
        encrypted_data (bytes): The encrypted data to send
    """

    client_socket.send(encrypted_data)

def receive_response(client_socket, buffer_size=1024):
    """
    Receive a response from the server using the provided socket.

    Args:
        client_socket (socket.socket): The client socket object.
        buffer_size (int): The size of the buffer for receiving data.

    Returns:
        str: The received response as a string.
    """
    response = client_socket.recv(buffer_size)
    return response.decode('utf-8')

def main():
    try:
        client_socket = create_client_socket()

        server_address = ('localhost', 12345)
        connect_to_server(client_socket, server_address)

        # Generate and write a new key
        write_key()

        # Load the previously generated key
        key = load_key()

    # Add a new dictionary
        dictionary = {"name": "Pawan", "age": 40, "city": "Preston"}

    # Create a file to serialise into pickle
        with open('dict.pickle', 'wb') as file:
            pickle.dump(dictionary, file)

    # Read the serialized data from the file
        with open('dict.pickle', 'rb') as file:
            serialised_data = file.read()

    # Encrypt the serialized data
        encrypted_data = encrypt(serialised_data, key)

    # Send encrypted data to the server
        client_socket.send(encrypted_data)
    
    # Send encrypted data to the server
        send_encrypted_data(client_socket, encrypted_data)

    # Receive a response from the server
        response = receive_response(client_socket)
        print(f"Message from server: {response}")
        #response = client_socket.recv(1024)
        #print(f"Message from server: {response.decode('utf-8')}")

    except Exception as e:
        """
        try-except block to handle excpetion and print error message
        """
        print(f"An error occurred: {e}")
    #sys.exit(1)

    finally:
    # Clean up the connection
        client_socket.close()
        
if __name__ == '__main__':
    main()