import socket
import pickle
from cryptography.fernet import Fernet

"""
We are using Fernet encryption algorithm 
The Fernet class from the cryptography library.

Fernet is an implementation of authenticated cryptography.
It is a secure way to perform encryption and decryption using a shared secret key.
"""

def create_server_socket(address, port):

    """
    Created a socket server that is open to listening for connections from clients.
    """
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((address, port))
        server_socket.listen(1)
        print("Server is listening on {}:{}".format(address, port))
        return server_socket
    except socket.error as e:
        print("Socket error:", e)
        raise

def accept_connection(server_socket):
    try:
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from {}:{}".format(*client_address))
        return client_socket
    except socket.error as e:
        print("Error accepting connection:", e)
        raise

    """
    accept_connection allows the client to connect and if there is an error prints socket server error message.
    """

def load_fernet_key(key_file_path):
    
    """
    Loads a Fernet Encryption key from a file.

    This function reads the Fernet encryption key from the path set up.

    Args:
    key_file_path (str): The path to the file containing the Fernet encryption key.

    Returns:
    bytes: The Fernet encryption key loaded from the file.

    Raises:
    FileNotFoundError: If the specified file does not exist.

    """

    try:
        with open(key_file_path, "rb") as key_file:
            key = key_file.read()
        print("Loaded key: ", key)
        return key
    except FileNotFoundError as e:
        print("Key file not found:", e)
        raise
    except Exception as e:
        print("Error loading key:", e)
        raise

    
def receive_and_decrypt_data(client_socket, key):
    
    """
    Receive and decrypt encrypted data using a decryption key.

    This function takes encrypted data and a decryption key as input and
    decrypts the data using the Fernet encryption algorithm.
    The decrypted data is returned.

    Args:
        encrypted_data : The encrypted data to be decrypted.
        decryption_key : The Fernet decryption key used for decryption.

    Returns:
        The decrypted data.

    Raises:
        cryptography.fernet.InvalidToken: If the decryption fails due to an
            invalid or expired decryption key.
    """

    try:
        encrypted_data = client_socket.recv(1024)
        print("Received encrypted_data: ", encrypted_data)

        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)
        print("Decryption successful.")
        return decrypted_data
    except Exception as e:
        print("Decryption failed:", e)
        raise

def deserialize_data(data):

    """
    
    Deserialise the serialised data from the client data in an object from Python.
    The function takes the data, from pickle and deserialises it into a Python object.
    
    """
    
    try:
        deserialized_data = pickle.loads(data)
        print("Deserialized data:", deserialized_data)
        return deserialized_data
    except pickle.PickleError as e:
        print("Error deserializing data:", e)
        raise

def save_decrypted_data_to_filec(data, file_path):

    """
    Save decrypted data to a file.

    This function takes decrypted data and saves it to a specified file using pickle. The
    decrypted data is in a text file. We have specified where the file will be saved. 

    Args:
        decrypted_data (bytes or str): The decrypted data to be saved.
        output_file_path (str): The path to the output file where the data will be saved.

    Raises:
        Exception: If an error occurs while saving the data to the file, it is raised.

    Returns:
        Error Statement
    """
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
        #print("Data saved to file:", file_path)
    except Exception as e:
        print("Error saving data to file:", e)
        raise

def send_response(client_socket, response):

    """
    Send a response to a client socket.
    This function sends a response message to a connected client socket

    Args:
        client_socket (socket.socket): The client socket object to which the response will be sent.
        response (str): The response message to send to the client.

    Raise:

        Prints the error message if no response.
    """
    try:
        client_socket.send(response.encode('utf-8'))
    except socket.error as e:
        print("Error sending response:", e)
        raise

    
def server_connection(
    server_address='localhost',
    server_port=12345,
    key_file_path='key.key',
    decrypted_data_file_path='decrypted_dict.pickle'
):
    
    """
    Establish a connection to a remote server.

    This function establishes a network connection to a remote server using
    the specified host and port. It creates a socket and attempts to connect
    to the server.
    """

    server_socket = None
    client_socket = None

    try:
        server_socket = create_server_socket(server_address, server_port)
        client_socket = accept_connection(server_socket)

        key = load_fernet_key(key_file_path)
        decrypted_data = receive_and_decrypt_data(client_socket, key)
        deserialized_data = deserialize_data(decrypted_data)
        save_decrypted_data_to_file(deserialized_data, decrypted_data_file_path)

        #use of input() to prompt use to either save to print the file

        output_option = input("Enter 'print' to print the decrypted data or 'save' to save it to a file: ")

        if output_option == 'print':
            print("Decrypted data:", deserialized_data)
        elif output_option == 'save':
            save_decrypted_data_to_file(deserialized_data, decrypted_data_file_path)
            print("Data saved to file:", decrypted_data_file_path)
            return
        else:
            print("Invalid output option:", output_option)

       
        response = "Received and decrypted data successfully."
        send_response(client_socket, response)
    except Exception as e:
        print("Server error:", e)
    finally:
        if client_socket:
            client_socket.close()
        if server_socket:
            server_socket.close()

if __name__ == "__main__":
    server_connection()
