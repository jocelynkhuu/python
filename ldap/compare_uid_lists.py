#!/usr/bin/env python3

# Script to check 2 lists from ldap groups 
# Allows taking input from user in format of memberUID: first.lastname

import sys

first_list = []
second_list = []

print("Paste in first ldap list and hit enter then CTRL+D to save.")
first_contents = sys.stdin.readlines()
for item in first_contents:
    uid = item.split()[-1]
    first_list.append(uid)

print("Paste in second ldap list and hit enter then CTRL+D to save.")
second_contents = sys.stdin.readlines()
for item in corp_contents:
    uid = item.split()[-1]
    second_list.append(uid)

missing_second = list(set(first_list).difference(second_list))
missing_first = list(set(second_list).difference(first_list))
matches = list(set(first_list).intersection(second_list))

print("THESE UIDs ARE IN FIRST BUT NOT SECOND:")
print(missing_second)
print("THESE UIDs ARE IN SECOND BUT NOT FIRST:")
print(missing_first)
print("THESE UIDS ARE IN BOTH SECOND AND FIRST:")
print(matches)
