import requests


URL = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"

HEADERS = {
    "x-rapidapi-key": "e90f86c0a3msh11a87df2d00efaap12e82fjsndf07f4b79923",
    "x-rapidapi-host": "google-translate113.p.rapidapi.com",
    "Content-Type": "application/json",
}


def translate_text(text):
    """
    Translate Spanish text to English.
    """

    payload = {
        "from": "auto",
        "to": "en",
        "text": text,
    }

    try:

        response = requests.post(
            URL,
            json=payload,
            headers=HEADERS,
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        return data["trans"]

    except requests.RequestException as e:

        print(f"Translation failed: {e}")

        return text