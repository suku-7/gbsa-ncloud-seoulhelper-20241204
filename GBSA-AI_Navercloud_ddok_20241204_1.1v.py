#--------------------------------------------------------------------
# 라이브러리 불러오기
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import re
import os  # .env 파일 관리를 위해 os 라이브러리 추가
from dotenv import load_dotenv  # .env 파일 로드를 위한 라이브러리 추가

# .env 파일에서 환경 변수 불러오기
load_dotenv()

# Google Maps API Key
API_KEY = os.getenv("Maps_API_KEY")

# Naver Clova API 정보
CLOVA_HOST = os.getenv("CLOVA_HOST")
CLOVA_API_KEY = os.getenv("CLOVA_API_KEY")
CLOVA_API_KEY_PRIMARY_VAL = os.getenv("CLOVA_API_KEY_PRIMARY_VAL")
CLOVA_REQUEST_ID = os.getenv("CLOVA_REQUEST_ID")

# Naver Search API 정보 (함수 내부에서 사용되므로 미리 변수화)
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")


# CSV 파일 읽기
df_restaurants = pd.read_csv('restaurants1.csv', encoding='utf-8')
df_attractions = pd.read_csv('attraction1.csv', encoding='utf-8')

#--------------------------------------------------------------------
# 맛집 및 관광 명소 위치 정보를 저장
restaurants_locations = []
attractions_locations = []

for idx, row in df_restaurants.iterrows():
    lat, lon = row['Latitude'], row['Longitude']
    restaurant_location = {
        "name": row["상호명"],
        "address": row["주소"],
        "hours": row["운영시간"],
        "transport": row["교통정보"],
        "menu": row["대표메뉴"],
        "lat": row["Latitude"],
        "lon": row["Longitude"],
    }
    restaurants_locations.append(restaurant_location)

for idx, row in df_attractions.iterrows():
    lat, lon = row['Latitude'], row['Longitude']
    attraction_location = {
        "name": row["상호명"],
        "address": row["주소"],
        "hours": row["운영시간"],
        "transport": row["교통정보"],
        "tag": row["태그"],
        "lat": row["Latitude"],
        "lon": row["Longitude"],
    }
    attractions_locations.append(attraction_location)

#--------------------------------------------------------------------
# 서울시 챗봇 실행 클래스
class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }
        response = requests.post(
            self._host + '/testapp/v1/chat-completions/HCX-003',
            headers=headers,
            json=completion_request,
            stream=True
        )
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8")[5:])  # `data:` 부분 제거
                    if "message" in data and data["message"]["role"] == "assistant":
                        content = data["message"]["content"]
                        if full_response != content:  # 중복된 내용인지 확인
                            full_response += content  # 중복이 아닌 경우만 추가

                except json.JSONDecodeError:
                    continue
        return full_response.strip()  # 중복 방지를 위해 출력 문자열을 정리
#--------------------------------------------------------------------
# Streamlit 페이지 설정
st.set_page_config(layout="wide")

# 화면 좌우 분할
col1, col2 = st.columns([3, 2])

