#!/usr/bin/env python3

# This script was just practice to generate a script using default write commands to generate plist files

import os

### VARIABLES
HOME = os.path.expanduser('~')
DOWNLOADS = f"{HOME}/Downloads"
plist_script = f"{DOWNLOADS}/create_plist.sh"

nameofplist = str(input("What is the name of the plist? "))
numberofKeys = int(input("How many keys are you creating? "))
print("")

if os.path.isfile(plist_script):
    os.remove(plist_script)
    with open(plist_script, "a") as file:
        file.write("#!/bin/bash\n\n")
else:
    with open(plist_script, "a") as file:
        file.write("#!/bin/bash\n\n")

for i in range(numberofKeys):
    nameofKey = str(input("What is the name of the key? "))
    typeofKey = str(input("What is the type of key? (ex. -bool, -string): "))
    valueofKey = str(input("What is the value of the key? "))
    print("")

    cmd = f"defaults write {DOWNLOADS}/{nameofplist} {nameofKey} {typeofKey} {valueofKey}\n"
    
    with open(plist_script,"a") as file:
        file.write(cmd)

if os.path.isfile(plist_script):
    os.chmod(plist_script, 0o755)
