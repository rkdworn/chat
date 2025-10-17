import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

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

# 보내기 버튼 클릭 시
if st.button("보내기"):
    if user_input.strip() == "":
        st.warning("질문을 입력해주세요!")
    else:
        # AI에게 질문 보내기
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )
        # 대화 기록에 추가
        st.session_state.history.append((user_input, response.text))

# 대화 기록 출력
for q, a in st.session_state.history:
    st.write(f"💬 Q: {q}")
    st.write(f"🤖 A: {a}")
