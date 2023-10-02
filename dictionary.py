'''
The code uses pickle module to serialize dictionary and
save it to file in binary format
'''
# importing pickle module
import pickle

# Create a dictionary with key-value pairs
dictionary = {"name": "Pawan", "age": 40, "city": "Preston"}

# creates new file to serialize into pickle
with open('dict.pickle', 'wb') as file:
    pickle.dump(dictionary, file)
