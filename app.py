# importing necessory libraries
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from typing import Generator
#global response
#response = " "

# loading the env variables
load_dotenv()

# set the page
st.set_page_config(
    page_title="MickAI",
    page_icon="🎇",
    layout="wide",initial_sidebar_state="auto",
)
def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


icon("🏎️")
# initializing the models
## llama3
llama_model = ChatGroq(
    temperature=0,
    model="llama3-70b-8192",
    api_key=os.getenv("GROQ_API") # Optional if not set as an environment variable
)
## gemini 1.5 pro
genai.configure(api_key=os.getenv("Google_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

# title
st.title("Mick Your Own Chatbot! ")

# Making our model to give more appropriate answers
#system = st.text_input("Exaplin who is the AI")

# creating the session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# display the chat history
for message in st.session_state.messages:
    avatar = '🎃' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


if prompt := st.chat_input("Say something.."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)
        #response = (prompt)

    # fetch response from API
    try:
        #if st.session_state.system is None:
         #   st.session_state.system = "You are a helpful assistant"
          #  system = st.session_state.system
        #else:
        if "system" not in st.session_state:
            st.session_state['system'] = "You are a helpful assistant"
        
        system = st.session_state.system
                  
        human = "{text}"
        chat = ChatPromptTemplate.from_messages(
        [("system", system),
          ("human", human)])
        chain = chat | llama_model
        response = chain.invoke({"text": prompt})
    
        with st.chat_message("assistant", avatar="🎃"):
           st.write(response.content)
        #st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(e, icon="🚨")
    try:
            
       if response.content:
          st.session_state.messages.append(
              {"role": "assistant", "content": response.content})
       else:
          st.warning("System is not updated to content other than in strings")
    except Exception as e:
        st.error(e, icon="🚨")
    
# create an feebback from users


