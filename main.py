import openai
import streamlit as st


st.set_page_config(page_title="Chatgpt", page_icon='gpt.png')

with st.sidebar:
    api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password", autocomplete="new-password")
    if not api_key:
        st.error('Enter the API Key', icon="🚨")
        text_1 = "If you dont have an api key, visit the "
        text_2 = "official website"
        text_3 = " to get it"
        url = 'https://platform.openai.com/signup?launch'
        st.markdown(f"{text_1}[{text_2}]({url}){text_3}")
    else:
        st.success('API Key entered!', icon="✅")

st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
