# importing required libraries
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from time import sleep
import os
from dotenv import load_dotenv
load_dotenv()


# creatin session states to more functionality

if "logged" not in st.session_state:
    st.session_state.logged = False
    
if "signup" not in st.session_state:
    st.session_state.signup = False

if "admin" not in st.session_state:
    st.session_state.admin = False

if "default" not in st.session_state:
    st.session_state.default = False

if 'model' not in st.session_state:
   st.session_state.model = "llama3-70b-8192"

currentpage = st.session_state.default

# function for firebase app initialization
def init_with_service_account(credintial):
    cred = credentials.Certificate(credintial)
    try:
         firebase_admin.get_app()
    except ValueError:
         firebase_admin.initialize_app(cred)
    return firestore.client()
        

# initailazing firebase firestore
#cred_path = "D:/Work/Python/Streamlit Apps/Chatbot_org/mickai-fd72a-8872d7000274.json"
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

# Login Function page
def login():
    st.title("Login your account here..")
    with st.form('Login', clear_on_submit=True):
       name = st.text_input("Username: ")
       password = st.text_input("Password", type='password')
       if st.form_submit_button('Submit'):
          userid = db.collection('users').document(name)
          doc_ref = userid.get()
          if doc_ref.exists:
             doc = doc_ref.get('password')
             admin = doc_ref.to_dict().get('admin', False)
             if password == doc:
                 #st.toast('Hooraay you have blasted', icon='😎')
                sleep(0.5)
                st.success("Logged in successfully!")
                st.session_state.logged = True
                if admin:
                  st.session_state.admin = True
                else: pass

                st.rerun()
                
             else:
                st.toast("Password doesn't match", icon='😑')

          else:
            st.toast('Oooh looks like you have not registered', icon='🤔')
    if st.button("Don't have an account here, click to join"):
        st.session_state.signup = True
        st.rerun()

# logout system page 
def logout():
    if st.button("Log out"):
        st.session_state.logged = False
        st.session_state.default = False
        st.session_state.admin = False
        st.rerun()

# All our pages is assigning here
login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("sidepages/setting.py", title="Settings", icon=":material/settings:")
signup_page = st.Page('sidepages/signup.py', title="Sign Up", icon=":material/thumb_up:")
Lab1_page = st.Page('sidepages/test.py', title="Lab1", icon="🧪", default=(currentpage == 'admin'))
Home = st.Page(
    "sidepages/app.py",
    title="Home",
    icon=":material/home:",
    default=(currentpage == 'Home')
)
history = st.Page(
    "sidepages/chat_history.py",
    title="Chat History",
    icon=":material/history:",
    )


if st.session_state.logged:
    if st.session_state.admin == True:
       st.session_state.default = 'admin'
       pg = st.navigation(
           {
            "Home Page": [Home, history],
            "Account": [Lab1_page, settings, logout_page]})
    else:
        st.session_state.default = 'Home'
        pg = st.navigation(
         {
           "Home Page": [Home],
           "Account": [settings, logout_page]})
elif st.session_state.signup:
    pg = st.navigation([signup_page])
else:
    pg = st.navigation([login_page])

pg.run()

   
## create an admin page 