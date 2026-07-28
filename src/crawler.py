import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from pathlib import Path

BASE_URL = "https://www.curopilot.com/"

OUTPUT_FILE = Path("CuroPilot-RAG-Assistant/data/urls.txt")


def is_internal_link(url: str) -> bool:

    parsed = urlparse(url)

    if parsed.netloc == "":
        return True

    return parsed.netloc == urlparse(BASE_URL).netloc


def normalize_url(base: str, link: str) -> str:

    return urljoin(base, link).split("#")[0]


def fetch_page(url: str):

    try:

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        return response.text

    except Exception as e:

        print(f"Failed: {url}")

        print(e)

        return None


def extract_links(html: str, current_url: str):

    soup = BeautifulSoup(html, "html.parser")

    links = set()

    for tag in soup.find_all("a", href=True):

        href = tag["href"]

        if href.startswith("mailto:"):
            continue

        if href.startswith("javascript:"):
            continue

        absolute = normalize_url(current_url, href)

        if is_internal_link(absolute):

            links.add(absolute)

    return links


def crawl(seed_url: str):

    queue = deque()

    queue.append(seed_url)

    visited = set()

    discovered = []

    while queue:

        current_url = queue.popleft()

        if current_url in visited:
            continue

        print(f"Crawling: {current_url}")

        visited.add(current_url)

        discovered.append(current_url)

        html = fetch_page(current_url)

        if html is None:
            continue

        links = extract_links(html, current_url)

        for link in links:

            if link not in visited:

                queue.append(link)

    return discovered


def save_urls(urls):

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        for url in sorted(urls):

            file.write(url + "\n")


def main():

    urls = crawl(BASE_URL)

    save_urls(urls)

    print()

    print(f"Found {len(urls)} pages.")

    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()