# importing necessory libraries
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq



load_dotenv()
chat = ChatGroq(
    temperature=0,
    model="llama3-70b-8192",
    api_key=os.getenv("GROQ_API") # Optional if not set as an environment variable
)
human = st.chat_input("Enter your mesg")
#system = "You are a data analyst specialist."
#system = st.text_input("Exaplin who is the AI")
#human = "{text}"
#prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
if human:
    with st.chat_message("user"):
        st.write(human)
    with st.chat_message("assistant", avatar="🎃"):
        st.write(human)
#prompt = input("Enter your prompt:")
#sdf = SmartDataframe(df, config={"llm": chat})
#chain = prompt | chat
#response = st.text_area("Enter your Prompt")
#res = chain.invoke({"text": response})
#res = sdf.chat(prompt)
#if st.button("Generate"):
 #   with st.spinner("Wait a second........"):
  #      st.write(res.text)
#else:
 #   print("Problem")
genai.configure(api_key=os.getenv("Google_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')
st.title("Our Own Gemini😎")
prompt=st.text_area("Enter your prompt")
if st.button("Generate"):
    res = model.generate_content(prompt)
    st.success(res.text)
else:
    st.warning("Please enter an prompt in above field")


