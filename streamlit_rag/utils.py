import streamlit as st
from time import sleep
# from streamlit.runtime.scriptrunner import get_script_run_ctx
# from streamlit.source_util import get_pages


# def get_current_page_name():
#     """Get the name of the current running Streamlit page."""
#     ctx = get_script_run_ctx()
#     if ctx is None:
#         return None  # Prevent errors

#     pages = get_pages("")  # Get all registered pages

#     return pages[ctx.page_script_hash]["page_name"]


def check_authentication():
    """Redirect to login page if user is not authenticated."""
    if not st.session_state.get("authenticated", False):
        st.warning("You must log in first.")
        sleep(1)
        st.switch_page("pages/login.py")  


def logout():
    """Fully clear session state and redirect to login."""
    
    st.session_state.clear() 
    st.session_state["logged_out"] = True  

    st.info("✅ Logged out successfully! Redirecting to login page...")
    sleep(1)

    # Redirect to login page
    st.switch_page("pages/login.py") 


