import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("Google_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')
st.title("Our Own Gemini😎")
prompt=st.text_area("Enter your prompt")
if st.button("Generate"):
    res = model.generate_content(prompt)
    st.success(res.text)
else:
    st.warning("Please enter an prompt in above field")


