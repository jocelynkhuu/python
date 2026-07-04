#!/usr/bin/env python

# Just a script for some API practice

import requests

pokemon = input("What pokemon's ability would you like to look up?: ")
url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'

response = requests.get(url)
print(f"\nChecking connection... {response}")

if response.status_code == 200:
    poke_info = response.json()

    print(f"\nHere are the different keys we can look up: \n{poke_info.keys()}") # like looking at this "curl -s "https://pokeapi.co/api/v2/pokemon/ditto" | jq 'keys'"
    data_type = type(poke_info['abilities'])
    print(f"What is the type of data this is : {data_type}")

    print(f"\nNow let's get all the abilities: \n{poke_info['abilities']}")

    print(f"\nPrint me a list of all the {pokemon}'s abilities:\n")
    for ability in poke_info['abilities']:
        print(f" - {ability['ability']['name']}")

    print(f"\nHere are all the games where {pokemon} appears:")
    for index in poke_info['game_indices']:
        print(f" - {index['version']['name']}")
else:
    print(f"Unable to connect with status code: {response.status_code}")