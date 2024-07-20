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
st.title("Our Own Gemini😎")
col1, col2, col3, col4, col5 = st.columns(5)
system = col1.text_input("Exaplin who is the AI")

# creating the session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# display the chat history
for message in st.session_state.messages:
    with st.chat_message(message.get("role")):
        st.write(message.get("content"))


user = st.chat_input("Say something..")
#system = "You are a data analyst specialist."
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
chain = prompt | llama_model


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if user:
    with st.chat_message("user"):
        st.write(user)
        res = chain.invoke({"text": user})
    
    st.session_state.messages.append({"role": "user", "content": user})
    
    with st.chat_message("assistant", avatar="🎃"):
        response = st.write(res.content)
        print(type(res))
    st.session_state.messages.append({"role": "assistant", "content": response})
    #with st.chat_message("assistant", avatar="🎃"):
     #   #chat_responses_generator  = generate_chat_responses(res.content)
      #  full_response = st.write(res)
       # print(type(res))
   # st.session_state.messages.append({"role": "assistant", "content": response})
    #    if isinstance(full_response, str):
     #       st.session_state.messages.append(
      #      {"role": "assistant", "content": full_response})
       # else:
        ## Handle the case where full_response is not a string
         #   combined_response = "\n".join(str(item) for item in full_response)
          #  st.session_state.messages.append(
           # {"role": "assistant", "content": combined_response})
#prompt = input("Enter your prompt:")
#response = st.text_area("Enter your Prompt")
#res = sdf.chat(prompt)
#if st.button("Generate"):
 #   with st.spinner("Wait a second........"):
  #      st.write(res.text)
#else:
 #   print("Problem")
#prompt=st.text_area("Enter your prompt")
#if st.button("Generate"):
 #   res = gemini_model.generate_content(prompt)
  #  st.success(res.text)
#else:
 #   st.warning("Please enter an prompt in above field")


