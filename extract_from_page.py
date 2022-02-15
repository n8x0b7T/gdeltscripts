import requests

url = "https://www.itespresso.fr/press-release/sectigo-annonce-lvnement-exclusif-du-secteur-de-la-cyberscurit-le-sommet-identity-first-security-2022-de-sectigo"

req_headers = {'User-Agent': 'Mozilla/5.0'}


r = requests.get(url, headers=req_headers)