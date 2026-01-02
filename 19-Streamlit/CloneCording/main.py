import streamlit as st

st.title("Example  :blue[AI] :sunglasses:")


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


# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")

# 사용자의 입력이 들어왔을 경우
if user_input:
    st.write(f"사용자 입력 : {user_input}")