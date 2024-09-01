<<<<<<< HEAD
# Done something with st.authenticator
Sample Login.py
```
import yaml
import streamlit_authenticator as stauth
import streamlit as st
from yaml.loader import SafeLoader
with open('D:/Work/Python/Streamlit Apps/Chatbot_org/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login()

if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')
```
=======
# MickAI Chatbot
Creating an Personalized chatbot for own is every techies one wish, I created this chatbot by using `streamlit`, `langchain`, `groq`. 

More on the way
>>>>>>> 9c52eedb40d6bb0b9e5f78be2e81850009803278
