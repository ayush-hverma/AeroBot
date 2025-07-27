from backend.scraper import scrape_website
from backend.vectorstore import build_vector_store

URLS = [
    "https://www.changiairport.com/in/en.html",
    "https://www.jewelchangiairport.com"
]

def main():
    texts = []
    for url in URLS:
        try:
            text = scrape_website(url)
            texts.append(text)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    build_vector_store(texts)

if __name__ == "__main__":
    main()
