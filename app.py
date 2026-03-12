import time
from http.client import responses

import streamlit as st
from agent.react_agent import ReactAgent
from utils.config_handler import prompts_conf

st.title("智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "您好，我是客服小祥，请问有什么可以帮到您吗？"}]

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])
# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})
    response_messages = []
    with st.spinner("思考中..."):
        time.sleep(1)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char
        res = st.session_state["agent"].execute_stream(prompt)
        st.chat_message("assistant").write_stream(capture(res, response_messages))
        st.session_state["message"].append({"role": "assistant", "content": response_messages})
        st.rerun()
