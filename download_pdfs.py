#!/usr/bin/env python3

# Quick script to download chapter pdfs of publicly available books

import requests

for i in range (1,31): # 30 chapters 
    r = requests.get(f'https://link/to/pdfs/{i:02d}.pdf') # chapters are named the the same but numbered differently
    file = open(f"~/Downloads/name/of/pdf/{i:02d}.pdf", 'wb')
    file.write(r.content)
    file.close()
