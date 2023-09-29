import socket 

#local server details

server_address=("127.0.0.1",12345)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(server_address)

# file to send
file_name = "dicitionary.py"  #json file script

try:
    # Open file in read me file
    with open(file_name, "rb") as file:
        
        chunk = file.read(1024)
        while chunk:     #chunk is parts of the file
            # Send the chunk to the socketserver
            client_socket.send(chunk)
            chunk = file.read(1024)
    print(f"Python script '{file_name}' sent successfully.")
except FileNotFoundError:
    print(f"Python script '{file_name}' not found.")

# Close the socket
client_socket.close()