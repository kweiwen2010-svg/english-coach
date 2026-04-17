import streamlit as st
import google.generativeai as genai

# 1. 基礎設定
st.set_page_config(page_title="AI English Coach", layout="centered")
genai.configure(api_key=st.secrets["GEMINI_KEY"])

# 2. 設定老師角色 (針對你的需求：主動問問題、慢語速、糾正錯誤)
SYSTEM_PROMPT = """
You are a patient and friendly English teacher. 
Your goal is to have a casual conversation with the user to help them practice speaking.

RULES:
1. LEAD THE TALK: Always end your response with ONE simple question.
2. SLOW & SIMPLE: Use basic vocabulary (A1-A2 level) and short sentences. 
3. CORRECTION: If the user makes a mistake, gently correct them first, then continue the chat.
4. HELP: If the user says they don't know or asks for help, provide a full example answer and explain it simply.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# 3. 初始化對話歷史
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. UI 介面
st.title("💬 AI 英文老師")
st.caption("一位會主動找你聊天、有耐心的慢速英語教練")

# 顯示對話紀錄
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. 輸入與互動區
prompt = st.chat_input("用英文回覆老師...")

# 老師救我按鈕
if st.button("🆘 老師教我怎麼回答 (Help)"):
    prompt = "Teacher, I'm not sure how to answer. Can you teach me and give me an example?"

if prompt:
    # 顯示使用者訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 回應 (加上 Loading 動畫)
    with st.chat_message("assistant"):
        with st.spinner("老師正在打字中..."):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"發生錯誤：{e}")