# <<- 좌측 지도 및 데이터프레임 표시
with col1:
    # 지도 섹션
    st.title("서울시 여행 지도")
    st.write("서울시에서 놀러갈 맛집, 놀 곳, 핫플들을 지도에서 확인하세요.")

    # 장소 선택 박스 (맛집)
    selected_restaurant_name = st.selectbox("맛집을 선택하세요", df_restaurants['상호명'])
    selected_restaurant = df_restaurants[df_restaurants['상호명'] == selected_restaurant_name].iloc[0]
    selected_restaurant_address = selected_restaurant['주소']

    # 장소 선택 박스 (관광 명소)
    selected_attraction_name = st.selectbox("관광 명소를 선택하세요", df_attractions['상호명'])
    selected_attraction = df_attractions[df_attractions['상호명'] == selected_attraction_name].iloc[0]
    selected_attraction_address = selected_attraction['주소']

    # Google Maps HTML 생성
    html_code = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>서울시 여행 지도</title>
        <script src="https://maps.googleapis.com/maps/api/js?key={API_KEY}"></script>
        <script>
          function initMap() {{
            var mapCenter = {{lat: 37.5665, lng: 126.9780}};  // 서울 중심
            var map = new google.maps.Map(document.getElementById('map'), {{
              zoom: 12,
              center: mapCenter
            }});

            // 맛집 마커 추가
            var restaurantLocation = {{lat: {selected_restaurant["Latitude"]}, lng: {selected_restaurant["Longitude"]}}};
            var restaurantMarker = new google.maps.Marker({{
              map: map,
              position: restaurantLocation,
              title: '{selected_restaurant_name}',
              icon: {{
                url: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                scaledSize: new google.maps.Size(60, 60),
              }}
            }});
            var restaurantInfowindow = new google.maps.InfoWindow({{
              content: "<b>" + '{selected_restaurant_name}' + "</b><br>" +
                       "주소: " + '{selected_restaurant_address}' + "<br>" +
                       "운영시간: " + '{selected_restaurant["운영시간"]}' + "<br>" +
                       "교통정보: " + '{selected_restaurant["교통정보"]}' + "<br>" +
                       "대표메뉴: " + '{selected_restaurant["대표메뉴"]}'
            }});
            restaurantMarker.addListener("click", function() {{
              restaurantInfowindow.open(map, restaurantMarker);
            }});
            map.setCenter(restaurantLocation);

            // 관광 명소 마커 추가
            var attractionLocation = {{lat: {selected_attraction["Latitude"]}, lng: {selected_attraction["Longitude"]}}};
            var attractionMarker = new google.maps.Marker({{
              map: map,
              position: attractionLocation,
              title: '{selected_attraction_name}',
              icon: {{
                url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                scaledSize: new google.maps.Size(60, 60),
              }}
            }});
            var attractionInfowindow = new google.maps.InfoWindow({{
              content: "<b>" + '{selected_attraction_name}' + "</b><br>" +
                       "주소: " + '{selected_attraction_address}' + "<br>" +
                       "운영시간: " + '{selected_attraction["운영시간"]}' + "<br>" +
                       "교통정보: " + '{selected_attraction["교통정보"]}' + "<br>" +
                       "태그: " + '{selected_attraction["태그"]}'
            }});
            attractionMarker.addListener("click", function() {{
              attractionInfowindow.open(map, attractionMarker);
            }});
            map.setCenter(attractionLocation);
          }}
        </script>
      </head>
      <body onload="initMap()">
        <div id="map" style="height: 500px; width: 100%;"></div>
      </body>
    </html>
    """
    components.html(html_code, height=700)

    # 맛집 리스트 표시
    st.subheader("맛집 리스트")
    st.write(df_restaurants[['상호명', '주소', '운영시간', '교통정보', '대표메뉴']])

    # 관광 명소 리스트 표시
    st.subheader("관광 명소 리스트")
    st.write(df_attractions[['상호명', '주소', '운영시간', '교통정보', '태그']])
#--------------------------------------------------------------------
# ->> 우측 챗봇 표시(크롤링 데이터)
with col2:
  # 네이버 검색 API를 통한 데이터 크롤링
  def search_blog(query, display=4):
    encoded_query = query
    url = f"https://openapi.naver.com/v1/search/blog.json?query={encoded_query}&display={display}"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        items = response.json().get('items', [])
        for item in items:
            # HTML 태그 제거 (<b>, </b>)
            item['title'] = re.sub(r'<\/?b>', '', item['title'])
            item['description'] = re.sub(r'<\/?b>', '', item['description'])
        return items
    else:
        st.error(f"Failed to search blog. Status code: {response.status_code}")
        return []

# 크롤링 데이터 요약
  def summarize_clova(text_to_summarize):
    completion_executor = CompletionExecutor(
        host='https://clovastudio.apigw.ntruss.com',
        api_key=CLOVA_API_KEY,
        api_key_primary_val=CLOVA_API_KEY_PRIMARY_VAL,
        request_id=CLOVA_REQUEST_ID
    )

    # 크롤링 데이터 요약 프롬프트 및 파라미터
    request_data = {
        "messages": [
            {"role": "user", "content": f"다음 글을 3줄로 요약해줘. 친절하게 대답해줘.: {text_to_summarize}"}
        ],
        "topP": 0.6,
        "topK": 0,
        "maxTokens": 150,
        "temperature": 0.5,
        "repeatPenalty": 5.0,
        "includeAiFilters": True,
        "seed": 0
    }
    # 텍스트 요약 요청 및 응답 처리
    summarization_response = completion_executor.execute(request_data)
    return summarization_response if summarization_response else 'Summarization Error'

# 서울 챗봇 표시
  st.title("서울 챗봇 🤖")
  st.write("안녕! 서울에 대해 무엇이든 물어보세요. 질문을 입력하면 친절하게 답변해줄게요!")
  system_prompt = (
        "- 나는 서울의 관광, 맛집, 교통, 문화에 대해 잘 아는 친절한 안내자야.\n"
        "- 반말을 사용해서 질문에 쉽고 명확하게 답변해줄게.\n"
        "- 사용자에게 서울에서 갈 만한 장소, 맛집 추천, 대중교통 정보 등을 직관적으로 알려줘.\n"
        "- 답변은 서울에서 유용한 팁이나 실제 경험을 바탕으로 사례를 들어서 설명해.\n"
        "- 처음 답변시 '안녕! 서울에 대해 뭐든 물어봐. 내가 친절히 알려줄게!'로 시작해."
    )

# 사용자 입력 및 버튼
  user_input = st.text_input("질문을 입력하세요:", placeholder="예: 명동 칼국수 맛집, 서울 산책길 명소")
  submit_button = st.button("질문 보내기")

# 질문 처리 및 응답 출력
  if submit_button and user_input.strip():

    # 프롬프트 구성
    preset_text = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    request_data = {
        'messages': preset_text,
        'topP': 0.6,
        'topK': 0,
        'maxTokens': 512,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }

    # 서울 챗봇 실행
    completion_executor = CompletionExecutor(
        host=CLOVA_HOST,
        api_key=CLOVA_API_KEY,
        api_key_primary_val=CLOVA_API_KEY_PRIMARY_VAL,
        request_id=CLOVA_REQUEST_ID
    )
    # 챗봇 답변 대기
    with st.spinner("답변 생성 중..."):
        response = completion_executor.execute(request_data)

    # 챗봇 답변 출력
    if response:
        st.success("답변이 생성되었습니다!")
        st.write(response)
        st.markdown("<hr style='border: 1px solid gray; margin: 15px 0;'>", unsafe_allow_html=True)
        st.title("네이버 블로그 검색결과")
        blog_items = search_blog(query=user_input)
        for item in blog_items:
            st.subheader(item['title'])

    # 블로그 요약 생성 및 출력
            summary = summarize_clova(item['description'])
            st.write("요약:", summary)
    else:
        st.error("답변 생성에 실패했습니다. 다시 시도해주세요.")
  elif submit_button:
        st.warning("질문을 입력해주세요.")