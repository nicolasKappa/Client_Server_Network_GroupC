import socket
import pickle
from cryptography.fernet import Fernet

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server address and port
server_address = ('localhost', 12345)

# Connect to the server
client_socket.connect(server_address)

def write_key():
    """
    Generate a cryptographic key and save it to a file.

    This function generates a Fernet key and saves it to a file named 'key.key' in binary format.
    Generating a key and saving it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Load the cryptographic key from the 'key.key' file.

    Returns:
        bytes: The Fernet key loaded from the 'key.key' file.
    Loading the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()

# Generate and write a new key
write_key()

# Load the previously generated key
key = load_key()
#print(f"Fernet Key: {key.hex()}")

# Call the print_key function to print the key
load_key()
#write_key()

try:
    # Add a new dictionary
    dictionary = {"name": "Pawan", "age": 40, "city": "Preston"}

    # Create a file to serialize into pickle
    with open('dict.pickle', 'wb') as file:
        pickle.dump(dictionary, file)

    # Read the serialized data from the file
    with open('dict.pickle', 'rb') as file:
        serialised_data = file.read()

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

    # Encrypt the serialized data
    encrypted_data = encrypt(serialised_data, key)

    # Send encrypted data to the server
    client_socket.send(encrypted_data)

    # Receive a response from the server
    response = client_socket.recv(1024)
    print(f"Message from server: {response.decode('utf-8')}")

except Exception as e:
    """
    try-except block to handle excpetion and print error message
    """
    print(f"An error occurred: {e}")
    sys.exit(1)

finally:
    # Clean up the connection
    client_socket.close()
