import schedule
import time
import subprocess
import random
from datetime import datetime
import asyncio
from main import main as run_newsletter_generation

# 키워드 풀 (다양한 주제)
KEYWORD_POOL = [
    "Generative AI Business Models",
    "SaaS Pricing Trends",
    "B2B AI Startups",
    "Low Code No Code Tools",
    "AI Marketing Automation",
    "Web3 Gaming Trends",
    "Climate Tech Startups",
    "Digital Health AI",
    "E-commerce AI personalization",
    "Fintech AI agents",
    "AI in Education",
    "Robotics Trends 2026",
    "Sustainable Tech",
    "Cybersecurity AI"
]

def job():
    print(f"\n[JOB] Starting scheduled job at {datetime.now()}")
    
    # 랜덤 키워드 선택
    selected_keyword = random.choice(KEYWORD_POOL)
    print(f"[JOB] Today's Keyword: {selected_keyword}")
    
    # main.py의 로직을 실행
    from main import main as run_newsletter_generation
    
    try:
        # 비동기 실행을 위해 asyncio.run 사용
        # main함수 내에서 loop를 새로 생성하는 방식이므로, 
        # 이미 loop가 돌고 있다면 주의해야 하지만 simple script라 괜찮음
        asyncio.run(run_newsletter_generation(keyword=selected_keyword))
    except Exception as e:
        print(f"[ERROR] Job failed: {e}")

if __name__ == "__main__":
    # 매일 오전 8시에 실행
    print("[SCHEDULER] Daily Newsletter Generator Started.")
    print("[SCHEDULER] Will run every day at 08:00 AM.")
    print("[SCHEDULER] Press Ctrl+C to stop.")
    
    # 매일 아침 7시, 오후 3시에 실행
    schedule.every().day.at("07:00").do(job)
    schedule.every().day.at("15:00").do(job)
    
    # schedule.every(10).seconds.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
