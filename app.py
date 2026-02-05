import streamlit as st
import pandas as pd
import os
import glob
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="Unicorn Signal",
    page_icon="🦄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 스타일 커스텀
st.markdown("""
<style>
    .reportview-container {
        background: #f9fafb;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    h1 {
        font-family: 'Merriweather', serif;
        color: #1f2937;
    }
    .stButton>button {
        background-color: #7c3aed;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 구독자 파일 경로
SUBSCRIBERS_FILE = 'subscribers.csv'

def load_subscribers():
    if not os.path.exists(SUBSCRIBERS_FILE):
        df = pd.DataFrame(columns=['email', 'nickname', 'date'])
        df.to_csv(SUBSCRIBERS_FILE, index=False)
        return df
    return pd.read_csv(SUBSCRIBERS_FILE)

def save_subscriber(email, nickname):
    df = load_subscribers()
    if email in df['email'].values:
        return False, "이미 구독 중인 이메일입니다! 🦄"
    
    new_entry = pd.DataFrame([{
        'email': email, 
        'nickname': nickname, 
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }])
    # concat 사용 권장 (append는 deprecated)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(SUBSCRIBERS_FILE, index=False)
    return True, "구독 신청이 완료되었습니다! 매일 아침 만나요 👋"

# 사이드바: 구독하기
with st.sidebar:
    st.image("https://emojigraph.org/media/apple/unicorn_1f984.png", width=50) # 로고 대체
    st.title("Unicorn Signal")
    st.caption("1인 유니콘 기업가를 위한\n트렌드 큐레이션")
    
    st.divider()
    
    st.subheader("📬 뉴스레터 구독하기")
    with st.form("subscribe_form"):
        nickname = st.text_input("별명 (Nickname)", placeholder="예: 100억 부자")
        email = st.text_input("이메일 (Email)", placeholder="example@gmail.com")
        submit = st.form_submit_button("무료 구독하기")
        
        if submit:
            if email and nickname:
                success, msg = save_subscriber(email, nickname)
                if success:
                    st.success(msg)
                    st.balloons()
                else:
                    st.warning(msg)
            else:
                st.error("이메일과 별명을 모두 입력해주세요.")
    
    st.divider()
    st.info("매일 아침 8시, 가장 핫한 테크 트렌드를 배달해드립니다.")

# 메인 콘텐츠
tab1, tab2 = st.tabs(["🏠 최신 뉴스레터", "📚 지난 아카이브"])

# 아카이브 폴더 확인
if not os.path.exists('archives'):
    os.makedirs('archives')

html_files = glob.glob('archives/*.html')
html_files.sort(key=os.path.getmtime, reverse=True) # 최신순 정렬

with tab1:
    # 1. Hero Section (상단 배너)
    # 로고 이미지 표시 (중앙 정렬)
    col_spacer1, col_img, col_spacer2 = st.columns([1, 2, 1])
    with col_img:
        if os.path.exists("unicorn_signal_logo.png"):
            st.image("unicorn_signal_logo.png", use_container_width=True)
        else:
            st.markdown("<div style='font-size: 4rem; text-align: center;'>🦄</div>", unsafe_allow_html=True)
            
    st.markdown("""
    <div style="text-align: center; padding: 0 0 20px 0;">
        <p style="font-size: 1.1rem; color: #666; font-weight: 500;">
            "바쁜 1인 기업가를 위한, <b>AI가 떠먹여주는 테크 트렌드</b>"
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. 대시보드 (KPI) - 작고 깔끔하게 변경
    # 최신 주제 가져오기
    latest_topic = "-"
    if html_files:
        # 파일명 형식: YYYY-MM-DD_Keyword_Name.html
        # 0번째는 날짜, 1번째부터 끝까지가 키워드
        file_parts = os.path.basename(html_files[0]).replace('.html', '').split('_')
        if len(file_parts) > 1:
            latest_topic = " ".join(file_parts[1:])

    # Custom CSS for metrics
    st.markdown("""
    <style>
    .metric-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 10px; /* 여백 축소 */
    }
    .metric-card {
        background: white;
        padding: 10px 20px; /* 패딩 축소 */
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #eee;
    }
    .metric-value {
        font-size: 1.1rem;
        font-weight: bold;
        color: #1f2937;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #6b7280;
    }
    .status-badge {
        background-color: #dcfce7;
        color: #166534;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">🚀 Today's Topic</div>
            <div class="metric-value">{latest_topic}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">📚 Reports</div>
            <div class="metric-value">{len(html_files)}</div>
        </div>
        <div class="metric-card" style="display: flex; align-items: center; justify-content: center;">
            <span class="status-badge">⚡ ONLINE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
# ... (중략)

# -------------------------------------------------------------------------
# 🔒 관리자 대시보드 (Admin Dashboard)
# -------------------------------------------------------------------------
with st.sidebar:
    st.divider()
    with st.expander("🔒 주인장 전용 (Admin)"):
        admin_pw = st.text_input("비밀번호", type="password")
        # 16자리 랜덤 비밀번호 적용
        SECURE_PW = "X7k9P2m4Rj1Wk8Lz" 
        
        if admin_pw == SECURE_PW:
            st.success("접속 승인! 🔓")
            st.session_state['is_admin'] = True
        elif admin_pw:
            st.error("비밀번호 오류")

if st.session_state.get('is_admin'):
    st.divider()
    st.subheader("📊 Admin Dashboard")
    
    # 구독자 데이터 읽기
    sub_count = 0
    if os.path.exists('subscribers.csv'):
        with open('subscribers.csv', 'r') as f:
            sub_count = len(f.readlines()) - 1 # 헤더 제외

    # 가상 수익 (예시)
    revenue = sub_count * 1000 # 인당 1000원 가치로 산정
    
    # 메트릭 표시
    a1, a2, a3 = st.columns(3)
    a1.metric("👥 총 구독자", f"{sub_count}명", "+2 (Today)")
    a2.metric("💰 예상 광고 수익", f"₩{revenue:,}", "Top 1%")
    a3.metric("📅 다음 발행", "15:00 PM")
    
    st.caption("※ 이 화면은 관리자(본인)에게만 보입니다.")
    st.bar_chart({"Day 1": 10, "Day 2": 15, "Day 3": sub_count}) # 성장이력 그래프 예시

import json

# ... (Previous code)

with tab2:
    st.markdown("### 📚 지난 뉴스레터 아카이브")
    
    # JSON 메타데이터 파일 찾기
    json_files = glob.glob('archives/*.json')
    json_files.sort(key=os.path.getmtime, reverse=True)
    
    if not json_files:
        st.info("아직 저장된 뉴스레터가 없습니다.")
    else:
        # 그리드 레이아웃 (3열)
        cols = st.columns(3)
        
        for idx, json_file in enumerate(json_files):
            with open(json_file, 'r', encoding='utf-8') as f:
                try:
                    meta = json.load(f)
                    
                    # 카드 UI 렌더링
                    with cols[idx % 3]:
                        with st.container(border=True):
                            # 썸네일 표시 (에러 시 기본 이미지)
                            try:
                                st.image(meta.get('thumbnail', 'https://placehold.co/600x400?text=No+Image'), use_container_width=True)
                            except:
                                st.image("https://placehold.co/600x400?text=Error", use_container_width=True)
                                
                            st.subheader(meta.get('title', 'Untitled'))
                            st.caption(f"🗓️ {meta.get('date', '')} | 🏷️ {meta.get('keyword', '')}")
                            st.write(meta.get('summary', ''))
                            
                            # '보기' 버튼 (Unique Key 필수)
                            html_file_path = os.path.join("archives", meta.get('filename', ''))
                            if st.button("뉴스레터 보기 ➡️", key=f"btn_{idx}"):
                                if os.path.exists(html_file_path):
                                    with open(html_file_path, 'r', encoding='utf-8') as hf:
                                        content = hf.read()
                                    # 세션 스테이트에 저장해서 탭 이동 효과
                                    # 세션 스테이트에 저장해서 탭 이동 효과
                                    st.session_state['selected_html'] = content
                                    st.rerun()
                except Exception as e:
                    # JSON 파일이 깨져있거나 읽을 수 없을 때
                    st.error(f"Error loading {os.path.basename(json_file)}")

# 탭 밖에서 선택된 뉴스레터 보여주기 (Overlay 형태)
if 'selected_html' in st.session_state:
    st.divider()
    st.markdown("## 📖 선택한 뉴스레터 읽기")
    if st.button("❌ 닫기 (목록으로 돌아가기)"):
        del st.session_state['selected_html']
        st.rerun()
    st.components.v1.html(st.session_state['selected_html'], height=900, scrolling=True)

# Footer
st.markdown("---")
st.markdown("© 2026 Unicorn Signal. All rights reserved.")
