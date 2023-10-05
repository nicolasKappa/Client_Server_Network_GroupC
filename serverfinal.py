import socket
import pickle
from cryptography.fernet import Fernet

def create_server_socket(address, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(1)
    print("Server is listening on {}:{}".format(address, port))
    return server_socket

def accept_connection(server_socket):
    client_socket, client_address = server_socket.accept()
    print("Accepted connection from {}:{}".format(*client_address))
    return client_socket

def load_fernet_key(key_file_path):
    with open(key_file_path, "rb") as key_file:
        key = key_file.read()
    print("Loaded key: ", key)
    return key

def receive_and_decrypt_data(client_socket, key):
    encrypted_data = client_socket.recv(1024)
    print("Received encrypted_data: ", encrypted_data)

    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    print("Decryption successful.")
    return decrypted_data

def deserialize_data(data):
    deserialized_data = pickle.loads(data)
    print("Deserialized data:", deserialized_data)
    return deserialized_data

def save_decrypted_data_to_file(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)
    print("Data saved to file:", file_path)

def send_response(client_socket, response):
    client_socket.send(response.encode('utf-8'))

#def server_logic(
def server_connection(
    server_address='localhost',
    server_port=12345,
    key_file_path='key.key',
    decrypted_data_file_path='decrypted_dict.pickle'
):
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
        print("Decryption failed:", e)
    finally:
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    server_connection()
