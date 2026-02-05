import google.generativeai as genai
import os
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
    당신은 1인 유니콘 기업가를 위한 **최고의 비즈니스 인텔리전스 분석가**입니다.
    아래 수집된 뉴스/영상 데이터를 바탕으로 **'유니콘 시그널(Unicorn Signal)' 뉴스레터**를 작성해주세요.
    
    독자는 새로운 사업 기회를 찾는 예비 창업가, 개발자, 투자자입니다. 
    단순한 정보 전달을 넘어, **"그래서 이걸로 어떻게 돈을 벌 수 있는데?"**에 대한 답을 주어야 합니다.

    **작성 규칙**:
    1. **메인 제목 (Headline)**:
        - "Generative AI Trend" 같은 지루한 제목 금지!
        - 독자의 클릭을 유도하는 **카피라이팅 제목**을 맨 첫 줄에 `<h1>` 태그로 작성해주세요.
        - 예: `<h1>자율 에이전트, 개발 기간을 2주로 단축해버리네? 😲</h1>`
    
    2. **톤앤매너**: 
        - 친구에게 말하듯 **위트 있고 센스 있게** ("~거든요", "~했지 뭐예요" 등).
        - 중요한 분석은 **날카롭고 전문적으로**.
        - 문장이 너무 길어지거나 단어가 잘리지 않도록, 호흡이 긴 문장은 적절히 끊어주세요.
        - 시작 멘트: "1인 유니콘 예비사업가 여러분 👋" (단어가 잘리지 않도록 주의)
    
    3. **구조**:
        - **🚨 Market Signal**: 가장 중요한 메가 트렌드 1개를 선정하여 깊이 있게 분석.
        - **💡 Biz Opportunities**: 뉴스들에서 발견한 구체적인 사업 아이디어 3가지.
        - **📚 Must Read**: 놓치면 안 되는 중요 기사/영상 요약.
    
    4. **이미지 배치 (Required)**:
        - 각 뉴스 항목에 해당하는 **Image URL**이 제공되었습니다.
        - 뉴스레터 내 적절한 위치에 `<img src="Image URL" alt="news image">` 태그를 사용하여 이미지를 반드시 삽입하세요.
        - 이미지가 없으면 사용하지 않아도 됩니다.

    5. **출력 형식**:
        - `<h1>...</h1>`로 시작해야 합니다.
        - 반드시 HTML 태그를 포함하여 출력하세요. (`<div>`, `<h2>`, `<ul>`, `<li>`, `<a>`, `<img>` 등)
        - CSS 클래스는 제외하고 시멘틱 태그 위주로 작성하세요.

    수집된 데이터 (상위 5개):
    {combined_text[:15000]}
    """
    
    try:
        response = model.generate_content(prompt)
        newsletter_body = response.text
    
        # 마크다운 코드 블록 제거
        if "```" in newsletter_body:
            newsletter_body = newsletter_body.replace("```html", "").replace("```", "").strip()
            
        # 제목 추출 (H1)
        import re
        title_match = re.search(r'<h1>(.*?)</h1>', newsletter_body, re.IGNORECASE)
        title = "Unicorn Signal Insight" # Default
        
        if title_match:
            title = title_match.group(1)
            # 본문에서는 제거 (또는 유지? 템플릿 헤더에 넣을 것이므로 제거가 깔끔)
            newsletter_body = newsletter_body.replace(title_match.group(0), "")
            
        return title, newsletter_body
        
    except Exception as e:
        return "Insight Generation Failed", f"<div><h3>⚠️ 분석 생성 실패</h3><p>{e}</p></div>"
