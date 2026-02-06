import google.generativeai as genai
import os
import warnings
warnings.filterwarnings("ignore") # Suppress FutureWarnings
from dotenv import load_dotenv

load_dotenv()

# Gemini 설정
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-flash-latest')

def expand_keywords(base_keywords):
    """
    사용자가 입력한 기본 키워드를 AI가 더 구체적인 검색어로 확장해줍니다.
    예: "AI" -> ["Generative AI", "LLM trends", "AI Ethics", "AI Hardware"]
    """
    prompt = f"""
    당신은 테크 트렌드 사냥꾼입니다.
    사용자가 입력한 다음 키워드를 바탕으로, **뉴스 및 유튜브 검색에 적합한 구체적인 연관 키워드 5개**를 영어로 생성해주세요.
    
    입력 키워드: {base_keywords}
    
    **반드시 파이썬 리스트 형식으로만 출력하세요.**
    예시: ["Generative AI", "LLM Applications", "NVIDIA H100", "AI Regulation", "OpenAI"]
    """
    
    try:
        response = model.generate_content(prompt)
        # 단순 파싱 (대괄호 안의 내용 추출)
        text = response.text.strip()
        if '[' in text and ']' in text:
            import ast
            keywords = ast.literal_eval(text[text.find('['):text.find(']')+1])
            if base_keywords not in keywords:
                keywords.append(base_keywords)
            return keywords
        return base_keywords # 실패 시 원본 반환
    except Exception as e:
        print(f"[ERROR] Keyword expansion failed: {e}")
        return base_keywords

def summarize_content(content_list):
    """
    수집된 뉴스 및 유튜브 자막 리스트를 받아서 뉴스레터 섹션을 생성합니다.
    """
    if not content_list:
        return "수집된 콘텐츠가 없습니다."

    # 텍스트 합치기
    combined_text = ""
    for item in content_list:
        # 이미지 정보도 함께 전달
        img_info = f"Image: {item.get('image', 'No Image')}"
        combined_text += f"\nTitle: {item['title']}\nLink: {item['link']}\n{img_info}\nSummary: {item['summary']}\n---"
    
    prompt = f"""
    당신은 실리콘밸리에서 가장 날카로운 통찰력을 가진 **테크 전문 에디터**입니다.
    딱딱한 AI 말투(예: "결론적으로", "살펴보겠습니다", "주목해야 합니다")를 **절대 사용하지 마세요.**
    
    대신, **스마트하고 위트 있는 동료가 커피를 마시며 핵심만 찔러주는 듯한 말투**를 사용하세요.
    - 문장은 짧고 간결하게 끊으세요.
    - 독자(창업가, 개발자)의 시간을 아껴주세요.
    - "왜냐하면", "또한", "따라서" 같은 접속사를 남발하지 마세요.

    **작성 목표:**
    아래 수집된 데이터를 바탕으로 독자가 **"돈이 되는 기회"**를 발견할 수 있는 뉴스레터를 구성하세요.

    **[필수 구성 요소 및 순서]**
    
    **1. [Part 0: The 3-Line "Dip" (핵심 요약)]**
    - 반드시 `<div class="summary-box">` 태그로 감싸세요.
    - 제목은 쓰지 마세요 (CSS로 처리됨).
    - **가장 중요한 3가지 핵심 인사이트**를 불렛포인트(`- `)로 작성하세요.
    - 설명조가 아닌, 핵심만 짚으세요.
    
    **2. [Part 1: Market Signal (메인 스토리)]**
    - **`<h1>` 태그로 섹시하고 자극적인 제목을 다세요.** (주의: "유니콘 시그널"이라는 단어는 제목에 절대 넣지 마세요.)
    - 여러 뉴스를 엮어서 하나의 흐름(Narrative)으로 설명하세요.
    - "이게 왜 중요하냐면..." 식의 화법을 구사하세요.
    
    **3. [Part 2: Key Updates (주요 뉴스)]**
    - 중요한 개별 뉴스들을 소개하세요.
    
    **4. [Part 3: One Business Idea (사업 아이디어)]**
    - 이 트렌드를 활용해 당장 시도해볼 만한 **SaaS 아이디어**나 **비즈니스 모델**을 제안하세요.
    
    **5. [이미지 배치]**
    - 제공된 Image URL을 적절한 곳에 `<img src="URL" alt="...">` 로 넣으세요.
    
    **수집된 데이터:**
    {combined_text[:15000]}
    """
    
    try:
        response = model.generate_content(prompt)
        newsletter_body = response.text
    
        # 마크다운 코드 블록 제거
        if "```" in newsletter_body:
            newsletter_body = newsletter_body.replace("```html", "").replace("```", "").strip()
            
        # 제목 추출 (H1) 및 강력 정제
        import re
        title_match = re.search(r'<h1>(.*?)</h1>', newsletter_body, re.IGNORECASE)
        title = "Unicorn Signal Insight" # Default
        
        if title_match:
            raw_title = title_match.group(1)
            # [Fix] 제목에서 불필요한 prefix 제거 (AI가 지시를 어길 경우 대비)
            title = raw_title.replace("Unicorn Signal", "").replace("유니콘 시그널", "").replace("🦄", "").replace(":", "").strip()
            
            # 본문에서는 제목(H1) 제거 (템플릿 상단에 따로 표시되므로 중복 방지)
            newsletter_body = newsletter_body.replace(title_match.group(0), "")
            
        return title, newsletter_body
        
    except Exception as e:
        return "Insight Generation Failed", f"<div><h3>⚠️ 분석 생성 실패</h3><p>{e}</p></div>"

def generate_thumbnail(keyword):
    """
    키워드를 기반으로 AI 썸네일 이미지를 생성합니다.
    (Note: Gemini Imagen API는 별도 권한이 필요하므로, 즉시 사용 가능한 Pollinations AI를 활용합니다.)
    """
    import random
    import urllib.parse
    
    # 프롬프트 엔지니어링 (Unicorn Signal 스타일)
    style_prompt = "futuristic, 3d render, isometric, high tech, tech trend, purple and neon lighting, unicorn signal style, minimal, premium"
    full_prompt = f"{keyword}, {style_prompt}"
    encoded_prompt = urllib.parse.quote(full_prompt)
    
    # Pollinations AI (Free Stable Diffusion API) 사용하여 이미지 URL 생성
    # 랜덤 시드로 매번 다른 이미지 생성
    seed = random.randint(1, 99999)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=450&seed={seed}&nologo=true"
    
    return image_url
