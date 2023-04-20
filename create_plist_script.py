#!/usr/bin/env python3

import os
import plistlib 

# Take input and generate a plist stored in ~/Downloads

### VARIABLES
HOME = os.path.expanduser('~')
DOWNLOADS = f"{HOME}/Downloads"

dict = {}

nameofplist = str(input("What is the name of the plist? "))
numberofKeys = int(input("How many keys are you creating? "))
print("")

plist_script = f"{DOWNLOADS}/{nameofplist}"

for i in range(numberofKeys):
    key_name = input("What is the name of the key? ")
    key_value = input("What is the value of the key? ")

    if key_value == "true" or key_value == "True" or key_value == '1':
        dict[key_name.title()] = bool(True)
    elif key_value == "false" or key_value == "False" or key_value == '0':
        dict[key_name.title()] = bool(False)
    elif key_name == "ProgramArguments":
        splitList = key_value.split()
        dict[key_name.title()] = splitList
    elif key_value.isdigit() and (key_value != 1 or key_value != 0):
        dict[key_name.title()] = int(key_value) 
    else:
        dict[key_name.title()] = key_value

print(plistlib.dumps(dict).decode())
# file = open(plist_script,"wb")
# plistlib.dump(dict, file)
# file.close()

# with open(plist_script, 'rb') as file:
#     plist = plistlib.load(file)
#     print(plist)
