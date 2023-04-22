#!/usr/bin/env python3

import os
import re
import plistlib
import argparse
import sys

# Argparse practice of plist script

### VARIABLES
HOME = os.path.expanduser('~')
DOWNLOADS = f"{HOME}/Downloads"

dict = {}

parser = argparse.ArgumentParser(prog="Plist scripter", description="Script to create a Plist")
parser.add_argument('-f', '--file', metavar='', required=True, help='File to create')
parser.add_argument('-k', '--key', metavar='', required=True, help='key value for plist')
parser.add_argument('-v', '--value', metavar='', required=True, help='value of key')

try:
    args = parser.parse_args()
except:
    sys.exit()

plist_name = args.file
key_name = args.key
key_value = args.value

plist_script = f"{DOWNLOADS}/{plist_name}.plist"

if key_value == "true" or key_value == "True" or key_value == '1':
    dict[key_name.title()] = bool(True)
elif key_value == "false" or key_value == "False" or key_value == '0':
    dict[key_name.title()] = bool(False)
elif re.search("/", key_value) and key_name == "ProgramArguments":
    splitList = key_value.split()
    dict[key_name.title()] = splitList
elif key_value.isdigit() and (key_value != 1 or key_value != 0):
    dict[key_name.title()] = int(key_value) 
else:
    dict[key_name.title()] = key_value

file = open(plist_script,"wb")
plistlib.dump(dict, file, sort_keys=None)
file.close()

with open(plist_script, 'rb') as file:
    plist = plistlib.load(file)
    print(plist)
