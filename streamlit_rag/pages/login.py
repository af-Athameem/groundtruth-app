import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import time
import os

# Set Page Configuration
st.set_page_config(
    page_title="Login | Ground Truth Benchmark",
    layout="centered"
)

# Get the absolute path of the root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load config.yaml from the root directory
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

try:
    with open(CONFIG_PATH, "r") as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("⚠️ Configuration file 'config.yaml' not found.")
    st.stop()

# Initialize Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

st.markdown("<h1 style='text-align: center;'>Ground Truth Benchmark</h1>", unsafe_allow_html=True)

# Show login form
name, authentication_status, username = authenticator.login(
    'main', fields={'Form name': 'Login Form'}
)

# Store authentication state
if authentication_status:
    if not st.session_state.get("logged_out", False):  # Prevent re-login loop
        st.session_state["authenticated"] = True
        st.session_state["username"] = username
        st.session_state["name"] = name
        
        st.session_state["redirect_to_app"] = True
        time.sleep(1)
        st.rerun()  # Refresh to trigger redirect

#Redirect if login is successful
if st.session_state.get("redirect_to_app", False):
    del st.session_state["redirect_to_app"]  
    st.session_state.pop("logged_out", None)  
    st.switch_page("app.py")  


elif authentication_status is False:
    st.error("Incorrect username or password. Please try again.")

elif authentication_status is None:
    st.warning("⚠️ Please enter your username and password.")

# Logout Button in Sidebar
if authentication_status:
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key] 
        time.sleep(1)
        st.rerun()  
