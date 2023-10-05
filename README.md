# Group Project to create a simple client server network

This is a Project to create a simple Client Server network. Create a dictionary, popluate it, serialise and encrypt it and send it to the server. 
The server will receive the file, decrypt, deserialise it and print the file


## Creating a file

First, we need to initialize the file we are going to work with:
```
dictionary = {"name": "Pawan", "age": 40, "city": "Preston"}
with open('dict.pickle', 'wb') as file:
    pickle.dump(dictionary, file)
```
## File encryption

We can encrypt the file by generating a key first and saving it:
```
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
```
After this, we need to load this key:
```
def load_key():
    return open("key.key", "rb").read()
```
Generating a new key:
```
write_key()
key = load_key()
message = "some secret message".encode()
```
Here we are encrypting the message and printing it out:
```
f = Fernet(key)
encrypted = f.encrypt(message)
print(encrypted)
```

The process of encrypting the file, reading the file data and writing the encrypted file:
```
def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:

        file_data = file.read()


    encrypted_data = f.encrypt(file_data)


    with open(filename, "wb") as file:
        file.write(encrypted_data)
```

## Contributing
Group C end of module assignment
Pull request accepted

## License

No Licence required

