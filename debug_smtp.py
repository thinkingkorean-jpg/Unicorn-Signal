
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SMTP_PASSWORD")

# Trim just in case
if SENDER_EMAIL: SENDER_EMAIL = SENDER_EMAIL.strip()
if SENDER_PASSWORD: SENDER_PASSWORD = SENDER_PASSWORD.strip()

print(f"Server: {SMTP_SERVER}:{SMTP_PORT}")
print(f"User: {SENDER_EMAIL}")
print(f"Pass: {SENDER_PASSWORD[:2]}...{SENDER_PASSWORD[-2:]}" if SENDER_PASSWORD else "None")

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.set_debuglevel(1)  # Enable detailed debug output
    print("1. EHLO...")
    server.ehlo()
    print("2. STARTTLS...")
    server.starttls()
    print("3. EHLO (again)...")
    server.ehlo()
    print("4. Login...")
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("5. Login Success!")
    server.quit()
except Exception as e:
    print(f"\n[FAILURE] {e}")
