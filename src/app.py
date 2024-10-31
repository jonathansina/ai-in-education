from path_handler import PathManager
import sys

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from main import ChatbotAgent
from path_handler import PathManager
import streamlit as st

with open(path_manager.get_custom_path('style.css')) as css:
    st.set_page_config(page_title="دستیار معلم هوشمند")
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

if 'model' not in st.session_state.keys():
    bot = ChatbotAgent()
    st.session_state['model'] = bot
    
if 'counter' not in st.session_state.keys():
    st.session_state['counter'] = 0

def generate_response(user_input):
    result = st.session_state['model'].get_response(user_input)
    return result


if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "سلام، من دستیار معلم هوشمند انجمن علامه طباطبایی هستم. چطور می‌توانم به شما کمک کنم؟"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == 'user':
            if 'voice' in message.keys():
                st.audio(message['voice'])
            else:
                st.write(message["content"])
        else:
            st.write(message["content"])



if (input := st.chat_input(placeholder="لطفا پیام خود را وارد کنید")):
    if input:
        st.session_state.messages.append({"role": "user", "content": input})
        with st.chat_message("user"):
            st.write(input)
            
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("لطفا چند لحظه منتظر باشید..."):
            response = generate_response(input) 
            if isinstance(response, list):
                for i in response:
                    st.write(i) 
            else:
                st.write(response)
    
    if isinstance(response, list):
        for i in response:
            message = {"role": "assistant", "content": i}
            st.session_state.messages.append(message)
    else:
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
