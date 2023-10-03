import socket
from cryptography.fernet import Fernet

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print("Server is listening on {}:{}".format(*server_address))

# Accept a connection
client_socket, client_address = server_socket.accept()
print("Accepted connection from {}:{}".format(*client_address))

try:
    # Load the Fernet key
    key = open("key.key", "rb").read()
    print("Loaded key: ", key)

    # Receive data from the client
    encrypted_data = client_socket.recv(1024)
    print("Received encrypted_data: ", encrypted_data)

    # Decrypt the data using the key
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    print("Decryption successful.")

    # Print the decrypted data
    #print("Decrypted data:", decrypted_data.decode('utf-8'))
    print("Decrypted data as bytes:", decrypted_data)

    # Save the decrypted data to a file
    with open('decrypted_dict.pickle', 'wb') as file:
        file.write(decrypted_data)

    print("Received and decrypted data successfully.")

    # Send a response back to the client
    response = "Received and decrypted data successfully."
    client_socket.send(response.encode('utf-8'))

except Exception as e:
    print("Decryption failed:", e)

finally:
    # Clean up the connection
    client_socket.close()
    server_socket.close()
