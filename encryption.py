from cryptography.fernet import Fernet


def write_key():
    """
    Generating a key and saving it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Loading the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()


# generating and writing a new key
write_key()

# loading the previously generated key
key = load_key()

message = "some secret message".encode()

# initializing the Fernet class
f = Fernet(key)

# encrypting the message
encrypted = f.encrypt(message)

# printing how it looks
print(encrypted)


def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()

    # encrypt data
    encrypted_data = f.encrypt(file_data)

    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)