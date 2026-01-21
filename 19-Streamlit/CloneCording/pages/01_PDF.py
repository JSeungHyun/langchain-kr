import streamlit as st

# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_teddynote.prompts import load_prompt
from langchain_core.messages.chat import ChatMessage
from langchainhub import Client
import glob
import os

# API KEY 정보로드
load_dotenv()
st.title("PDF 기반 QA💬")

#캐시 디렉토리 생성
if not os.path.exists(".cache"):
    os.mkdir(".cache")

if not os.path.exists(".cache/embeddings"):
    os.mkdir(".cache/embeddings")

if not os.path.exists(".cache/files"):
    os.mkdir(".cache/files")

# 초기화 된 적 없으면 실행 (최초 1회)
if "messages" not in st.session_state:
    # 대화기록을 저장하는 저장소
    st.session_state["messages"] = []

# 사이드바 생성
with st.sidebar:
    claer_btn = st.button("대화 초기화")
    # 파일 업로더
    uploaded_file = st.file_uploader("파일 업로드", type=["pdf"])
    selectedPrompt = "prompts/pdf-rag.yaml"

# 저장된 대화를 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

# 세션에 메세지 추가
def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

# 파일을 캐시 저장(시간이 오래 걸리는 작업을 처리할 예정)
@st.cache_resource(show_spinner="업로드한 파일을 처리 중입니다...")
def embed_file(file):
    # 업로드한 파일을 캐시 디렉토리에 저장
    file_content = file.read()
    file_path = f"./.cache/files/${file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)

# 파일이 업로드 되었을 때
if uploaded_file:
    embed_file(uploaded_file)

# 체인 생성
def create_chain(prompt_file_path):
    prompt = load_prompt(prompt_file_path, encoding="utf-8")

    # GPT
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    # 출력 파서
    output_parser = StrOutputParser()
    # 체인 생성
    print(type(prompt))
    chain = prompt | llm | output_parser
    return chain


# 대화 초기화 버튼 클릭 시
if claer_btn:
    st.session_state["messages"] = []

# 이전 대화기록 출력
print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")

# 사용자의 입력이 들어왔을 경우
if user_input:
    st.chat_message("user").write(user_input)
    chain = create_chain(selectedPrompt)

    # 스트리밍 호출
    response = chain.stream({"question": user_input})
    with st.chat_message("assistant"):
        container = st.empty()
        ai_answer = ""
        for token in response:
            ai_answer += token
            container.markdown(ai_answer)

    # 대화기록 저장
    add_message("user", user_input)
    add_message("assistant", ai_answer)