#!/usr/bin/env python3

# Quick script to download chapter pdfs of publicly available books

import requests

for i in range (1,28):
    file_name = f"{i:02d}.pdf"

    print(f"Downloading {file_name}")
    r = requests.get(f"https://link/to/pdf/here/{i:02d}.pdf")

    if r.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(r.content)
    else:
        print(f"Errored with status code: {r.status_code}")
