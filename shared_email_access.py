#!/usr/bin/python3

import re 

username = input("Email that needs access granted to: ")
user = input("User(s) email addresses that need access? ")

emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', user)

for addresses in emails:
    print(f"Add-MailboxFolderPermission -Identity {username}:\calendar -User {addresses} -AccessRights Editor -SharingPermissionFlags None")
