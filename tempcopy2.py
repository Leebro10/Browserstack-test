import requests

url = "https://elpais.com/opinion/2026-07-31/infantino-amenaza-al-futbol-mundial.html"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html",
    "Accept-Language": "es-ES,es;q=0.9",
    "Referer": "https://elpais.com/opinion/",
}

response = requests.get(url, headers=headers)

print(response.status_code)

print(response.text[:500])