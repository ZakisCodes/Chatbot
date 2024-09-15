# importing necessory libraries
import streamlit as st
#import google.generativeai as genai
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


# loading the env variables
load_dotenv()
# set the page
st.set_page_config(
    page_title="MickAI",
    page_icon="🎇",
    layout="wide",initial_sidebar_state="auto",
)

# hiding the Runner 
st.sidebar.html(
    """
   <style>
   [data-testid="stStatusWidget"]{
         visibility: hidden;
         height: 0;
         position: fixed
          }
    </style>
"""
)



##  Making an custom emoji displaying function
def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


icon("🤖")


# models
model = st.session_state.model
st.write(model)
# initializing the models
## llama3
llama_model = ChatGroq(
    temperature=0.7,
    top_p = 0.7,
    max_tokens=1024,
    model=model,
    api_key=os.getenv("GROQ_API") # Optional if not set as an environment variable)
)

## gemini 1.5 pro
#genai.configure(api_key=os.getenv("Google_API_KEY"))
#gemini_model = genai.GenerativeModel('gemini-1.5-pro')

# title
st.title("MickAI: Speak Freely, Discover More")


# creating the session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# display the chat history
for message in st.session_state.messages:
    avatar = '👤' if message["role"] == "assistant" else '🤖'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])




if prompt := st.chat_input("Say something.."):
    st.chat_message("user", avatar='👤').markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

   

    # fetch response from API
    try:
        if "system" not in st.session_state:
            st.session_state['system'] = "You are a helpful assistant"
        
        system = st.session_state.system
                  
        human = "{text}"
        chat = ChatPromptTemplate.from_messages(
        [("system", system),
          ("human", human)])
        chain = chat | llama_model 
        messages = [
        {"role":"system", "content": st.session_state.system},
        *st.session_state.messages ]
        
        response = chain.invoke(messages)
       
        
        with st.chat_message("assistant", avatar="🤖"):
           st.write(response.content)
        st.session_state.messages.append({"role": "assistant", "content": response.content})
    except Exception as e:
        st.error(e, icon="🚨")
    #try:
     #       
      # if response.content:
       #   st.session_state.messages.append(
        #      {"role": "assistant", "content": response.content})
       ##  st.warning("System is not updated to content other than in strings")
    #except Exception as e:
     #   st.error(e, icon="🚨")
    
# create an feebback from users


