#!/usr/bin/env python3

# Script to check 2 lists from prod and corp ldap groups 
# Allows taking input from user in format of memberUID: first.lastname

import os
import sys
import ldap
from getpass import getpass

admin_pass = getpass('Enter admin password: ')
ldap_server = 'ldaps://example.com'
base = 'dc=example,dc=com'
people_base = f'ou=example,{base}'
rootDN = f'cn=user,{base}'

con = ldap.initialize(ldap_server)
con.bind_s(rootDN, admin_pass)

prod_list = []

print("Paste in prod ldap list and hit enter then CTRL+D to save.")
prod_contents = sys.stdin.readlines()
for item in prod_contents:
    uid = item.split()[-1]
    prod_list.append(uid)

print("Comparing prod LDAP to corp LDAP")
full_corp_list = []
corp_list = []

filterstr = 'objectClass=posixaccount'
attrlist = ['uid']
results = con.search_s(people_base, ldap.SCOPE_SUBTREE, filterstr=filterstr, attrlist=attrlist)
for item in results:
    full_corp_list.append(item[1])
for uid in full_corp_list:
    uid = uid.get('uid')
    uid = uid[0].decode('utf-8')
    corp_list.append(uid)

missing_corp = list(set(prod_list).difference(corp_list))
missing_prod = list(set(corp_list).difference(prod_list))
matches = list(set(prod_list).intersection(corp_list))

print("THESE UIDs ARE IN PROD BUT NOT CORP:")
print(missing_corp)
#print("THESE UIDs ARE IN CORP BUT NOT PROD:")
#print(missing_prod)
#print("THESE UIDS ARE IN BOTH CORP AND PROD:")
#print(matches)
