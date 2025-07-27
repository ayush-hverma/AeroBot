import requests
from bs4 import BeautifulSoup
import re

def scrape_website(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript", "footer", "header", "svg"]):
        tag.extract()

    text = soup.get_text(separator="\n")

    # Clean text: remove excessive whitespace and junk
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text
