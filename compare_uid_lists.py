#!/usr/bin/env python3

# Script to check 2 lists from prod and corp ldap groups 
# Allows taking input from user in format of memberUID: first.lastname

import sys
import subprocess

base = 'dc=example,dc=com'
user_dn = f'cn=user,{base}'
corp_ldap_server = 'ldaps://example.network'

prod_list = []

# List is pasted here as an example for if you don't have access to prod ldap and get a list from someone else
print("Paste in prod ldap list and hit enter then CTRL+D to save.")
prod_contents = sys.stdin.readlines()
for item in prod_contents:
    uid = item.split()[-1]
    prod_list.append(uid)

# If you have access to corp ldap then can connect directly using creds to pull list of uids
print("Enter in admin password to pull corp ldap list")
corp_users = subprocess.check_output(f"ldapsearch -LLL -xD {user_dn} -b {base} -H {corp_ldap_server} -W '(uid=*)' uid | grep -v '^dn: ' | sed 's/uid: //g' | sort", shell=True)
corp_decode = corp_users.decode('utf-8')
corp_list = corp_decode.splitlines()

missing_corp = list(set(prod_list).difference(corp_list))
missing_prod = list(set(corp_list).difference(prod_list))
matches = list(set(prod_list).intersection(corp_list))

print("THESE UIDs ARE IN PROD BUT NOT CORP:")
print(missing_corp)
#print("THESE UIDs ARE IN CORP BUT NOT PROD:")
#print(missing_prod)
#print("THESE UIDS ARE IN BOTH CORP AND PROD:")
#print(matches)
