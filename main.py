import os
import asyncio
import sys
from config import RSS_FEEDS
from scrapers.news import fetch_rss_news
from scrapers.youtube import fetch_youtube_videos
from ai_agent import expand_keywords, summarize_content
from email_sender import send_email
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# 인자(Argument)로 키워드를 받을 수 있도록 수정
async def main(keyword=None):
    print("[START] TrendHunter AI Starting...")
    
    base_keywords = keyword
    
    # 1. 사용자 입력 (자동화 시 인자로 받음)
    if not base_keywords:
        print("Enter keywords (e.g., Generative AI, Crypto)")
        # 타임아웃 없는 input은 스케줄러에서 멈출 수 있음.
        # 테스트를 위해 인자가 없으면 기본값 사용하도록 변경하거나 input 사용
        if len(sys.argv) > 1:
             base_keywords = sys.argv[1]
        else:
             try:
                base_keywords = input("Input keywords: ")
             except EOFError:
                base_keywords = "Generative AI" # Default functionality for non-interactive
                
    if not base_keywords:
        base_keywords = "Generative AI"
        
    print(f"\n[ANALYSIS] Analyzing keywords: {base_keywords}...")
    
    # 2. AI 키워드 확장
    expanded_keywords = expand_keywords(base_keywords)
    print(f"[EXPAND] Expanded Keywords: {expanded_keywords}")
    
    # 3. 데이터 수집
    # 3-1. 뉴스 수집
    target_feeds = RSS_FEEDS['tech'] + RSS_FEEDS['ai']
    # 간단한 키워드 매칭으로 피드 추가
    if 'crypto' in base_keywords.lower() or 'coin' in base_keywords.lower():
        target_feeds += RSS_FEEDS['crypto']
        
    news_items = fetch_rss_news(target_feeds, expanded_keywords)
    
    # 3-2. 유튜브 수집
    video_items = fetch_youtube_videos(expanded_keywords)
    
    # 4. 콘텐츠 통합
    all_content = news_items + video_items
    print(f"\n[INFO] Collected {len(all_content)} items total.")
    
    if not all_content:
        print("[FAIL] No content found. Try broader keywords.")
        # 컨텐츠가 없어도 이메일은 보내지 않음
        return

    # 5. AI 요약 및 인사이트 (Unicorn Signal) 생성
    print("[AI] Generating Unicorn Signal Insight...")
    ai_title, newsletter_body = summarize_content(all_content)
    
    # 인코딩 에러 방지 처리
    try:
        safe_title = ai_title.encode('cp949', errors='ignore').decode('cp949')
    except:
        safe_title = ai_title
        
    print(f"[AI] Generated Title: {safe_title}")
    
    # 6. HTML 생성 (Jinja2)
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('newsletter_theme.html')
    
    today_str = datetime.now().strftime('%Y-%m-%d')
    output_html = template.render(
        title=ai_title,
        date=today_str,
        body_content=newsletter_body,
        keywords=", ".join(expanded_keywords)
    )
    
    # 7. 파일 저장 (Archiving)
    archive_dir = "archives"
    os.makedirs(archive_dir, exist_ok=True)
    
    safe_keyword = base_keywords.replace(' ', '_')
    filename_base = f"{archive_dir}/{today_str}_{safe_keyword}"
    
    html_filename = f"{filename_base}.html"
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(output_html)
        
    print(f"\n[DONE] Trend Report Saved: {html_filename}")
    
    # 8. 이메일 전송 (NEW)
    print("[EMAIL] Sending Newsletter...")
    email_subject = f"🦄 {ai_title} ({today_str})"
    send_email(email_subject, output_html, to_email="jh.lee267@cj.net")

if __name__ == "__main__":
    asyncio.run(main())
