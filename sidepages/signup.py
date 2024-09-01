import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os 
from dotenv import load_dotenv
load_dotenv()

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
        
firebase_credentials = { "type": os.getenv('type'),
  "project_id": os.getenv('project_id'),
  "private_key_id": os.getenv('private_key_id'),
  "private_key": os.getenv('private_key'),
  "client_email": os.getenv('client_email'),
  "client_id": os.getenv('client_id'),
  "auth_uri": os.getenv('auth_uri'),
  "token_uri": os.getenv('token_uri'),
  "auth_provider_x509_cert_url": os.getenv('auth_provider_x509_cert_url'),
  "client_x509_cert_url": os.getenv('client_x509_cert_url'),
  "universe_domain": os.getenv('universe_domain')}
db = init_with_service_account(firebase_credentials)

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
