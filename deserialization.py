'''
The code uses pickle module to deserialize dictionary from file
'''
# importing pickle module
import pickle

# Create a dictionary with key-value pairs
dictionary = {"name": "Pawan", "age": 40, "city": "Preston"}

# deserialize data from file
with open('dict.json', 'wb') as file:
    loaded_data = pickle.load(file)

# prints deserialized data
print(loaded_data)