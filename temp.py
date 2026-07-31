import requests

url = "https://elpais.com/opinion/2026-07-31/desafio-humanitario-y-diplomatico.html"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/138.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text[:500])