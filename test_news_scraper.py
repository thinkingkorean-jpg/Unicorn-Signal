import asyncio
from config import RSS_FEEDS
from scrapers.news import fetch_rss_news

def test_news_scraper():
    print("[TEST] Testing News Scraper...")
    
    # Test keywords
    keywords = ["Generative AI", "Ethereum", "LLM"]
    
    # Select a subset of feeds for testing to make it fast
    test_feeds = [
        RSS_FEEDS['tech'][0], # TechCrunch
        RSS_FEEDS['crypto'][0] # CoinDesk
    ]
    
    print(f"[SEARCH] Parsing feeds: {test_feeds}")
    print(f"[KEY] Keywords: {keywords}")
    
    try:
        results = fetch_rss_news(test_feeds, keywords, days_limit=3)
        
        print(f"\n[OK] Found {len(results)} items:")
        for idx, item in enumerate(results, 1):
            print(f"{idx}. [{item['source']}] {item['title']}")
            print(f"   - {item['link']}")
            print(f"   - {item['published']}")
            print("-" * 50)
            
    except Exception as e:
        print(f"[ERROR] Error during test: {e}")

if __name__ == "__main__":
    test_news_scraper()
