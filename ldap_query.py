#!/usr/bin/env python3

# Export ldap users as .csv

import csv
import ldap

ldap_server = 'ldaps://corpldapname.com'
base = 'dc=name,dc=com'
rootDN = f'cn=admin,{base}'

con = ldap.initialize(ldap_server)
con.bind_s(rootDN, admin_pass)

def get_all_users():
  result = con.search_s('ou=people,dc=name,dc=com', ldap.SCOPE_ONELEVEL, '(objectClass=posixaccount)', ['cn','mail','uid'])
  return result

data = get_all_users()

with open('ldap_data.csv', 'w') as f:
  all_users = csv.writer(f)
  all_users.writerow(data)
