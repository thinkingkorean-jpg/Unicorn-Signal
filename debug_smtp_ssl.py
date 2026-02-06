
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465 # SSL Port
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SMTP_PASSWORD")

if SENDER_EMAIL: SENDER_EMAIL = SENDER_EMAIL.strip()
if SENDER_PASSWORD: SENDER_PASSWORD = SENDER_PASSWORD.strip()

print(f"Server: {SMTP_SERVER}:{SMTP_PORT} (SSL mode)")
print(f"User: {SENDER_EMAIL}")

try:
    print("1. Connecting via SMTP_SSL...")
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
    server.set_debuglevel(1)
    
    print("2. EHLO...")
    server.ehlo()
    
    # SSL implies no starttls needed usually, encryption happens at connect
    
    print("3. Login...")
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("4. Login Success!")
    server.quit()
except Exception as e:
    print(f"\n[FAILURE] {e}")
