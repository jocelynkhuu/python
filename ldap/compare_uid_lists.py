#!/usr/bin/env python3

# Script to check 2 lists from 2 different ldap groups 
# Allows taking input from user in format of memberUID: first.lastname

import os
import sys
import ldap
from getpass import getpass

password = getpass('Enter password: ')
ldap_server = 'ldaps://example.com'
base = 'dc=example,dc=com'
people_base = f'ou=example,{base}'
rootDN = f'cn=user,{base}'

con = ldap.initialize(ldap_server)
con.bind_s(rootDN, password)

second_list = []

print("Paste in first ldap list and hit enter then CTRL+D to save.")
second_contents = sys.stdin.readlines()
for item in second_contents:
    uid = item.split()[-1]
    second_list.append(uid)

print("Comparing first LDAP to second LDAP group")
full_first_list = []
first_list = []

filterstr = 'objectClass=posixaccount'
attrlist = ['uid']
results = con.search_s(people_base, ldap.SCOPE_SUBTREE, filterstr=filterstr, attrlist=attrlist)
for item in results:
    full_first_list.append(item[1])
for uid in full_first_list:
    uid = uid.get('uid')
    uid = uid[0].decode('utf-8')
    first.append(uid)

missing_first = list(set(second_list).difference(first_list))
missing_second = list(set(first_list).difference(second_list))
matches = list(set(second_list).intersection(first_list))

print("THESE UIDs ARE IN SECOND BUT NOT FIRST:")
print(missing_first)
#print("THESE UIDs ARE IN FIRST BUT NOT SECOND:")
#print(missing_SECOND)
#print("THESE UIDS ARE IN BOTH FIRST AND SECOND:")
#print(matches)
