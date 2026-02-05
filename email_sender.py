import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "trendhunter.ai@gmail.com") 
SENDER_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_NAME = os.getenv("SENDER_NAME", "Unicorn Signal")

def send_email(subject, html_content, to_email="jh.lee267@cj.net"):
    """
    HTML 뉴스레터를 이메일로 발송합니다.
    """
    if not SENDER_PASSWORD:
        print("[EMAIL] SMTP_PASSWORD not set. Skipping email send.")
        print(f"[EMAIL] Would have sent to {to_email} with subject: {subject}")
        return False

    try:
        # 이메일 메시지 구성
        msg = MIMEMultipart()
        msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = subject

        # 본문 추가 (HTML)
        msg.attach(MIMEText(html_content, 'html'))

        # SMTP 연결 및 전송
        print(f"[EMAIL] Connecting to {SMTP_SERVER}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, to_email, text)
        server.quit()
        
        print(f"[EMAIL] Sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        return False

if __name__ == "__main__":
    # Test
    send_email("Test Newsletter", "<h1>Hello</h1><p>This is a test.</p>")
