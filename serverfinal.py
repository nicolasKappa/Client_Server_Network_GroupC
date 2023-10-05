import socket
import pickle
from cryptography.fernet import Fernet


def create_server_socket(address, port):    
# Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a specific address and port
#server_address = ('localhost', 12345)
    server_socket.bind((address, port))
# Listen for incoming connections
    server_socket.listen(1)
    print("Server is listening on {}:{}".format(address, port))
    return server_socket

def accept_connection(server_socket):
# Accept a connection
    client_socket, client_address = server_socket.accept()
    print("Accepted connection from {}:{}".format(*client_address))
    return client_socket

def load_fernet_key(key_file_path):
    # Load the Fernet key
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    print("Loaded key: ", key)
    return key

def receive_and_decrypt_data(client_socket, key):
    # Receive data from the client
    encrypted_data = client_socket.recv(1024)
    print("Received encrypted_data: ", encrypted_data)

    # Decrypt the data using the key
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    print("Decryption successful.")
    return decrypted_data

def deserialize_data(data):

    # Print the decrypted data
    #print("Decrypted data:", decrypted_data.decode('utf-8'))
    #print("Decrypted data as bytes:", decrypted_data)

    # Deserialize the decrypted data using pickle
    deserialized_data = pickle.loads(data)
    # Print the deserialized data
    print("Deserialized data:", deserialized_data)
    return deserialize_data

def save_decrypted_data_to_file(data, file_path):
    # Save the decrypted data to a file
    #with open('decrypted_dict.pickle', 'wb') as file:
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)
    print("Data saved to file:", file_path)

def send_response(client_socket, response):
    client_socket.send(response.encode('utf-8'))

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

   # Send a response back to the client
        response = "Received and decrypted data successfully."
        send_response(client_socket, response)
        #client_socket.send(response.encode('utf-8'))

    except Exception as e:
        print("Decryption failed:", e)

    finally:
    # Clean up the connection
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    server_connection()