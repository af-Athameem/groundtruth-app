import streamlit as st
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext

# Page setup
st.set_page_config(page_title="Login", layout="wide")

# Hide default Streamlit sidebar
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# SharePoint Credentials
SHAREPOINT_URL = "https://thameema.sharepoint.com/sites/Test"

def authentication(email_user, password_user):
    """Authenticate user and store session."""
    auth = AuthenticationContext(SHAREPOINT_URL)
    
    if not auth.acquire_token_for_user(email_user, password_user):
        st.error("❌ Authentication Failed. Please check your credentials.")
        return None

    ctx = ClientContext(SHAREPOINT_URL, auth)
    web = ctx.web
    ctx.load(web)
    ctx.execute_query()

    return ctx

# Check if user is already logged in
if "authenticated" in st.session_state and st.session_state["authenticated"]:
    st.success("✅ Already logged in!")
    st.switch_page("pages/app.py")  # Redirect to main app

else:
    st.title("Ground Truth Login")
    st.markdown("Enter your credentials to connect.")

    # User inputs
    email_user = st.text_input("📧 Email")
    password_user = st.text_input("🔑 Password", type="password")

    # Login Button
    if st.button("Login"):
        ctx = authentication(email_user, password_user)

        if ctx:
            st.session_state["authenticated"] = True
            st.session_state["email"] = email_user
            st.session_state["password"] = password_user
            st.session_state["ctx"] = ctx  # Store session for SharePoint
            st.success("✅ Authentication Successful! Redirecting...")
            st.switch_page("pages/app.py")  # Redirect to dashboard
