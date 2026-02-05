from scrapers.youtube import fetch_youtube_videos

def test_youtube_scraper():
    print("[TEST] Testing YouTube Scraper...")
    
    keywords = ["Generative AI", "Cursor AI Code Editor"]
    
    try:
        results = fetch_youtube_videos(keywords, limit=2)
        
        print(f"\n[OK] Found {len(results)} videos:")
        for idx, item in enumerate(results, 1):
            # 윈도우 콘솔 인코딩 문제 방지를 위한 safe print
            safe_title = item['title'].encode('ascii', 'ignore').decode('ascii')
            safe_link = item['link'].encode('ascii', 'ignore').decode('ascii')
            print(f"{idx}. [{item['source']}] {safe_title}")
            print(f"   - {safe_link}")
            print(f"   - Summary Length: {len(item['summary'])}")
            print("-" * 50)
            
    except Exception as e:
        print(f"[ERROR] Error during test: {e}")

if __name__ == "__main__":
    test_youtube_scraper()
