#!/usr/bin/env python3

# Script to check 2 lists of ldap uids
# Takes multiline input from user

import sys

prod_list = []
corp_list = []

print("Paste in prod ldap list and hit enter then CTRL+D to save.")
prod_contents = sys.stdin.readlines()
for item in prod_contents:
    uid = item.split()[-1]
    prod_list.append(uid)

print("Paste in corp ldap list and hit enter then CTRL+D to save.")
corp_contents = sys.stdin.readlines()
for item in corp_contents:
    uid = item.split()[-1]
    corp_list.append(uid)

missing_corp = list(set(prod_list).difference(corp_list))
missing_prod = list(set(corp_list).difference(prod_list))
matches = list(set(prod_list).intersection(corp_list))

print("THESE UIDs ARE IN PROD BUT NOT CORP:")
print(missing_corp)
print("THESE UIDs ARE IN CORP BUT NOT PROD:")
print(missing_prod)
print("THESE UIDS ARE IN BOTH CORP AND PROD:")
print(matches)
