import streamlit as st

# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_teddynote.prompts import load_prompt
from langchain_core.messages.chat import ChatMessage
from langchainhub import Client

# API KEY 정보로드
load_dotenv()
st.title("Example  :blue[AI] :sunglasses:")

# 초기화 된 적 없으면 실행 (최초 1회)
if "messages" not in st.session_state:
    # 대화기록을 저장하는 저장소
    st.session_state["messages"] = []

# 버튼 생성
with st.sidebar:
    claer_btn = st.button("대화 초기화")
    selectedPrompt = st.selectbox(
        "프롬프트를 선택해 주세요", ("기본모드", "블로그 게시글", "요약"), index=0
    )


# 세션에 메세지 추가
def add_message(role, message):
    # ChatMessage("user", content=user_input)
    # ChatMessage("assistant", content=user_input)
    # st.session_state["messages"].append(("user", user_input))
    # st.session_state["messages"].append(("assistant", user_input))
    st.session_state["messages"].append(ChatMessage(role=role, content=message))


# 저장된 대화를 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)


# 체인 생성
def create_chain(prompt_type):
    # prompt | llm | output_pasrser

    # 프롬프트
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "당신은 친절한 AI 어시스턴트입니다. 다음의 질문에 간결하게 답변해주세요.",
            ),
            ("user", "#Question:\n{question}"),
        ]
    )

    if prompt_type == "블로그 게시글":
        prompt = load_prompt("prompts/blog.yaml", encoding="utf-8")
    elif prompt_type == "요약":
        client = Client()
        prompt = client.pull("teddynote/chain-of-density-map-korean")

    # GPT
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
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
    # with st.chat_message("user"):
    #     st.write(user_input)
    # 웹에 대화를 출력, 동일 로직
    st.chat_message("user").write(user_input)
    chain = create_chain(selectedPrompt)
    # ai_answer = chain.invoke({"question": user_input})

    # 스트리밍 호출
    response = chain.stream({"question": user_input})
    with st.chat_message("assistant"):
        container = st.empty()
        ai_answer = ""
        for token in response:
            ai_answer += token
            container.markdown(ai_answer)

    # st.chat_message("assistant").write(ai_answer)

    # 대화기록 저장
    add_message("user", user_input)
    add_message("assistant", ai_answer)

# 마크다운 기능
# st.markdown("*Streamlit* is **really** ***cool***.")
# st.markdown('''
#     :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
#     :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
# st.markdown("Here's a bouquet &mdash;\
#             :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

# multi = '''If you end a line with two spaces,
# a soft return is used for the next line.

# Two (or more) newline characters in a row will result in a hard return.
# '''
# st.markdown(multi)
