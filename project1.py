import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import time

# .env 파일 읽기
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Gemini 클라이언트 생성
client = genai.Client(api_key=api_key)

# Streamlit UI
st.title("강재구 챗봇")

user_input = st.text_input("질문을 입력하세요:")

# 대화 기록 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# RPM/TPM 제한 초기화
if 'last_requests' not in st.session_state:
    st.session_state.last_requests = []  # [(timestamp, token_count), ...]

# 최대 제한
MAX_RPM = 10           # 분당 최대 요청
MAX_TPM = 250_000      # 분당 최대 토큰

def can_send_request(token_count):
    now = time.time()
    # 60초 이전 요청 제거
    st.session_state.last_requests = [
        (t, c) for t, c in st.session_state.last_requests if now - t < 60
    ]
    current_rpm = len(st.session_state.last_requests)
    current_tpm = sum(c for _, c in st.session_state.last_requests)
    if current_rpm >= MAX_RPM:
        return False, "⚠️ 1분에 최대 요청 횟수를 초과했습니다. 잠시 기다려주세요."
    if current_tpm + token_count > MAX_TPM:
        return False, "⚠️ 1분에 최대 토큰 사용량을 초과했습니다. 잠시 기다려주세요."
    return True, ""

# 보내기 버튼 클릭 시
if st.button("보내기"):
    if user_input.strip() == "":
        st.warning("질문을 입력해주세요!")
    else:
        # 대략적인 토큰 수 계산 (질문 길이 + 예상 답변)
        token_count = len(user_input.split()) + 50  # 50은 답변 예측 토큰
        allowed, msg = can_send_request(token_count)
        if not allowed:
            st.warning(msg)
        else:
            # API 요청
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input
            )
            st.session_state.history.append((user_input, response.text))
            st.session_state.last_requests.append((time.time(), token_count))

# 대화 기록 출력
for q, a in st.session_state.history:
    st.write(f"💬 Q: {q}")
    st.write(f"🤖 A: {a}")
