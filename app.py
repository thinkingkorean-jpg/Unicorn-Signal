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
    
    /* [Dark Mode Spec] 사이드바: 로고 배경(흰색)과 맞추기 위해 강제 흰색 유지 + 글씨 검정 */
    [data-testid="stSidebar"] { 
        background-color: #ffffff; 
    }
    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
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
        color: #1f2937; /* 다크모드에서도 글씨 잘 보이게 */
    }

    /* [Mobile/DarkMode Fix] 뉴스레터 본문용 '종이' 스타일 컨테이너 */
    .newsletter-paper {
        background-color: #ffffff;
        color: #000000;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }
    /* 모바일에서는 패딩 줄임 */
    @media (max-width: 640px) {
        .newsletter-paper {
            padding: 15px;
        }
    }
    
    /* [Fix] 이미지 테두리/그림자 제거 및 중앙 정렬 보정 */
    img {
        border: none !important;
        box-shadow: none !important;
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
# -------------------------------------------------------------------------
# 4. Main Page Routing
# -------------------------------------------------------------------------
# 공통 데이터 로딩
analytics = load_analytics()
sub_df = load_subscribers()

if st.session_state.get('is_admin', False):
    # ==========================
    # ==========================
    # ADMIN DASHBOARD
    # ==========================
    st.title("📊 Admin Dashboard")
    
    st.subheader("👥 구독자 현황")
    if not sub_df.empty:
        st.dataframe(sub_df, use_container_width=True)
        st.write(f"총 구독자: {len(sub_df)}명")
    else:
        st.info("아직 구독자가 없습니다.")
        
    st.divider()
    if st.button("⬅️ Logout / 메인으로"):
        st.session_state['is_admin'] = False
        st.rerun()
        
    st.divider()
    
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
        # Topic 파싱 개선: 날짜_주제.html -> 주제
        likes_list = []
        for k, v in likes_data.items():
            topic = k
            if '_' in k:
                parts = k.split('_', 1) # 첫번째 _로만 분리 (날짜, 나머지)
                if len(parts) > 1:
                    topic = parts[1].replace('.html', '').replace('_', ' ')
            likes_list.append({"Topic": topic, "Likes": v})
            
        df_likes = pd.DataFrame(likes_list).sort_values('Likes', ascending=False)
        st.bar_chart(df_likes, x="Topic", y="Likes")
    else:
        st.info("아직 좋아요 데이터가 없습니다.")

else:
    # ==========================
    # PUBLIC PAGE
    # ==========================
    
    # [수정] 메인 Hero 섹션: 텍스트 제목 제거, 로고와 슬로건만 유지
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://emojigraph.org/media/apple/unicorn_1f984.png" width="120" style="display: block; margin: 0 auto;">
        <p style="color: #555; font-size: 1.1rem; margin-top: 15px;">
            <b>"바쁜 1인 기업가를 위한, AI가 떠먹여주는 테크 트렌드"</b><br>
            <span style="font-size: 0.9rem; color: #888;">매일 아침 07:00, 오후 15:00 / 3줄 요약 + 인사이트</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab_home, tab_archive = st.tabs(["🏠 홈 (Latest)", "📚 아카이브 (History)"])
    
    # 데이터 로드
    if not os.path.exists('archives'): os.makedirs('archives')
    # [Fix] 파일명(날짜) 기준으로 정렬 (수정일 기준 X -> 내용 수정해도 순서 유지)
    html_files = sorted(glob.glob('archives/*.html'), reverse=True)
    json_files = sorted(glob.glob('archives/*.json'), reverse=True)

    # 1) 홈 탭
    # 1) 홈 탭
    with tab_home:
        # KPI 배지 & 최신 토픽 파싱 개선
        latest_title = "No Data"
        if html_files:
            filename = os.path.basename(html_files[0])
            # 2024-02-05_Generative_AI.html -> Generative AI
            if '_' in filename:
                parts = filename.split('_', 1)
                if len(parts) > 1:
                    latest_title = parts[1].replace('.html', '').replace('_', ' ')
            else:
                latest_title = filename.replace('.html', '')
            
        st.markdown(f"""
        <div style="display: flex; justify-content: center; gap: 15px; margin-bottom: 20px;">
            <div class="metric-card">🔥 Topic: <b>{latest_title}</b></div>
            <div class="metric-card">📑 Reports: <b>{len(html_files)}</b></div>
            <div class="metric-card" style="background:#dcfce7; color:#166534;">⚡ Status: <b>Online</b></div>
        </div>
        """, unsafe_allow_html=True)
        
        # 최신 뉴스레터 표시 (iframe 제거 -> st.markdown으로 통합 스크롤 구현)
        if html_files:
            with open(html_files[0], 'r', encoding='utf-8') as f:
                raw_html = f.read()
                
                # [Fix] HTML 구조 파싱 후 스타일과 본문만 추출하여 렌더링 (CSS 깨짐 완벽 방지)
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(raw_html, 'html.parser')
                
                # 1. 스타일 추출
                style_content = ""
                if soup.style:
                    style_content = soup.style.string
                
                # 2. 본문(Container) 추출
                body_content = soup.find('div', class_='container')
                if not body_content:
                    body_content = soup.body
                
                if body_content:
                    # newsletter-paper 클래스를 적용하여 스타일 통일
                    # [Fix] f-string 들여쓰기 제거 (Markdown Code Block 인식 방지)
                    final_html = f"""<style>{style_content}</style>
<div class="newsletter-paper">
{body_content.decode_contents()}
</div>"""
                    st.markdown(final_html, unsafe_allow_html=True)
                else:
                    st.error("뉴스레터 형식이 올바르지 않습니다.")

        else:
            st.info("👋 현재 발행된 뉴스레터가 없습니다. 스케줄러가 곧 첫 리포트를 배달합니다!")

    # 2) 아카이브 탭
    with tab_archive:
        if 'selected_html' in st.session_state and st.session_state['selected_html']:
            # >>> 상세 보기 화면 <<<
            
            # [수정] 상단 컨트롤 바 (심플하게 뒤로가기만)
            if st.button("⬅️ 목록으로"):
                del st.session_state['selected_html']
                st.rerun()
            
            # 뉴스레터 본문
            html_content = st.session_state['selected_html']
            
            # [Fix] HTML 파싱 및 렌더링
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            style_content = soup.style.string if soup.style else ""
            body_content = soup.find('div', class_='container')
            if not body_content: body_content = soup.body
            
            if body_content:
                # [Fix] f-string 들여쓰기 제거
                final_html = f"""<style>{style_content}</style>
<div class="newsletter-paper">
{body_content.decode_contents()}
</div>"""
                st.markdown(final_html, unsafe_allow_html=True)

            st.divider()
            
            # [수정] 좋아요 버튼을 하단으로 이동
            current_file = st.session_state.get('selected_file_name', 'unknown')
            like_count = analytics.get('likes', {}).get(current_file, 0)
            
            st.divider()
            
            # [수정] 좋아요 버튼을 하단으로 이동
            current_file = st.session_state.get('selected_file_name', 'unknown')
            like_count = analytics.get('likes', {}).get(current_file, 0)
            
            # 하단 중앙 정렬
            c_left, c_center, c_right = st.columns([1, 2, 1])
            with c_center:
                if st.button(f"❤️ 이 리포트가 맘에 드셨다면? (좋아요 {like_count})", use_container_width=True):
                    success, msg = toggle_like(current_file)
                    if success:
                        st.balloons()
                        st.success(msg)
                    else:
                        st.info(msg)
            
        else:
            # >>> 목록 화면 <<<
            if not json_files:
                st.info("보관된 리포트가 없습니다.")
            else:
                # [Fix] 정렬 (파일명 역순 = 날짜 최신순)
                json_files = sorted(json_files, reverse=True)

                # [Fix] 모던한 카드 디자인 & 이미지 폴백 CSS (Blue Theme)
                st.markdown("""
                <style>
                .archive-card-container {
                    height: 100%;
                    min-height: 460px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                }
                .archive-thumb-wrapper {
                    position: relative;
                    width: 100%;
                    height: 200px;
                    border-radius: 12px;
                    overflow: hidden;
                    /* 세련된 딥 블루 그라데이션 (기본 배경) */
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    margin-bottom: 12px;
                }
                .archive-thumb-placeholder-text {
                    position: absolute;
                    color: rgba(255,255,255,0.8);
                    font-weight: 700;
                    font-size: 1.2rem;
                    letter-spacing: 1px;
                    z-index: 1;
                }
                .archive-thumb {
                    position: relative;
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    z-index: 2;
                    transition: opacity 0.3s ease;
                }
                .archive-title {
                    font-size: 1.15rem;
                    font-weight: 800;
                    margin-bottom: 8px;
                    line-height: 1.4;
                    min-height: 2.8em;
                    color: #1f2937;
                }
                .archive-summ {
                    font-size: 0.9rem; 
                    color: #4b5563; 
                    margin-bottom: 15px; 
                    line-height: 1.6;
                }
                div[data-testid="stVerticalBlockBorderWrapper"] > div {
                    height: 100%;
                }
                </style>
                """, unsafe_allow_html=True)

                # [Fix] Grid System
                def chunked(iterable, n):
                    return [iterable[i:i + n] for i in range(0, len(iterable), n)]

                rows = chunked(json_files, 3)
                
                for row_files in rows:
                    cols = st.columns(3)
                    for i, jpath in enumerate(row_files):
                        with open(jpath, 'r', encoding='utf-8') as f:
                            try:
                                meta = json.load(f)
                            except:
                                continue
                        
                        # [Fix] 제목 정제
                        title = meta.get('title', '제목 없음')
                        for remove_str in ["유니콘 시그널:", "유니콘 시그널", "Unicorn Signal:", "Unicorn Signal", "🦄"]:
                            title = title.replace(remove_str, "")
                        title = title.strip()
                        if title.startswith(":"): title = title[1:].strip()
                        
                        # [Fix] 썸네일 URL 검증
                        thumb = meta.get('thumbnail')
                        # URL이 너무 짧거나(10자 이하) http가 없으면 아예 빈 문자열로 처리하여 바로 폴백이 보이게 함
                        if not thumb or not isinstance(thumb, str) or len(thumb) < 10 or not thumb.startswith("http"):
                           thumb = "" 
                        
                        # [Fix] 요약문 정제 (불렛포인트 변환)
                        summary = meta.get('summary', '')
                        summary = summary.replace("🚀 3줄 요약: 왜 이걸 봐야 할까요?", "").replace("3줄 요약:", "").replace("왜 이걸 봐야 할까요?", "").strip()
                        
                        if "- " not in summary:
                            sentences = summary.replace("?", "?|").replace(".", ".|").split("|")
                            clean_sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
                            summary = "<br>".join([f"• {s}" for s in clean_sentences[:3]])
                        else:
                            summary = summary.replace("\n", "<br>")

                        # HTML 렌더링 (이미지 로드 실패 시 투명화 -> 배경 그라데이션 노출)
                        cols[i].markdown(f"""
                        <div class="archive-card-container">
                            <div class="archive-thumb-wrapper">
                                <div class="archive-thumb-placeholder-text">Unicorn Signal</div>
                                <img src="{thumb}" class="archive-thumb" 
                                     onerror="this.style.opacity='0';" 
                                     onload="this.style.opacity='1';">
                            </div>
                            <div>
                                <div class="archive-title">{title}</div>
                                <div style="color: #6b7280; font-size: 0.8rem; margin-bottom: 8px;">{meta.get('date', '')}</div>
                                <div class="archive-summ">
                                    {summary}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with cols[i]:
                             unique_key = f"read_{os.path.basename(jpath)}"
                             if st.button("읽기 ➡️", key=unique_key):
                                target_html = jpath.replace('.json', '.html')
                                if os.path.exists(target_html):
                                    with open(target_html, 'r', encoding='utf-8') as hf:
                                        content = hf.read()
                                    st.session_state['selected_html'] = content
                                    st.session_state['selected_file_name'] = os.path.basename(target_html)
                                    st.rerun()
