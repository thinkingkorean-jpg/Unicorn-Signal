from youtube_transcript_api import YouTubeTranscriptApi
from youtube_search import YoutubeSearch

def fetch_youtube_videos(keywords, limit=2):
    """
    유튜브에서 관련 영상을 검색하고 자막(Transcript)을 가져옵니다.
    """
    video_data = []
    
    print(f"[SEARCH] Searching YouTube for: {keywords}")
    
    for keyword in keywords[:2]: # 너무 많이 검색하면 느리므로 상위 2개 키워드만
        try:
            # 키워드가 문자열인지 확인 (리스트인 경우 첫 번째 요소 사용) -> AI가 리스트로 줄 수도 있음
            if isinstance(keyword, list):
               keyword = keyword[0]
            
            # YoutubeSearch 사용
            results = YoutubeSearch(str(keyword), max_results=limit).to_dict()
            print(f"[DEBUG] results type: {type(results)}")
            if isinstance(results, list) and len(results) > 0:
                 print(f"[DEBUG] first item type: {type(results[0])}")
                 if isinstance(results[0], str): # 리스트의 요소가 문자열이면 (아마도 키값?)
                     print(f"[DEBUG] contents: {results}")
            if isinstance(results, dict):
                 print(f"[DEBUG] results is dict. keys: {results.keys()}")
                 # 만약 딕셔너리라면 리스트가 아닐 수 있음. 보통은 리스트를 반환함.
            
            for video in results:
                if not isinstance(video, dict):
                    print(f"[DEBUG] Skipping item of type {type(video)}: {video}")
                    continue
                    
                # youtube-search의 결과 딕셔너리 구조에 맞게 수정
                video_id = video.get('id')
                if not video_id: continue
                
                title = video.get('title', 'No Title')
                # url_suffix는 '/watch?v=...' 형태임
                link = f"https://www.youtube.com{video.get('url_suffix', '')}"
                
                # 자막 추출 시도
                transcript_text = ""
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
                    # 자막 텍스트 합치기 (최대 1000자만 - 요약용)
                    transcript_text = " ".join([t['text'] for t in transcript_list])[:1000] + "..."
                except:
                    transcript_text = "(No Transcript Available)"
                    
                # 썸네일 추출 (high resolution preferred)
                image_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                try:
                    if 'thumbnails' in video and video['thumbnails']:
                        thumbnails = video['thumbnails']
                        if isinstance(thumbnails, list):
                            image_url = thumbnails[-1]['url'] if thumbnails else image_url
                        elif isinstance(thumbnails, dict): # 가끔 dict로 올 수 있음
                            # dict인 경우 'high', 'maxres' 등의 키가 있는지 확인하거나 url 키 확인
                            if 'url' in thumbnails:
                                image_url = thumbnails['url']
                            # 만약 thumbnails가 list가 아니라면 그냥 기본 이미지 사용
                except Exception as e:
                    print(f"[DEBUG] Thumbnail extraction failed: {e}")

                video_data.append({
                    'title': title,
                    'link': link,
                    'summary': f"[YouTube Video] {transcript_text}",
                    'source': 'YouTube',
                    'image': image_url
                })
        except Exception as e:
            print(f"[ERROR] Error searching for {keyword}: {e}")
            continue
            
    print(f"[OK] Found {len(video_data)} videos.")
    return video_data
