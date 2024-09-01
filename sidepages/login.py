# importing required libraries
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from time import sleep



# creatin session states to more functionality

if "logged" not in st.session_state:
    st.session_state.logged = False
    
if "signup" not in st.session_state:
    st.session_state.signup = False

if "admin" not in st.session_state:
    st.session_state.admin = False

if "default" not in st.session_state:
    st.session_state.default = False

currentpage = st.session_state.default

# function for firebase app initialization
def init_with_service_account(file_path):
    cred = credentials.Certificate(file_path)
    try:
         firebase_admin.get_app()
    except ValueError:
         firebase_admin.initialize_app(cred)
    return firestore.client()
        

# initailazing firebase firestore
cred_path = "D:/Work/Python/Streamlit Apps/Chatbot_org/mickai-fd72a-8872d7000274.json"
db = init_with_service_account(cred_path)

# Login Function page
def login():
    st.title("Login your account here..")
    st.write("username': 'Zakin', password: '123azsdx'")
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
                st.success("Logged in successfully!")
                st.session_state.logged = True
                sleep(0.5)
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