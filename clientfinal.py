import socket
import pickle
from cryptography.fernet import Fernet

def create_client_socket():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return client_socket
    except socket.error as e:
        print(f"Socket creation error: {e}")
        return None

def connect_to_server(client_socket, server_address):
    try:
        client_socket.connect(server_address)
    except socket.error as e:
        print(f"Connection error: {e}")
        client_socket.close()

def write_key(key_filename="key.key"):
    try:
        key = Fernet.generate_key()
        with open(key_filename, "wb") as key_file:
            key_file.write(key)
    except Exception as e:
        print(f"Key generation and writing error: {e}")

def load_key(key_filename="key.key"):
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
    try:
        f = Fernet(key)
        encrypted_data = f.encrypt(data)
        return encrypted_data
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

def send_encrypted_data(client_socket, encrypted_data):
    try:
        client_socket.send(encrypted_data)
    except socket.error as e:
        print(f"Data sending error: {e}")

def receive_response(client_socket, buffer_size=1024):
    try:
        response = client_socket.recv(buffer_size)
        return response.decode('utf-8')
    except socket.error as e:
        print(f"Data receiving error: {e}")
        return None

def main():
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

if __name__ == '__main__':
    main()
