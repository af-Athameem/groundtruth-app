import streamlit_authenticator as stauth

# List of plain-text passwords
passwords = ['', '']

# Hash the passwords
hashed_passwords = stauth.Hasher(passwords).generate()

print(hashed_passwords)
