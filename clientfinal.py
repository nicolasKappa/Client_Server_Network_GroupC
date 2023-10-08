
"""
This script establishes a TCP connection with a server, generates and shares a Fernet encryption key, 
encrypts and sends data to the server, and receives and prints a response.

"""

# import necessary modules
import socket
import pickle
from cryptography.fernet import Fernet

def create_client_socket():
    
    """
    Create a client socket.

    Returns:
        socket.socket or None: The created client socket, or None if there is an error creating the socket.

    Raises:
        socket.error: If there's an error creating the socket.
    """
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return client_socket
    except socket.error as e:
        print(f"Socket creation error: {e}")
        return None

def connect_to_server(client_socket, server_address):
    
    """
    Connect the client socket to the specified server address.

    Args:
        client_socket : The client socket to connect.
        server_address : Containing the server's address (IP, port).

    Raises:
        socket.error: If there's an error connecting to the server.
    """
    
    try:
        client_socket.connect(server_address)
    except socket.error as e:
        print(f"Connection error: {e}")
        client_socket.close()

def write_key(key_filename="key.key"):
    
    """
    Generate a Fernet key and write it to a file.

    Args:
        key_filename : The filename to save the key. Default is "key.key".

    Raises:
        Exception: If there's an error generating or writing the key.
    """
 
    try:
        key = Fernet.generate_key()
        with open(key_filename, "wb") as key_file:
            key_file.write(key)
    except Exception as e:
        print(f"Key generation and writing error: {e}")

def load_key(key_filename="key.key"):
    
    """
    Load a Fernet key from a file.

    Args:
        key_filename : The filename from which to load the key. Default is "key.key".

    Returns:
        bytes or None: The loaded Fernet key, or None if there is an error loading the key.

    Raises:
        FileNotFoundError: If the key file is not found.
        Exception: If there's an error loading the key.
    """
    
    try:
        key = open(key_filename, "rb").read()
        return key
    except FileNotFoundError:
        print(f"Key file '{key_filename}' not found.")
        return None
    except Exception as e:
        print(f"Key loading error: {e}")
        return None

def encrypt(data, key):
   
    """
    Encrypt data using a Fernet key.

    Args:
        data : The data to be encrypted.
        key : The Fernet key.

    Returns:
        bytes or None: The encrypted data, or None if there is an error during encryption.

    Raises:
        Exception: If there's an error during encryption.
    """
    
    try:
        f = Fernet(key)
        encrypted_data = f.encrypt(data)
        return encrypted_data
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

def send_encrypted_data(client_socket, encrypted_data):
    """
    Sends the given encrypted data to the client socket.
        Args:
            client_socket: A TCP client socket object.
            encrypted_data: The encrypted data to send.
        Returns:
            `None` if there was an error sending the data.
    """
    try:
        client_socket.send(encrypted_data)
    except socket.error as e:
        print(f"Data sending error: {e}")

def receive_response(client_socket, buffer_size=1024):
    
    """
    Receive a response from the server.

    Args:
        client_socket : The client socket.
        buffer_size : The size of the buffer for receiving data. Default is 1024.

    Returns:
        str or None: The received response as a string, or None if there is an error receiving data.

    Raises:
        socket.error: If there's an error receiving data.
    """
    
    try:
        response = client_socket.recv(buffer_size)
        return response.decode('utf-8')
    except socket.error as e:
        print(f"Data receiving error: {e}")
        return None

def main():

    """
    Main function for client-side communication with the server.

    This function performs the following steps:
    1. Creates a client socket.
    2. Connects to the server at the specified address.
    3. Generates and writes a Fernet key to a file.
    4. Loads the Fernet key.
    5. Creates a dictionary, serializes it, and encrypts the data.
    6. Sends the encrypted data to the server.
    7. Receives and prints a response from the server.

    If any error occurs during these steps, it will be caught and an error message will be printed.

    Returns:
        None
    """

    try:
        client_socket = create_client_socket()
        if client_socket is None:
            return

        server_address = ('localhost', 12345)
        connect_to_server(client_socket, server_address)

        write_key()

        key = load_key()
        if key is None:
            return

        dictionary = {"name": "Pawan", "age": 40, "city": "Preston"}

        with open('dict.pickle', 'wb') as file:
            pickle.dump(dictionary, file)

        with open('dict.pickle', 'rb') as file:
            serialised_data = file.read()

        encrypted_data = encrypt(serialised_data, key)
        if encrypted_data is None:
            return

        send_encrypted_data(client_socket, encrypted_data)

        response = receive_response(client_socket)
        if response is not None:
            print(f"Message from server: {response}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if client_socket is not None:
            client_socket.close()

# call main function if script if code is executed directly
if __name__ == '__main__':
    main()
