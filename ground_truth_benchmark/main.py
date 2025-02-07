import streamlit as st

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

# Redirect users to login page initially
st.switch_page("pages/login.py")
