
import json
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

SITEMAP_URL = (
    "https://support.brilliantdirectories.com/support/sitemap.xml"
)
ALLOWED_HOST = "support.brilliantdirectories.com"
DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "articles.jsonl"
PROGRESS_FILE = DATA_DIR / "processed_urls.txt"


def get_sitemap_urls(client: httpx.Client) -> list[str]:
    """Read page URLs from a standard XML sitemap."""
    response = client.get(SITEMAP_URL)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    urls = []

    for element in root.iter():
        if element.tag.endswith("loc") and element.text:
            url = element.text.strip()
            parsed = urlparse(url)

            if parsed.scheme == "https" and parsed.hostname == ALLOWED_HOST:
                urls.append(url)

    return list(dict.fromkeys(urls))


def extract_article(client: httpx.Client, url: str) -> dict:
    """Extract basic article text and image metadata."""
    response = client.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    main = soup.find("main") or soup.find("article") or soup.body

    if main is None:
        main_text = ""
        images = []
    else:
        main_text = main.get_text(" ", strip=True)
        images = [
            {
                "url": image.get("src"),
                "alt": image.get("alt", ""),
            }
            for image in main.find_all("img")
            if image.get("src")
        ]

    return {
        "url": url,
        "title": title,
        "content": main_text,
        "images": images,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


def crawl(max_pages: int = 10, delay_seconds: float = 1.0) -> dict:
    """Crawl a limited number of URLs, recording progress and errors."""
    if max_pages < 1:
        raise ValueError("max_pages must be at least 1")
    if delay_seconds < 0:
        raise ValueError("delay_seconds cannot be negative")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    processed = set()
    if PROGRESS_FILE.exists():
        processed = set(
            PROGRESS_FILE.read_text(encoding="utf-8").splitlines()
        )

    succeeded = 0
    failed = 0

    with httpx.Client(
        timeout=20.0,
        follow_redirects=True,
        headers={"User-Agent": "AI-Tech-Consultant-Student-Project/1.0"},
    ) as client:
        urls = get_sitemap_urls(client)
        pending = [url for url in urls if url not in processed][:max_pages]

        for url in pending:
            article = None

            for attempt in range(3):
                try:
                    article = extract_article(client, url)
                    break
                except (httpx.HTTPError, ValueError):
                    if attempt < 2:
                        time.sleep(2 ** attempt)

            if article is not None:
                with OUTPUT_FILE.open("a", encoding="utf-8") as file:
                    file.write(json.dumps(article, ensure_ascii=False) + "\n")
                succeeded += 1
            else:
                failed += 1

            # Record each attempted URL so a successful URL is not
            # fetched again on the next run.
            with PROGRESS_FILE.open("a", encoding="utf-8") as file:
                file.write(url + "\n")
            processed.add(url)

            if url != pending[-1]:
                time.sleep(delay_seconds)

    return {
        "discovered_urls": len(urls),
        "attempted": succeeded + failed,
        "succeeded": succeeded,
        "failed": failed,
    }
