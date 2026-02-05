# 🦄 Unicorn Signal (유니콘 시그널)

**"1인 유니콘 기업가를 위한 AI 기반 트렌드 큐레이션 서비스"**

Unicorn Signal은 매일 아침 전 세계의 테크 뉴스(TechCrunch, MIT Tech Review 등)와 유튜브 영상을 AI가 자동으로 수집하고 분석하여, 비즈니스 인사이트가 담긴 뉴스레터를 생성해주는 자동화 도구입니다.

## 🚀 주요 기능

- **자동 수집 (Automation)**: RSS 피드와 유튜브에서 특정 키워드(예: Generative AI) 관련 최신 정보를 자동으로 긁어옵니다.
- **AI 분석 (Gemini Pro)**: 수집된 방대한 정보를 AI가 읽고, "비즈니스 기회" 관점에서 요약 및 분석합니다.
- **웹 대시보드 (Streamlit)**: 생성된 뉴스레터를 웹에서 바로 확인하고, 지난 아카이브를 모아볼 수 있습니다.
- **구독 시스템**: 이메일과 별명을 입력하여 구독자를 관리할 수 있습니다 (`subscribers.csv`).

## 🛠 설치 및 실행 방법

### 1. 환경 설정
Python이 설치되어 있어야 합니다.

```bash
# 필수 라이브러리 설치
pip install -r requirements.txt
```

### 2. API 키 설정
`.env.example` 파일의 이름을 `.env`로 변경하고, Google Gemini API 키를 입력하세요.

```ini
GEMINI_API_KEY=your_api_key_here
```

### 3. 웹 앱 실행 (추천)
바탕화면의 `run_app.bat` 파일을 더블 클릭하거나, 터미널에서 아래 명령어를 입력하세요.

```bash
python -m streamlit run app.py
```

### 4. 스케줄러 실행 (백그라운드 자동화)
매일 아침 8시에 자동으로 뉴스를 수집하려면 스케줄러를 켜두세요.

```bash
python scheduler.py
```

## 📂 프로젝트 구조

- `app.py`: Streamlit 웹 애플리케이션 메인 파일
- `main.py`: 뉴스 수집 및 분석 핵심 로직
- `scheduler.py`: 자동화 스케줄러
- `scrapers/`: 뉴스 및 유튜브 크롤러 모듈
- `archives/`: 생성된 뉴스레터 HTML 파일 저장소
- `subscribers.csv`: 구독자 명단

---
© 2026 Unicorn Signal. Built with Python & Streamlit.
