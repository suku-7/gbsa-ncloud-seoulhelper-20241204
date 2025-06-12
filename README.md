![demo-gif](./gcamp_ai_ncloud_team2_demo_20241204.gif)  

---
# 똑똑콩 - 서울 생활 도우미 AI 챗봇

> 관광객과 서울 시민 모두를 위한 생성형 AI 기반 위치 정보 추천 서비스  
> Google Maps API · HyperCLOVA · Naver Search API · Streamlit 기반

---
## 📌 프로젝트 개요

**서울 생활 도우미**는 서울을 방문한 **관광객에게는 유용한 명소·음식점 정보를**,  
**지역 주민에게는 생활 편의를 높이는 정보 제공**을 목표로 한 **생성형 AI 기반 정보 추천 플랫폼**입니다.

> - 다양한 공공데이터 + 생성형 AI를 활용해  
>   실제 사용할 수 있는 "챗봇 기반 인터페이스" 구현  
> - Streamlit 기반 GUI로 위치 기반 시각화 및 실시간 상호작용 지원

---

## 🧩 주요 기능

| 기능 | 설명 |
|------|------|
| 🗺️ 위치 기반 지도 시각화 | 서울시 공공데이터를 바탕으로 음식점 및 명소를 지도 위에 마커로 표시 |
| 🤖 HyperCLOVA 기반 챗봇 | "명동 칼국수 추천해줘", "서울 한강 산책 코스 알려줘"와 같은 자연어 질의 응답 |
| 🔎 Naver 검색 API 연동 | 챗봇 응답과 함께 블로그/포스트 데이터를 검색 및 3줄 요약 표시 |
| 🌐 Geocoding 기능 | 주소 데이터를 위도·경도로 변환하여 지도에 표시 가능 |

---

## 🛠 사용 기술 스택
- **Frontend**: Streamlit (GUI + 지도 시각화)
- **LLM**: HyperCLOVA (생성형 AI)
- **API**: Google Maps API, Naver Search API
- **Data**: 서울시 공공데이터 (관광음식점, 관광명소 정보)
- **ETL**: 주소 → 좌표 변환 (geocoding), JSON 파싱, 데이터 요약 처리

---
## 🧪 시행착오 및 해결 경험

| 문제 | 해결 방법 |
|------|------------|
| 🔒 Instagram 크롤링 차단 | → Naver 블로그/카페 API로 대체 |
| 📍 Naver/Kakao 지도 API 오류 | → Google Maps API로 전환 |
| 📐 Streamlit 지도 UI 구성 어려움 | → 좌우 분할 구조로 레이아웃 최적화 |
| 📌 Geocoding 사용 미숙 | → 주소 기반 위도·경도 변환 구조 습득 |

---

## ✨ 회고 및 배운 점
> **📌 “계획은 변경되기 마련, 중요한 건 유연하게 수정하는 능력”**

- 기획 당시 예상치 못했던 기술적 제약(Instagram 차단, 지도 API 오류 등)을 겪으며,  
  대안을 빠르게 찾아내고 우회하는 과정에서 문제 해결력을 키웠습니다.
- 생성형 AI를 사용하는 것만큼, **데이터 연동과 UX 설계가 중요**함을 체감했습니다.
- 짧은 프로젝트 기간(3일) 속에서 **기획 → 수집 → 처리 → 시각화** 전 과정을 직접 해보며  
  실제 프로덕트 구현에 대한 감각을 익혔습니다.

---

## 🔧 개선 방향 및 확장성

- 🌐 **다국어 지원**: 영어·중국어·일본어 관광객을 위한 데이터 연동
- 📌 **RAG 방식 강화**: 챗봇이 단순 생성형이 아닌 DB 기반 추천까지 수행
- 📍 **지도 연동 개선**: 챗봇이 추천한 장소를 지도에 자동 표시
- 📱 **모바일 대응 UI 및 UX 개선**: 더 직관적이고 예쁜 인터페이스

---

## 👨‍👩‍👧 팀원 역할 분담

| 이름 | 역할 |
|------|------|
| 류근우 | 팀장, 발표, ppt작성, 프로그램 통합 |
| 장수진 | 데이터 수집 및 챗봇 구현, CLOVA 연동 |
| 변소윤 | 프론트 Streamlit UI 구성, 지도 구현 |
| 정용우 | API 통합, Naver 검색 및 요약 처리, 문서 작성 |

---
## API .env 파일

## Google Maps API  
Maps_API_KEY="YOUR_Maps_API_KEY"  

## Naver Clova Studio API  
CLOVA_HOST="https://clovastudio.stream.ntruss.com"  
CLOVA_API_KEY="YOUR_CLOVA_API_KEY"  
CLOVA_API_KEY_PRIMARY_VAL="YOUR_CLOVA_API_KEY_PRIMARY_VAL"  
CLOVA_REQUEST_ID="YOUR_CLOVA_REQUEST_ID"  

## Naver Search API
NAVER_CLIENT_ID="YOUR_NAVER_CLIENT_ID"
NAVER_CLIENT_SECRET="YOUR_NAVER_CLIENT_SECRET"
---
![경과원AI_네이버 클라우드_똑똑콩2조_서울생활도우미_20241204_1 0v_page-0001](https://github.com/user-attachments/assets/0d4826f4-5ead-4e6c-a63c-50d2ddaaba3c)
![경과원AI_네이버 클라우드_똑똑콩2조_서울생활도우미_20241204_1 0v_page-0003](https://github.com/user-attachments/assets/7de39ae2-a8e7-4f28-a28c-918f5a3cda01)
![경과원AI_네이버 클라우드_똑똑콩2조_서울생활도우미_20241204_1 0v_page-0004](https://github.com/user-attachments/assets/a668401f-4d97-4143-858a-611c9eafe050)
![경과원AI_네이버 클라우드_똑똑콩2조_서울생활도우미_20241204_1 0v_page-0005](https://github.com/user-attachments/assets/acef1707-9429-4d6c-bf0b-f11f821a11c1)
![경과원AI_네이버 클라우드_똑똑콩2조_서울생활도우미_20241204_1 0v_page-0006](https://github.com/user-attachments/assets/f968e3b8-b77c-4d0e-9622-50f8698e7e70)
![경과원AI_네이버 클라우드_똑똑콩2조_서울생활도우미_20241204_1 0v_page-0007](https://github.com/user-attachments/assets/ca553c56-7c44-43cd-8d6d-e95f9f5ec506)
![경과원AI_네이버 클라우드_똑똑콩2조_서울생활도우미_20241204_1 0v_page-0020](https://github.com/user-attachments/assets/95e01a2f-29cf-44dc-98cf-e78d820bf232)




