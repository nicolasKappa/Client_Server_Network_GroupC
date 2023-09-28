'''
The code uses pickle module to deserialize dictionary from file
'''
# importing pickle module
import pickle

# deserialize data from file
with open('dict.pickle', 'rb') as file:
    data = pickle.load(file)

# prints deserialized data
print(data) 