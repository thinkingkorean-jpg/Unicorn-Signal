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
    
    # [UI Fix] 제목에서 '유니콘 시그널:' 브랜드명 중복 제거
    replacements = ["유니콘 시그널:", "유니콘 시그널 :", "Unicorn Signal:", "Unicorn Signal :"]
    for r in replacements:
        safe_title = safe_title.replace(r, "")
    safe_title = safe_title.strip()
    
    print(f"[AI] Generated Title: {safe_title}")
    
    # 6. HTML 생성 (Jinja2)
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('newsletter_theme.html')
    
    # [Monetization] 키워드 기반 추천 상품 선정 (잠시 비활성화)
    # from products import get_recommended_product
    # recommended_product = get_recommended_product(expanded_keywords)
    # print(f"[ADS] Selected Product: {recommended_product['title']}")
    
    today_str = datetime.now().strftime('%Y-%m-%d')
    output_html = template.render(
        title=ai_title,
        date=today_str,
        body_content=newsletter_body,
        keywords=", ".join(expanded_keywords),
        # product=recommended_product # 광고 비활성화 요청
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

    # 7-1. 메타데이터 저장 (For Archive UI)
    thumbnail_url = None
    
    # 1. 뉴스 이미지 확인
    if 'news_items' in locals() and news_items:
        for item in news_items:
            if item.get('image'):
                thumbnail_url = item['image']
                break
    
    # 2. 유튜브 썸네일 확인 (뉴스 이미지가 없으면)
    if not thumbnail_url and 'video_items' in locals() and video_items:
        for item in video_items:
            if item.get('thumbnail'):
                thumbnail_url = item['thumbnail']
                break
    
    # 3. 그래도 없으면 깔끔한 텍스트 썸네일 (placeholder) -> [Update] AI 썸네일 생성
    if not thumbnail_url:
        print("[AI] Generating Thumbnail Image...")
        from ai_agent import generate_thumbnail
        thumbnail_url = generate_thumbnail(base_keywords)
        print(f"[AI] Thumbnail Generated: {thumbnail_url}")

    # 요약문 추출 (HTML의 summary-box에서 텍스트만 발췌)
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(output_html, 'html.parser')
        summary_div = soup.find("div", class_="summary-box")
        if summary_div:
            # "3줄 요약" 제목 제외하고 내용만 가져오기
            summary_text = summary_div.get_text(separator=" ", strip=True)
            # 너무 길면 자르기
            if len(summary_text) > 100:
                summary_text = summary_text[:100] + "..."
        else:
            summary_text = f"{base_keywords} 트렌드 분석 및 주요 뉴스 요약"
    except Exception as e:
        print(f"[WARN] Summary extraction failed: {e}")
        summary_text = f"{base_keywords} 트렌드 분석 Report"

    metadata = {
        "title": f"🦄 {ai_title}",
        "date": today_str,
        "keyword": base_keywords,
        "summary": summary_text,
        "thumbnail": thumbnail_url,
        "filename": os.path.basename(html_filename)
    }
    
    import json
    json_filename = html_filename.replace(".html", ".json")
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)
    print(f"[MAIN] Metadata saved to {json_filename}")
    
    # 8. 이메일 전송 (NEW)
    print("[EMAIL] Sending Newsletter...")
    email_subject = f"🦄 {ai_title} ({today_str})"
    # 이메일 수신자 설정 (환경 변수 또는 기본값)
    to_email = os.getenv("TO_EMAIL", "recipient@example.com")
    send_email(email_subject, output_html, to_email=to_email)

if __name__ == "__main__":
    asyncio.run(main())
