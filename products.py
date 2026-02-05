# 쿠팡 파트너스/제휴 마케팅 상품 리스트
# 키워드와 매칭되는 상품을 설정해두면, 뉴스레터 주제에 맞춰 자동으로 노출됩니다.

# [사용법]
# 1. 쿠팡 파트너스에서 상품 링크 생성
# 2. 아래 리스트에 추가 (키워드, 상품명, 이미지주소, 구매링크)
# 3. 매칭되는 키워드가 없으면 'default' 상품이 노출됩니다.

AFFILIATE_PRODUCTS = [
    {
        "keywords": ["AI", "Generative", "GPT", "LLM"],
        "title": "AI 2025: 트렌드와 미래 전망",
        "description": "생성형 AI 시대, 무엇을 준비해야 하는가? 필독서",
        "image_url": "https://image.yes24.com/goods/122090360/XL", # 예시 이미지
        "link": "https://link.coupang.com/..." # 실제 파트너스 링크로 교체 필요
    },
    {
        "keywords": ["Finance", "Economy", "Fintech", "Bitcoin", "Crypto"],
        "title": "돈의 속성 - 최상위 부자가 말하는 돈",
        "description": "자본주의 시장에서 살아남는 법",
        "image_url": "https://image.yes24.com/goods/90428162/XL",
        "link": "https://link.coupang.com/..."
    },
    {
        "keywords": ["Startup", "SaaS", "Business", "Marketing"],
        "title": "제로 투 원 (Zero to One)",
        "description": "경쟁하지 말고 독점하라, 스타트업 바이블",
        "image_url": "https://image.yes24.com/goods/15135431/XL",
        "link": "https://link.coupang.com/..."
    },
    # 기본값 (매칭 안될 때 표시)
    {
        "id": "default",
        "title": "맥북 프로 14 M3",
        "description": "1인 기업가를 위한 최고의 생산성 도구",
        "image_url": "https://img.danawa.com/prod_img/500000/393/947/img/29947393_1.jpg?shrink=330:*&_v=20231121153322",
        "link": "https://link.coupang.com/..."
    }
]

def get_recommended_product(target_keywords):
    """
    뉴스레터의 핵심 키워드 리스트를 받아서, 가장 적절한 상품을 반환합니다.
    """
    target_str = " ".join(target_keywords).lower()
    
    # 1. 키워드 매칭 시도
    for product in AFFILIATE_PRODUCTS:
        if "keywords" in product:
            for k in product["keywords"]:
                if k.lower() in target_str:
                    return product
                    
    # 2. 매칭 실패 시 기본 상품(default) 반환
    for product in AFFILIATE_PRODUCTS:
        if product.get("id") == "default":
            return product
            
    return AFFILIATE_PRODUCTS[0] # Fallback
