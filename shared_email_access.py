# This script was created to help with generating powershell cmds to add users to shared emails. Cmdlet normally does not take multiple users so each line had to be generated manually.
# With this script, I am able to input in emails and have the output the cmds to copy and paste.

#!/usr/bin/env python3

import re 

username = input("Email that needs access granted to: ")
user = input("User(s) email addresses that need access? ")

emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', user)

for addresses in emails:
    print(f"Add-MailboxFolderPermission -Identity {username}@email.com -User {addresses} -AccessRights Editor -SharingPermissionFlags None")
