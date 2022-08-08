import requests
from my_secrets import imdb_api
from typing import List, Dict

def imdb_search(query: str) -> List[Dict[str, str]]:
    query.replace(' ', '%20')
    r = requests.get(f'https://imdb-api.com/en/API/Search/{imdb_api}/{query}')
    data = r.json()
    options = []
    i = 0
    for title in data['results']:
        if i > 4:
            break

        options.append({"label": f'{title["title"]} {title["description"]}', "value": title["id"]})
        i+=1
    return options
