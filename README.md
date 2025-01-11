# Group Project to create a simple client server network

This is a Project to create a simple Client Server network. Create a dictionary, popluate it, serialise and encrypt it and send it to the server. 
The server will receive the file, decrypt, deserialise it and print the file


## Creating a file

First, we need to initialize the file we are going to work with:
```python
dictionary = {"name": "Pawan", "age": 40, "city": "Preston"}
with open('dict.pickle', 'wb') as file:
    pickle.dump(dictionary, file)
```
## File encryption

We can encrypt the file by generating a key first and saving it:
```python
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
```
After this, we need to load this key:
```python
def load_key():
    return open("key.key", "rb").read()
```
Generating a new key:
```python
write_key()
key = load_key()
message = "some secret message".encode()
```
Here we are encrypting the message and printing it out:
```python
f = Fernet(key)
encrypted = f.encrypt(message)
print(encrypted)
```

The process of encrypting the file, reading the file data and writing the encrypted file:
```python
def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:

        file_data = file.read()


    encrypted_data = f.encrypt(file_data)


    with open(filename, "wb") as file:
        file.write(encrypted_data)
```

## Error Handling
'create_client_socket_mock' is called once to create a client socket:
```python
create_client_socket_mock = mock.MagicMock()
```
     
'connect_to_server_mock' is called once with the returned value of create_client_socket_mock and the server address ('localhost', 12345) to establish a connection to the server:
```python
connect_to_server_mock = mock.MagicMock()
```

'write_key_mock' is called once to generate a key for the test:
```python
write_key_mock = mock.MagicMock()
```

'load_key_mock' is called once and returns the test key (b"test_key"):
```python
load_key_mock = mock.MagicMock(return_value=b"test_key")
```
    
'encrypt_mock' is called once with any serialized data argument (mock.ANY) and the test key to encrypt the data:
```python
encrypt_mock = mock.MagicMock(return_value=b"encrypted_data")
```

'clientfinal.send_encrypted_data' method is mocked:
```python
clientfinal.encrypt = encrypt_mock
```

'receive_response_mock' is called once and returns the message "Connection successful":
```python
receive_response_mock = mock.MagicMock(return_value="Connection successful")
```

The assertions ensure that the above functions and methods are called with the expected arguments.

'test_receive_and_decrypt_data' executes several tasks:
   - Mocks the socket and other dependencies to simulate receiving encrypted data and decrypting it using a key;
   - Sets up a mock socket (mock_socket), a mock key (mock_key), encrypted and decrypted data;
   - Mocks the recv method of the socket to return the encrypted data;
   - Mocks the Fernet class (from the serverfinal module) to return the decrypted data when decrypt is called;
   - Calls the serverfinal.receive_and_decrypt_data function under test with the mocked objects;

Assertions are made to check if:
     - The result matches the expected decrypted data (self.assertEqual(result, decrypted_data)).
     - The recv method of the socket is called once with the correct argument (mock_socket.recv.assert_called_once_with(1024)).
     - The Fernet class is instantiated once with the mock key (mock_fernet.assert_called_once_with(mock_key)).
     - The decrypt method of the Fernet instance is called once with the encrypted data (mock_fernet.return_value.decrypt.assert_called_once_with(encrypted_data)).

'test_deserialize_data' executes the following tasks:
   - Tests the serverfinal.deserialize_data function to ensure it correctly deserializes the given data and returns a dictionary;
   - Sets up serialized data (serialized_data) and expected data (expected_data);
   - Calls the serverfinal.deserialize_data function with the serialized data;
   - Assertion is made to check if the result matches the expected data (self.assertEqual(result, expected_data)).

Both tests include print statements to indicate when the specific test is being executed and when the test is successful.

These tests ensure that the 'receive_and_decrypt_data' and 'deserialize_data' functions in the 'serverfinal' module are functioning as expected, with the necessary dependencies being invoked and returning the correct results.


## Contributing
Group C end of module assignment
Pull request accepted

## License
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
- This project is licensed under the MIT License.

