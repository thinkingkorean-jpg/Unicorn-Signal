import gspread
import os
import json
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials
import streamlit as st

# 구글 시트 범위 설정
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# 접속할 구글 시트 이름 (미리 생성해두거나, 코드로 생성 가능)
SHEET_NAME = "Unicorn_Signal_Subscribers"

def get_gspread_client():
    """
    인증을 처리하고 gspread 클라이언트를 반환합니다.
    1. 로컬: service_account.json 확인
    2. 클라우드: st.secrets 확인
    """
    creds = None
    
    # 1. 로컬 파일 확인
    if os.path.exists("service_account.json"):
        creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
    
    # 2. Streamlit Cloud Secrets 확인
    elif "gcp_service_account" in st.secrets:
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
        
    if not creds:
        return None
        
    return gspread.authorize(creds)

def init_google_sheet():
    """
    시트에 연결하고, 없으면 생성(권한 필요)하거나 찾습니다.
    헤더가 없으면 작성합니다.
    """
    client = get_gspread_client()
    if not client:
        return None, "Google 인증 키(service_account.json)가 없습니다."
        
    try:
        # 시트 열기 시도
        sheet = client.open(SHEET_NAME).sheet1
    except gspread.SpreadsheetNotFound:
        try:
            # 시트가 없으면 생성 시도 (서비스 계정에 권한이 있어야 함)
            sh = client.create(SHEET_NAME)
            sheet = sh.sheet1
            # 이메일 공유가 필요할 수 있음 (출력 권장)
            # sh.share('thinkingkorean@gmail.com', perm_type='user', role='owner')
        except Exception as e:
             return None, f"시트를 찾을 수 없고 생성도 실패했습니다: {e}"

    # 헤더 확인
    try:
        header = sheet.row_values(1)
        if not header:
            sheet.append_row(["email", "nickname", "date"])
    except:
         sheet.append_row(["email", "nickname", "date"])
         
    return sheet, "Success"

def save_subscriber_gsheet(email, nickname):
    """
    구글 시트에 구독자 저장
    """
    sheet, msg = init_google_sheet()
    if not sheet:
        return False, msg # 인증 실패 혹은 시트 오류
        
    try:
        # 중복 확인
        # 모든 레코드 가져오기 (데이터가 적을 때 유효)
        records = sheet.get_all_records()
        df = pd.DataFrame(records)
        
        if not df.empty and 'email' in df.columns and email in df['email'].values:
             return False, "이미 구독 중인 이메일입니다! (Google Sheet)"
             
        # 추가
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sheet.append_row([email, nickname, current_time])
        return True, "구독 완료! (Google Sheet 저장됨)"
        
    except Exception as e:
        return False, f"저장 중 오류 발생: {e}"

def load_subscribers_gsheet():
    """
    구글 시트에서 구독자 목록 로드 (DataFrame 반환)
    """
    sheet, msg = init_google_sheet()
    if not sheet:
        return pd.DataFrame(columns=['email', 'nickname', 'date']) # 실패 시 빈 DF
        
    try:
         records = sheet.get_all_records()
         # gspread는 빈 시트일 때 빈 리스트 반환
         if not records:
             return pd.DataFrame(columns=['email', 'nickname', 'date'])
         return pd.DataFrame(records)
    except Exception:
        return pd.DataFrame(columns=['email', 'nickname', 'date'])
