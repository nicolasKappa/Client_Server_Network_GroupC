import socket
import pickle
from cryptography.fernet import Fernet

def create_server_socket(address, port):
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

def load_fernet_key(key_file_path):
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
    try:
        deserialized_data = pickle.loads(data)
        print("Deserialized data:", deserialized_data)
        return deserialized_data
    except pickle.PickleError as e:
        print("Error deserializing data:", e)
        raise

def save_decrypted_data_to_file(data, file_path):
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
        print("Data saved to file:", file_path)
    except Exception as e:
        print("Error saving data to file:", e)
        raise

def send_response(client_socket, response):
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
    server_socket = None
    client_socket = None

    try:
        server_socket = create_server_socket(server_address, server_port)
        client_socket = accept_connection(server_socket)

        key = load_fernet_key(key_file_path)
        decrypted_data = receive_and_decrypt_data(client_socket, key)
        deserialized_data = deserialize_data(decrypted_data)
        save_decrypted_data_to_file(deserialized_data, decrypted_data_file_path)

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
