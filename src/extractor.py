import re
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

URLS_FILE = Path("data/urls.txt")
OUTPUT_DIR = Path("data/extracted")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    )
}

def read_urls():

    if not URLS_FILE.exists():
        raise FileNotFoundError(f"{URLS_FILE} not found.")

    with open(URLS_FILE, "r", encoding="utf-8") as file:
        urls = [line.strip() for line in file if line.strip()]

    return urls

def fetch_page(url):
    #Download HTML content of a webpage

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        return response.text

    except Exception as e:
        print(f"Failed to fetch {url}")
        print(e)
        return None
    

def extract_visible_text(html):
    #Extracting readable text from HTML

    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags
    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "img",
        "iframe",
        "footer"
    ]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    return text


def clean_text(text):
    # Clean extracted text

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n{2,}", "\n\n", text)

    return text.strip()


def url_to_filename(url):
    """
    Convert URL to filename.

    https://www.curopilot.com/
        -> home.txt

    https://www.curopilot.com/about
        -> about.txt
    """

    parsed = urlparse(url)

    path = parsed.path.strip("/")

    if path == "":
        return "home.txt"

    filename = path.replace("/", "_")

    return f"{filename}.txt"


def save_document(filename, text):
    #Save extracted text

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filepath = OUTPUT_DIR / filename

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(text)


def main():

    urls = read_urls()

    print(f"\nFound {len(urls)} URLs\n")

    for url in urls:

        print(f"Downloading: {url}")

        html = fetch_page(url)

        if html is None:
            continue

        text = extract_visible_text(html)

        text = clean_text(text)

        filename = url_to_filename(url)

        save_document(filename, text)

        print(f"Saved -> {filename}\n")

    print("Extraction Completed")


if __name__ == "__main__":
    main()