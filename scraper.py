import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time

SITES = [
    "https://www.wmfestival.com/call-for-speakers",
    "https://www.makerfairerome.eu/it/call-for-speakers/",
    "https://tedxitaly.com/",
]

KEYWORDS = [
    "call for speakers", "proponi il tuo talk", "partecipa come relatore", 
    "call for papers", "speaker"
]

USER_AGENT = "Mozilla/5.0 (compatible; SpeakerFinder/1.0)"

def scrape_page(url):
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        results = []

        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = (a.get_text() or "").strip()
            full_url = urljoin(url, href)
            combined = (text + " " + full_url).lower()
            if any(k in combined for k in KEYWORDS):
                results.append({
                    "title": text or full_url,
                    "url": full_url,
                    "source": url
                })
        return results
    except Exception as e:
        print(f"Errore su {url}: {e}")
        return []

def main():
    all_events = []
    for site in SITES:
        all_events.extend(scrape_page(site))

    # rimuovi duplicati
    seen = set()
    unique_events = []
    for ev in all_events:
        if ev["url"] not in seen:
            seen.add(ev["url"])
            unique_events.append(ev)

    with open("events.json", "w", encoding="utf-8") as f:
        json.dump(unique_events, f, ensure_ascii=False, indent=2)

    print(f"{len(unique_events)} eventi salvati ({time.strftime('%Y-%m-%d %H:%M')})")

if __name__ == "__main__":
    main()
