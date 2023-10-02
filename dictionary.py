'''
The code creates JSON file for corresponding Key-value paires
written in dictionary
'''
# importing Json module
import json


# Create an empty dictionary
my_dict = {}

# Create a dictionary with key-value pairs
dictionary = {"name": "Pawan", "age": 40, "city": "Preston"}

# convert dictionary to json
json_dict = json.dumps(dictionary)

# print dictionary
print(dictionary)

# Json representation of dictionary
print(json_dict)
