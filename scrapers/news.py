import feedparser
from datetime import datetime, timedelta
import ssl

# SSL 인증 우회 (로컬 개발용)
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def fetch_rss_news(feeds, keywords, days_limit=7):
    """
    RSS 피드에서 키워드와 연관된 최신 뉴스를 가져옵니다.
    """
    news_items = []
    seen_links = set()
    
    # 날짜 제한 계산
    date_cutoff = datetime.now() - timedelta(days=days_limit)
    
    print(f"[SEARCH] Scraping {len(feeds)} feeds for keywords: {keywords}")

    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries:
                # 이미 본 링크면 스킵
                if entry.link in seen_links:
                    continue
                
                # 날짜 필터링 (published_parsed 사용)
                published_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published_date = datetime(*entry.updated_parsed[:6])
                
                # 날짜가 파싱되었고, 제한보다 오래된 경우에만 스킵 (날짜 파싱 실패하면 가져오도록 변경 - 최신순 정렬이라 가정)
                if published_date and published_date < date_cutoff:
                    continue
                
                # 키워드 필터링 (제목 또는 요약에 키워드가 포함되어 있는지)
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                content_text = (title + " " + summary).lower()
                
                # [DEBUG]
                print(f"[DEBUG] Checking: {title} ({published_date})")
                
                # 이미지 추출 (media_content > enclosures > summary img)
                image_url = "https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" # Tech/Chip default image
                
                if hasattr(entry, 'media_content') and entry.media_content:
                    if 'url' in entry.media_content[0]:
                        image_url = entry.media_content[0]['url']
                elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                    if 'url' in entry.media_thumbnail[0]:
                        image_url = entry.media_thumbnail[0]['url']
                elif 'links' in entry:
                    for link in entry.links:
                        if link.type.startswith('image/'):
                            image_url = link.href
                            break
                            
                # 키워드 중 하나라도 포함되면 수집
                if any(k.lower() in content_text for k in keywords):
                    news_items.append({
                        'title': title,
                        'link': entry.link,
                        'published': published_date.strftime('%Y-%m-%d') if published_date else 'Recent',
                        'summary': summary[:200] + "..." if len(summary) > 200 else summary,
                        'source': feed.feed.get('title', 'Unknown Source'),
                        'image': image_url
                    })
                    seen_links.add(entry.link)
                    
        except Exception as e:
            print(f"[ERROR] Error parsing {feed_url}: {e}")
            continue

    print(f"[OK] Found {len(news_items)} relevant news items.")
    return news_items
