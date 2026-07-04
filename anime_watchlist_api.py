#!/usr/bin/env python

# Just a script for some API practice

import requests

print("=" * 50)
print(f"To quit this script, type 'q' when asked to enter an anime title.")
print("=" * 50)

while True:
    search_term = input("Enter an anime title: ").strip()

    if search_term.lower() == "q":
        print("Closing script.")
        break

    if not search_term:
        print("Please enter an anime title to search.")
        continue

    url = f'https://api.jikan.moe/v4/anime' #https://api.jikan.moe/v4/anime?q={search_term}
    query_terms = { 'q': search_term, 'limit' : 5 }
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, params=query_terms, headers=headers)

    if response.status_code == 200:
        anime_info = response.json()

        # print(f"\nHere are the top dict keys we can search for: {list(anime_info.keys())}")
        
        # Tells us the type of data it is: dict or list. If list then need to look in it with [0]
        data_type = type(anime_info['data'])
        
        #print(f"\nThis is the data type: {data_type}")
        #print(f"\nThese are the keys we can search for in 'data': {anime_info['data'][0].keys()}")
        #print(f"\nHere are the search results based on the terms and number of episodes:")
        #if data_type == list: # This line is just to verify the data type is a list
        for anime in anime_info['data']:
            print(f"\nTitle: {anime['title']}")
            print(f"Japanese Title: {anime['title_japanese']}")
            print(f"Number of Episodes: {anime['episodes']}")
            print(f"MyAnimeList ID: {anime['mal_id']}")
            print(f"Aired: {anime['aired']['string']}")
            # print(f"\nTitle: {anime_info['data'][0]['title']}")
            # print(f"Japanese Title: {anime_info['data'][0]['title_japanese']}")
            # print(f"Number of Episodes: {anime_info['data'][0]['episodes']}")
            #print(f"Synopsis : {anime_info['data'][0]['synopsis']}")
        
        add_list = input("\nWould you like to add an anime to your list? (y/n): ")

        if "y" in add_list.lower():
            mal_id_check = input("\nWhat is the MyAnimeList ID? ").strip()
            if mal_id_check:
                matched_anime = None
                for anime in anime_info['data']:
                    if str(anime['mal_id']) == mal_id_check:
                        matched_anime = anime
                        break

                if matched_anime:
                    file_name = "anime_watchlist.txt"
                    with open(file_name, "a") as f:
                        f.write(f"TITLE: {matched_anime['title']}\n -- URL: https://myanimelist.net/anime/{matched_anime['mal_id']}/\n -- MAL_ID: {matched_anime['mal_id']}\n\n")
                        print(f"Added TITLE: {matched_anime['title']} to {file_name}")
                else:
                    print("That MAL ID doesn't exist or cannot be found.")
            else: 
                print("Nothing entered. Try again!")
        # else:
        #     print(f"The data is not a list: {anime_info['data'].keys()}")

    else:
        print(f"Failed with status code: {response.status_code}")
    