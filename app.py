import streamlit as st
import pandas as pd
import os
import glob
import json
from datetime import datetime

# -------------------------------------------------------------------------
# 1. Page Config & CSS
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="Unicorn Signal",
    page_icon="🦄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* 전체 배경 */
    .reportview-container { background: #f9fafb; }
    
    /* 사이드바 배경 흰색으로 고정 (로고 위화감 제거) */
    [data-testid="stSidebar"] { background-color: #ffffff; }
    
    /* 헤더 폰트 */
    h1 { font-family: 'Merriweather', serif; color: #1f2937; }
    
    /* 버튼 스타일 */
    .stButton>button {
        background-color: #7c3aed;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #6d28d9;
    }
    
    /* 메트릭 카드 스타일 */
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        border: 1px solid #f3f4f6;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# 2. File & Data Management
# -------------------------------------------------------------------------
SUBSCRIBERS_FILE = 'subscribers.csv'
ANALYTICS_FILE = 'analytics.json'

def load_analytics():
    if not os.path.exists(ANALYTICS_FILE):
        return {"visits": 0, "likes": {}}
    try:
        with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return {"visits": 0, "likes": {}}

def save_analytics(data):
    with open(ANALYTICS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def increment_visit():
    if 'visited' not in st.session_state:
        data = load_analytics()
        data['visits'] = data.get('visits', 0) + 1
        save_analytics(data)
        st.session_state['visited'] = True

def toggle_like(filename):
    # 세션 내 중복 클릭 방지
    liked_key = f"liked_{filename}"
    if st.session_state.get(liked_key, False):
        return False, "이미 좋아요를 누르셨습니다! (중복 방지) 😉"
    
    data = load_analytics()
    if 'likes' not in data: data['likes'] = {}
    
    if filename not in data['likes']:
        data['likes'][filename] = 0
    data['likes'][filename] += 1
    
    save_analytics(data)
    st.session_state[liked_key] = True
    return True, "소중한 피드백 감사합니다! ❤️"

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
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(SUBSCRIBERS_FILE, index=False)
    return True, "구독 신청이 완료되었습니다! 매일 아침 만나요 👋"

# 앱 실행 시 방문자 카운트
increment_visit()

# -------------------------------------------------------------------------
# 3. Sidebar UI
# -------------------------------------------------------------------------
with st.sidebar:
    # [수정] 텍스트 제목 제거하고 로고만 깔끔하게
    if os.path.exists("unicorn_signal_logo.png"):
        st.image("unicorn_signal_logo.png", use_container_width=True)
    else:
        st.image("https://emojigraph.org/media/apple/unicorn_1f984.png", width=80)
        st.markdown("### Unicorn Signal")
    
    st.markdown("---")
    
    st.subheader("📬 뉴스레터 구독")
    with st.form("subscribe_form"):
        nickname = st.text_input("별명", placeholder="예: 100억 부자")
        email = st.text_input("이메일", placeholder="example@gmail.com")
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
                st.error("입력 정보를 확인해주세요.")
    
    st.markdown("---")
    
    # [수정] 관리자 로그인 (맨 아래 숨김 처리)
    with st.expander("🔐 Admin"):
        admin_pw = st.text_input("PW", type="password", key="admin_pw_entry")
        if st.button("Login"):
            if admin_pw == "X7k9P2m4Rj1Wk8Lz":
                st.session_state['is_admin'] = True
                st.rerun()
            else:
                st.error("비밀번호 실패")

# -------------------------------------------------------------------------
# 4. Main Page Routing
# -------------------------------------------------------------------------
if st.session_state.get('is_admin', False):
    # ==========================
    # ADMIN DASHBOARD
    # ==========================
    st.title("📊 Admin Dashboard (Secret)")
    if st.button("⬅️ Logout / 메인으로"):
        st.session_state['is_admin'] = False
        st.rerun()
        
    st.divider()
    
    # 데이터 집계
    analytics = load_analytics()
    sub_df = load_subscribers()
    total_visits = analytics.get('visits', 0)
    sub_count = len(sub_df)
    
    # 3-Column Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("👥 총 구독자", f"{sub_count}명")
    c2.metric("👀 총 방문자", f"{total_visits}회")
    c3.metric("💰 가상 수익", f"₩{(sub_count*1000 + total_visits*10):,}")
    
    st.divider()
    
    # Charts
    st.subheader("📈 인기 리포트 (Likes)")
    likes_data = analytics.get('likes', {})
    if likes_data:
        # Dictionary to DataFrame
        likes_list = [{"Topic": k.replace('.html','').split('_')[-1], "Likes": v} for k,v in likes_data.items()]
        df_likes = pd.DataFrame(likes_list).sort_values('Likes', ascending=False)
        st.bar_chart(df_likes, x="Topic", y="Likes")
    else:
        st.info("아직 좋아요 데이터가 없습니다.")

else:
    # ==========================
    # PUBLIC PAGE
    # ==========================
    
    # [수정] 메인 Hero 섹션: 사용자 요청대로 귀여운 유니콘 이미지 + 중앙 정렬
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://emojigraph.org/media/apple/unicorn_1f984.png" width="100">
        <h1 style="margin-top: 10px;">Unicorn Signal</h1>
        <p style="color: #666;">"바쁜 1인 기업가를 위한, AI가 떠먹여주는 테크 트렌드"</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab_home, tab_archive = st.tabs(["🏠 홈 (Latest)", "📚 아카이브 (History)"])
    
    # 데이터 로드
    if not os.path.exists('archives'): os.makedirs('archives')
    html_files = sorted(glob.glob('archives/*.html'), key=os.path.getmtime, reverse=True)
    json_files = sorted(glob.glob('archives/*.json'), key=os.path.getmtime, reverse=True)

    # 1) 홈 탭
    with tab_home:
        # KPI 배지 (간단하게)
        latest_title = "No Data"
        if html_files:
            latest_title = os.path.basename(html_files[0]).split('_')[1] if '_' in os.path.basename(html_files[0]) else "Tech Trend"
            
        st.markdown(f"""
        <div style="display: flex; justify-content: center; gap: 15px; margin-bottom: 30px;">
            <div class="metric-card">🔥 Topic: <b>{latest_title}</b></div>
            <div class="metric-card">📑 Reports: <b>{len(html_files)}</b></div>
            <div class="metric-card" style="background:#dcfce7; color:#166534;">⚡ Status: <b>Online</b></div>
        </div>
        """, unsafe_allow_html=True)
        
        # 최신 뉴스레터 표시
        if html_files:
            with open(html_files[0], 'r', encoding='utf-8') as f:
                st.components.v1.html(f.read(), height=800, scrolling=True)
        else:
            st.info("👋 현재 발행된 뉴스레터가 없습니다. 스케줄러가 곧 첫 리포트를 배달합니다!")

    # 2) 아카이브 탭
    with tab_archive:
        # [수정] 보기 모드 vs 목록 모드 (Toggle)
        
        if 'selected_html' in st.session_state and st.session_state['selected_html']:
            # >>> 상세 보기 화면 <<<
            
            # [수정] 상단 컨트롤 바 (뒤로가기 + 좋아요)
            c_back, c_like = st.columns([1, 4])
            with c_back:
                if st.button("⬅️ 목록으로"):
                    del st.session_state['selected_html']
                    st.rerun()
            with c_like:
                current_file = st.session_state.get('selected_file_name', 'unknown')
                if st.button(f"❤️ 좋아요 ({analytics.get('likes', {}).get(current_file, 0)})"):
                    success, msg = toggle_like(current_file)
                    if success:
                        st.balloons()
                        st.success(msg)
                    else:
                        st.info(msg)
            
            # 뉴스레터 본문
            st.components.v1.html(st.session_state['selected_html'], height=900, scrolling=True)
            
        else:
            # >>> 목록 화면 <<<
            if not json_files:
                st.info("보관된 리포트가 없습니다.")
            else:
                cols = st.columns(3)
                for i, jpath in enumerate(json_files):
                    with open(jpath, 'r', encoding='utf-8') as f:
                        try:
                            meta = json.load(f)
                        except:
                            continue
                            
                    with cols[i % 3]:
                        with st.container(border=True):
                            # 썸네일
                            thumb = meta.get('thumbnail')
                            if thumb: st.image(thumb, use_container_width=True)
                            else: st.markdown("🦄")
                            
                            st.subheader(meta.get('title', '제목 없음'))
                            st.caption(meta.get('date', ''))
                            
                            # [수정] '읽기' 버튼 누르면 selected_html 세션에 담고 rerun -> 상세 화면 전환
                            if st.button("읽기 ➡️", key=f"read_{i}"):
                                target_html = jpath.replace('.json', '.html')
                                if os.path.exists(target_html):
                                    with open(target_html, 'r', encoding='utf-8') as hf:
                                        content = hf.read()
                                    st.session_state['selected_html'] = content
                                    st.session_state['selected_file_name'] = os.path.basename(target_html)
                                    st.rerun()
