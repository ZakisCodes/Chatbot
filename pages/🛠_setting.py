import streamlit as st

st.title("SETTINGS")
st.subheader("You can customize thi settings according to your need")

st.markdown("### Who Am I?")
st.write("You can improve the chat response by telling what role does this Ai need to be")


system = st.text_input("Please tell me who am I?", value="You are a helpful assistant(By default)")
if st.button("Save"):
   st.session_state['system'] = system
else:
   pass
   #st.session_state.system = "You are a helpful assistant"
