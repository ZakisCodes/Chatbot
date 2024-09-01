import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


st.title("Registering our account here..")


# initailazing firebase firestore

def init_with_service_account(file_path):
     """
     Initialize the Firestore DB client using a service account
     :param file_path: path to service account
     :return: firestore
     """
     cred = credentials.Certificate(file_path)
     try:
         firebase_admin.get_app()
     except ValueError:
         firebase_admin.initialize_app(cred)
     return firestore.client()
        

cred_path = "D:/Work/Python/Streamlit Apps/Chatbot_org/mickai-fd72a-8872d7000274.json"
db = init_with_service_account(cred_path)

with st.form('Register your account', clear_on_submit=True):
    name = st.text_input("Username: ")
    email = st.text_input("EmailID:")
    password = st.text_input("Password", type='password')
    if st.form_submit_button('Submit'):
        doc_ref = db.collection('users').document(name)
        doc_ref.set({'name': name ,'email': email, 'password': password})
        st.success('Account created succesfully')
        st.session_state.signup = False
        st.rerun()
    else:
        st.error("Please fill the form")