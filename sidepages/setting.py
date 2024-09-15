import streamlit as st

st.title("SETTINGS")
st.subheader("You can customize thi settings according to your need")

st.markdown("### Who Am I?")
st.write("You can improve the chat response by telling what role does this Ai need to be")


system = st.text_input("Please tell me who am I?", value="You are a helpful assistant")

st.subheader('Select your model')
model = st.selectbox("Modal Name",
             ("llama3-70b-8192","gemma-7b-it","gemma2-9b-it","llama3-groq-70b-8192-tool-use-preview"))

if 'model' not in st.session_state:
   st.session_state.model = "llama3-70b-8192"

if st.button("Save"):
   st.session_state['system'] = system
   st.session_state.model = model
else:
   pass
   #st.session_state.system = "You are a helpful assistant"