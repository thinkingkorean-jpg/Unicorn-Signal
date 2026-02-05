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
    if html_files:
        latest_file = html_files[0]
        with open(latest_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=800, scrolling=True)
        
        # 다운로드 버튼
        st.download_button(
            label="이 뉴스레터 다운로드 (HTML)",
            data=html_content,
            file_name=os.path.basename(latest_file),
            mime="text/html"
        )
    else:
        st.warning("아직 발행된 뉴스레터가 없습니다. 스케줄러를 실행하거나 main.py를 실행해보세요!")

with tab2:
    if len(html_files) > 0:
        st.markdown("### 지난 뉴스레터 다시보기")
        selected_file = st.selectbox("보고 싶은 날짜를 선택하세요", html_files, format_func=lambda x: os.path.basename(x).replace('.html', ''))
        
        if selected_file:
            with open(selected_file, 'r', encoding='utf-8') as f:
                archive_content = f.read()
            st.components.v1.html(archive_content, height=800, scrolling=True)
    else:
        st.info("아카이브가 비어있습니다.")

# Footer
st.markdown("---")
st.markdown("© 2026 Unicorn Signal. All rights reserved.")
